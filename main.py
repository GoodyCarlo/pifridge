from gpiozero import Button
from signal import pause
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from libcamera import controls

button = Button(26)
button.hold_time = .1

closedFlag = True

camera = Picamera2()
mode = camera.sensor_modes[0]
config = camera.create_preview_configuration(
    sensor={'output_size': mode['size'], 'bit_depth':mode['bit_depth']},
    raw={'fps':30, 'size':(640,640)})
camera.configure(config)
camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

encoder = H264Encoder(10000000000)

camera.start_preview(Preview.QTGL)
camera.stop_preview()

def closed():
    global closedFlag

    if not closedFlag:
        print("closed\n")
        closedFlag = True
        camera.stop_recording()
        # camera.stop_preview()

def open(): 
    
    print("open\n")
    camera.start_recording(encoder, 'test.h264')
    
    global closedFlag
    closedFlag = False

button.when_held = open
button.when_released = closed

pause()