import mouse
import time
import math

rotation_velocity = 0.01

left_button = False
right_button = False
velocity = 0.0
rotation = 0.0
pos_x = 0.0
pos_y = 0.0

def onEvent(event):
    global velocity, left_button, right_button
    if type(event) == mouse._mouse_event.WheelEvent:
        velocity += event.delta
    if type(event) == mouse._mouse_event.ButtonEvent:
        val = True if event.event_type == 'down' else False
        if event.button == 'left':
            left_button = val
        elif event.button == 'right':
            right_button = val
        print(event)

def updatePosition():
    mouse.move(pos_x, pos_y)

def enforceBounds():
    global pos_x, pos_y
    pos_x = max(0, pos_x)
    pos_y = max(0, pos_y)
    pox_x = min(512, pos_x)
    pox_y = min(512, pos_y)

def tick():
    global pos_x, pos_y, rotation
    pos_x += velocity*math.sin(rotation)
    pos_y += velocity*math.cos(rotation)
    if left_button:
        rotation -= rotation_velocity
    if right_button:
        rotation += rotation_velocity
    enforceBounds()
    # print('r'+str(right_button))
    # print('l'+str(left_button))
    print(f"{pos_x}, {pos_y}")
    updatePosition()

mouse.hook(onEvent)

while True:
    time.sleep(0.01)
    tick()
