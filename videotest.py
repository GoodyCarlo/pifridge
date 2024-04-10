from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from libcamera import controls
import time
camera = Picamera2()
mode = camera.sensor_modes[1]
config = camera.create_preview_configuration(
            sensor={'output_size': mode['size'], 'bit_depth':mode['bit_depth']},
            raw={"size": (640, 480)}
            )

camera.configure(config)
camera.set_controls({"AfMode": controls.AfModeEnum.Manual})
camera.set_controls({"LensPosition" : 1.0})
camera.set_controls({"FrameRate": 60})

encoder = H264Encoder(10000000000)

camera.start(show_preview=True)
# camera.start_recording(encoder, f"10secondvideo.h264")
while True:
    pass