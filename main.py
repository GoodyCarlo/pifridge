from gpiozero import Button
from signal import pause
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
button = Button(26)

button.hold_time = .1

closedFlag = True

camera = Picamera2()
preview_config = camera.create_preview_configuration()
camera.configure(preview_config)
encoder = H264Encoder()
camera.start_preview(Preview.QTGL)
camera.stop_preview()

def closed():
    global closedFlag

    if not closedFlag:
        print("closed\n")
        closedFlag = True
        camera.stop_recording()
        camera.stop_preview()

def open():
    
    print("open\n")
    camera.start_preview(Preview.QTGL)
    camera.start_recording(encoder, 'test.h264', quality=Quality.HIGH)
    
    global closedFlag
    closedFlag = False

button.when_held = open
button.when_released = closed

pause()