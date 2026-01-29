import Leap, sys
from autopy import screen, mouse, alert
from time import sleep

screenWidth = 0
screenHeight = 0
rangeX = 150
minY = 100
maxY = 300
click = False

"""
class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"
"""
def on_frame(controller):
    global screenWidth, screenHeight, rangeX, minY, maxY, click

    frame = controller.frame()

    finger1 = frame.hands[0].fingers[0].tip_position
    finger2 = frame.hands[0].fingers[1].tip_position

    pointerFinger = finger1
    if(finger2[2] < finger1[2]):
        pointerFinger = finger2

    cursorX = int(pointerFinger[0]+rangeX)*(screenWidth/rangeX)
    cursorY = screenHeight-int(pointerFinger[1]-minY)*(screenHeight/(maxY-minY))

    if screen.point_visible(cursorX, cursorY):
        mouse.move(cursorX, cursorY)
    #print "%d, %d" % (cursorX, cursorY)

    if len(frame.fingers) == 1 and not(click):
        click = True
        mouse.toggle(click, mouse.LEFT_BUTTON)

    if len(frame.fingers) == 2 and click:
        click = False
        mouse.toggle(click, mouse.LEFT_BUTTON)

    #if len(frame.fingers) == 5:
    #    print "Cover!    %d" % (frame.timestamp)

def main():
    global screenWidth, screenHeight

    screenWidth = screen.get_size()[0]
    screenHeight = screen.get_size()[1]

    # Create a sample listener and controller
    #listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    #controller.add_listener(listener)

    while(True):
        sleep(.005)
        on_frame(controller)

    # Remove the sample listener when done
    #controller.remove_listener(listener)


if __name__ == "__main__":
    main()
