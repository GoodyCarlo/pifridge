from gpiozero import Button
from signal import pause

button = Button(27)
button.hold_time = .3

closedFlag = True

def closed():
    global closedFlag

    if not closedFlag:
        print("closed\n")
        closedFlag = True


def open(): 
    
    print("open\n")
    
    global closedFlag
    closedFlag = False

button.when_held = open
button.when_released = closed

pause()