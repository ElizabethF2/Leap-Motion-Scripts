from time import sleep
try:
    import json
except ImportError:
    import simplejson as json

#Download the latest websocket-client from https://pypi.python.org/pypi/websocket-client/
import websocket

#AutoPy must be installed: https://pypi.python.org/pypi/autopy/
from autopy import key

key_left = key.K_LEFT
key_right = key.K_RIGHT
key_jump = ord('X')
key_clap = ord('K')

status_left = False
status_right = False
status_jump = False
status_clap = False

hitThreshold = 400
sleepTime = 500


def on_message(ws, message):

    global hitThreshold, sleepTime
    global key_left, key_right, key_jump, key_clap
    global status_left, status_right, status_jump, status_clap

    frame = json.loads(message)

    if len(frame['hands']) < 2:
        return

    leftHand = frame['hands'][0]
    rightHand = frame['hands'][1]

    if leftHand['palmPosition'][0] > rightHand['palmPosition'][0]:
        leftHand, rightHand = rightHand, leftHand

    hitLeft = False
    hitRight = False

    if leftHand['palmVelocity'][1] < -hitThreshold:
        hitLeft = True

    if rightHand['palmVelocity'][1] < -hitThreshold:
        hitRight = True

    tempSleep = sleepTime
    if leftHand['palmVelocity'][0] > hitThreshold and rightHand['palmVelocity'][0] < -hitThreshold:
        key.toggle(key_clap, True)
        status_clap = True
    elif hitLeft and hitRight:
        key.toggle(key_jump, True)
        status_jump = True
    elif hitLeft:
        key.toggle(key_left, True)
        status_left = True
    elif hitRight:
        key.toggle(key_right, True)
        status_right = True
    else:
        if status_clap:
            key.toggle(key_clap, False)
            status_clap = False
        if status_jump:
            key.toggle(key_jump, False)
            status_jump = False
        if status_left:
            key.toggle(key_left, False)
            status_left = False
        if status_right:
            key.toggle(key_right, False)
            status_right = False

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
