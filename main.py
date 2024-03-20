from gpiozero import Button
from signal import pause
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from libcamera import controls
import os
class CameraControls:
    def __init__(self):
        self.camera = Picamera2()
        self.mode = self.camera.sensor_modes[0]
        self.config = self.camera.create_preview_configuration(
            sensor={'output_size': self.mode['size'], 'bit_depth':self.mode['bit_depth']},
            raw={'fps':30, 'size':(640,640)})

        self.camera.configure(self.config)
        self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

        self.encoder = H264Encoder(10000000000)
        self.camera.start_preview(Preview.QTGL)
        self.camera.stop_preview()

    def stop_recording(self):
        self.camera.stop_recording()

    def start_recording(self):
        print("started")
        is_dir = os.path.isdir(f'jobs/job_0')
        count = 0
        while is_dir:
            count += 1
            is_dir = os.path.isdir(f'jobs/job_{count}')
        output = f'jobs/job_{count}'
        os.mkdir(output)
        print("output")
        self.camera.start_recording(self.encoder, f"{output}/video.h264")

    def start_preview(self):
        self.camera.start_preview(Preview.QTGL)

    def stop_preview(self):
        self.camera.stop_preview()

button = Button(26)
button.hold_time = .1
closedFlag = True

camera = CameraControls()

def closed():
    global closedFlag

    if not closedFlag:
        print("closed\n")
        closedFlag = True
        camera.stop_recording()
        camera.stop_preview()


def open(): 
    
    print("open\n")
    
    camera.start_preview()
    camera.start_recording()
    
    global closedFlag
    closedFlag = False

button.when_held = open
button.when_released = closed

pause()