from sys import maxint

try:
    import json
except ImportError:
    import simplejson as json

#Download the latest websocket-client from https://pypi.python.org/pypi/websocket-client/
import websocket

#AutoPy must be installed: https://pypi.python.org/pypi/autopy/
from autopy import screen, mouse

rangeX = 150
minY = 100
maxY = 300
click = False

def on_message(ws, message):
    global screenWidth, screenHeight, rangeX, minY, maxY, click

    frame = json.loads(message)

    if len(frame['hands']) < 1:
        return

    hand = frame['hands'][0]['palmPosition']

    cursorX = int(hand[0]+rangeX)*(screenWidth/rangeX)
    cursorY = screenHeight-int(hand[1]-minY)*(screenHeight/(maxY-minY))

    if screen.point_visible(cursorX, cursorY):
        mouse.move(cursorX, cursorY)

    if len(frame["pointables"]) < 3 and not(click):
        click = True
        mouse.toggle(click, mouse.LEFT_BUTTON)
    elif click:
        click = False
        mouse.toggle(click, mouse.LEFT_BUTTON)


def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### open ###"

if __name__ == "__main__":

    global screenWidth, screenHeight

    screenWidth = screen.get_size()[0]
    screenHeight = screen.get_size()[1]

    #Uncomment the line below to view the raw JSON from the websocket
    #websocket.enableTrace(True)

    ws = websocket.WebSocketApp("ws://127.0.0.1:6437",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()
