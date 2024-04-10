from picamera2 import Picamera2, Preview
from libcamera import controls
camera = Picamera2()
mode = camera.sensor_modes[1]
config = camera.create_preview_configuration(
            sensor={'output_size': mode['size'], 'bit_depth':mode['bit_depth']},
            raw={"size": (1500, 1000)}
            )

camera.configure(config)
camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
camera.set_controls({"FrameRate": 30})
camera.start(show_preview=True)

while True:
    pass