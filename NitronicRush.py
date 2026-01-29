try:
    import json
except ImportError:
    import simplejson as json

#Download the latest websocket-client from https://pypi.python.org/pypi/websocket-client/
import websocket

#AutoPy must be installed: https://pypi.python.org/pypi/autopy/
from autopy import key

key_accelerate = key.K_UP
key_brake = key.K_DOWN
key_left = key.K_LEFT
key_right = key.K_RIGHT
key_nitro = key.K_SHIFT

status_accelerate = False
status_brake = False
status_left = False
status_right = False
status_nitro = False

steeringRange = 30
accelerationRange = 30
nitroRange = 0


def on_message(ws, message):

    global steeringRange, accelerationRange, nitroRange
    global key_accelerate, key_brake, key_left, key_right, key_nitro
    global status_accelerate, status_brake, status_left, status_right, status_nitro

    frame = json.loads(message)

    if len(frame['hands']) < 2:
        return

    leftHand = frame['hands'][0]
    rightHand = frame['hands'][1]

    if leftHand['palmPosition'][0] > rightHand['palmPosition'][0]:
        leftHand, rightHand = rightHand, leftHand

    steering = leftHand['palmPosition'][1]-rightHand['palmPosition'][1]

    if steering > steeringRange:
        if not(status_right):
            status_right = True
            key.toggle(key_right, True)
    elif steering < -steeringRange:
        if not(status_left):
            status_left = True
            key.toggle(key_left, True)
    else:
        if status_left:
            status_left = False
            key.toggle(key_left, False)
        if status_right:
            status_right = False
            key.toggle(key_right, False)

    acceleration = (leftHand['palmPosition'][2]+rightHand['palmPosition'][2])/2

    if acceleration < nitroRange:
        if not(status_nitro):
            status_nitro = True
            key.toggle(key_nitro, True)
    elif acceleration < accelerationRange:
        if not(status_accelerate):
            status_accelerate = True
            key.toggle(key_accelerate, True)
    elif acceleration > (2*accelerationRange):
        if not(status_brake):
            status_brake = True
            key.toggle(key_brake, True)
    else:
        if status_nitro:
            status_nitro = False
            key.toggle(key_nitro, False)
        if status_accelerate:
            status_accelerate = False
            key.toggle(key_accelerate, False)
        if status_brake:
            status_brake = False
            key.toggle(key_brake, False)


def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### open ###"

if __name__ == "__main__":

    #Uncomment the line below to view the raw JSON from the websocket
    #websocket.enableTrace(True)

    ws = websocket.WebSocketApp("ws://127.0.0.1:6437",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()
