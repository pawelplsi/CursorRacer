import mouse
import time
import math
import subprocess
import screeninfo
from pynput.mouse import Controller as MouseController, Button

rotation_velocity = 0.05

class MouseDisabler:
    def __init__(self):
        self.scan_done = False
        self.mouse_ids = []

    def scan(self):
        proc = subprocess.Popen(['xinput','list','--id-only'],stdout=subprocess.PIPE)
        ids = [int(line) for line in proc.stdout.readlines()]
        proc = subprocess.Popen(['xinput','list'],stdout=subprocess.PIPE)
        lines = [str(line) for line in proc.stdout.readlines()]
        self.mouse_ids = []
        for i in range(0, len(ids)):
            if 'pointer' in lines[i]:
                self.mouse_ids.append(ids[i])
        self.scan_done = True

    def disable(self):
        if not self.scan_done:
            self.scan()
        for id in self.mouse_ids:
            subprocess.Popen(['xinput','disable',str(id)], stderr=open("NUL","w"))

    def enable(self):
        for id in self.mouse_ids:
            subprocess.Popen(['xinput','enable',str(id)], stderr=open("NUL","w"))

class Controller:
    def __init__(self):
        self.left_button = False
        self.right_button = False
        self.middle_button = False
        self.out_left = False
        self.out_right = False
        self.out_middle = False
        self.velocity = 0.0
        self.rotation = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.max_x = 0
        self.max_y = 0
        self.mouse_ctrl = MouseController()


    def onEvent(self, event):
        if type(event) == mouse._mouse_event.WheelEvent:
            if self.left_button and self.right_button:
                self.mouse_ctrl.scroll(0, event.delta)
            else:
                self.velocity += event.delta
                self.velocity = max(0, self.velocity)
        if type(event) == mouse._mouse_event.ButtonEvent:
            val = True if event.event_type == 'down' else False
            if event.button == 'middle':
                self.middle_button = val
            elif event.button == 'left':
                self.left_button = val
            elif event.button == 'right':
                self.right_button = val
            self.updateButtons()

    def updatePosition(self):
        mouse.move(self.pos_x, self.pos_y)

    def updateButtons(self):
        left, right, middle = self.outputButtons(self.left_button, self.right_button, self.middle_button)
        if(left != self.out_left):
            self.sendButtonEvent(Button.left, left)
            self.out_left = left
        if(right != self.out_right):
            self.sendButtonEvent(Button.right, right)
            self.out_right = right
        if(middle != self.out_middle):
            self.sendButtonEvent(Button.middle, middle)
            self.out_middle = middle

    def sendButtonEvent(self, button, down):
        if down:
            self.mouse_ctrl.press(button)
        else:
            self.mouse_ctrl.release(button)

    def outputButtons(self, left, right, middle):
        zero = (False, False, False)
        if left and right:
            if middle:
                return (False, False, True)
            return zero
        elif middle:
            return (left, right, False)
        return zero
    
    def bounceBounds(self):
        if self.pos_x < 0:
            self.pos_x = 0
            self.rotation = math.pi - self.rotation
        if self.pos_y < 0:
            self.pso_y = 0
            self.rotation = -self.rotation
        if self.pos_x > self.max_x:
            self.pos_x = self.max_x
            self.rotation = math.pi - self.rotation
        if self.pos_y > self.max_y:
            self.pso_y = self.max_y
            self.rotation = -self.rotation


    def tick(self):
        self.pos_x += self.velocity*math.cos(self.rotation)
        self.pos_y += self.velocity*math.sin(self.rotation)
        if self.left_button and not self.middle_button:
            self.rotation -= rotation_velocity
        if self.right_button and not self.middle_button:
            self.rotation += rotation_velocity
        if(self.left_button and self.right_button):
            self.velocity = 0.0
        self.bounceBounds()
        # print('r'+str(right_button))
        # print('l'+str(left_button))
        # print(f"{self.pos_x}, {self.pos_y}")
        self.updatePosition()

ctrl = Controller()

def callback(e):
    ctrl.onEvent(e)

def start():
    try:
        m_disabler = MouseDisabler()
        # m_disabler.scan()
        m_disabler.disable()
        ctrl.max_x = max([m.width for m in screeninfo.get_monitors()])
        ctrl.max_y = max([m.height for m in screeninfo.get_monitors()])
        ctrl.pos_x, ctrl.pos_y = mouse.get_position()

        mouse.hook(callback)
        while True:
            time.sleep(0.01)
            # mouse.double_click()
            ctrl.tick()
    except KeyboardInterrupt:
        m_disabler.enable()
        pass


start()
