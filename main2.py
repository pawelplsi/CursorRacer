import mouse
import time
import math
import subprocess

rotation_velocity = 0.05

class MouseDisabler:
    def __init__(self):
        self.scan_done = False
        self.mouse_ids = []

    def scan(self):
        proc = subprocess.Popen(['xinput','list','--id-only'],stdout=subprocess.PIPE)
        ids = [int(line) for line in proc.stdout.readlines()]
        proc = subprocess.Popen(['xinput','list','--name-only'],stdout=subprocess.PIPE)
        names = [str(line) for line in proc.stdout.readlines()]
        self.mouse_ids = []
        for i in range(0, len(ids)):
            if 'mouse' in names[i].lower():
                self.mouse_ids.append(ids[i])
        self.scan_done = True

    def disable(self):
        if not self.scan_done:
            scan(self)
        for id in self.mouse_ids:
            subprocess.Popen(['xinput','disable',str(id)])

    def enable(self):
        for id in self.mouse_ids:
            subprocess.Popen(['xinput','enable',str(id)])

class Controller:
    def __init__(self):
        self.left_button = False
        self.right_button = False
        self.velocity = 0.0
        self.rotation = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.max_x = 1920
        self.max_y = 1080


    def onEvent(self, event):
        if type(event) == mouse._mouse_event.WheelEvent:
            self.velocity += event.delta
            self.velocity = max(0, self.velocity)
        if type(event) == mouse._mouse_event.ButtonEvent:
            val = True if event.event_type == 'down' else False
            if event.button == 'left':
                self.left_button = val
            elif event.button == 'right':
                self.right_button = val

    def updatePosition(self):
        mouse.move(self.pos_x, self.pos_y)

    def enforceBounds(self):
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
        if self.left_button:
            self.rotation -= rotation_velocity
        if self.right_button:
            self.rotation += rotation_velocity
        self.enforceBounds()
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
        m_disabler.scan()
        m_disabler.disable()
        ctrl.pos_x, ctrl.pos_y = mouse.get_position()
        mouse.hook(callback)
        while True:
            time.sleep(0.01)
            ctrl.tick()
    except KeyboardInterrupt:
        m_disabler.enable()
        pass


start()
