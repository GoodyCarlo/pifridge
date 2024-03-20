"""
Python 3/PyQt5 + picamera2 to control Raspberry Pi Camera Modules
Tested on Raspberry Pi 5/64-bit Raspberry Pi OS (bookworm)
# in my setup:
# Picamera2(0) - HQ Camera
# Picamera2(1) - Camera Module 3
"""
import sys, platform, os
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QWidget, QTabWidget, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

from PyQt5.QtGui import QPalette, QColor, QFont

from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2
from picamera2 import __name__ as picamera2_name
from libcamera import controls

import time
from importlib.metadata import version

os.environ["LIBCAMERA_LOG_LEVELS"] = "3"

picam2 = Picamera2(1)

#=====================================
preview_width= 800
preview_height = int(picam2.sensor_resolution[1] * preview_width/picam2.sensor_resolution[0])
preview_config_raw = picam2.create_preview_configuration(main={"size": (preview_width, preview_height)},
                                                         raw={"size": picam2.sensor_resolution})
picam2.configure(preview_config_raw)
#=====================================
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#=====================================

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = __file__
        self.left = 0
        self.top = 0
        self.setWindowTitle(self.title)

        self.main_widget = MyMainWidget(self)
        self.setCentralWidget(self.main_widget)
        
        self.show()

class MyMainWidget(QWidget):
    
    def read_f(self, file):
        with open(file, encoding='UTF-8') as reader:
            content = reader.read()
        return content
    
    def read_pretty_name(self):
        with open("/etc/os-release") as f:
            os_release = {}
            for line in f:
                k,v = line.rstrip().split("=")
                os_release[k] = v.strip('"')
        return os_release['PRETTY_NAME']
                
    def on_Capture_Clicked(self):
        global picam2
        self.btnCapture.setEnabled(False)
        
        cfg = picam2.create_still_configuration()
        
        timeStamp = time.strftime("%Y%m%d-%H%M%S")
        targetPath="/home/pi/Desktop/img_"+timeStamp+".jpg"
        print("- Capture image:", targetPath)
        
        picam2.switch_mode_and_capture_file(cfg, targetPath,signal_function=self.qpicamera2.signal_done)

    def capture_done(self, job):
        global picam2
        result = picam2.wait(job)
        self.btnCapture.setEnabled(True)
        print("- capture_done.")
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabCapture = QWidget()
        self.tabInfo = QWidget()

        # Add tabs
        self.tabs.addTab(self.tabCapture,"Capture")
        self.tabs.addTab(self.tabInfo,"  Info  ")
        
        #=== Tab Capture ===
        # Create first tab
        self.tabCapture.layout = QVBoxLayout()
        
        self.tabCapture.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('black'))
        self.tabCapture.setPalette(palette)
        
        #Prepare Preview
        self.qpicamera2 = QGlPicamera2(picam2,
                          width=preview_width, height=preview_height,
                          keep_ar=True)

        self.tabCapture.layout.addWidget(self.qpicamera2)
        self.qpicamera2.done_signal.connect(self.capture_done)

        self.btnCapture = QPushButton("Capture Image")
        self.btnCapture.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.btnCapture.clicked.connect(self.on_Capture_Clicked)
        
        self.tabCapture.layout.addWidget(self.btnCapture)
        #self.tabCapture.layout.addStretch()
        
        self.tabCapture.setLayout(self.tabCapture.layout)
        
        #=== Tab Info ===
        self.tabInfo.layout = QVBoxLayout()
        
        infoGridLayout = QGridLayout()
        
        rowSpan = 1
        columnSpan0 = 1
        columnSpan1 = 5
        infoGridLayout.addWidget(QLabel('Python', self), 0, 0, rowSpan, columnSpan0)
        infoGridLayout.addWidget(QLabel(platform.python_version(), self), 0, 1, rowSpan, columnSpan1)
        
        infoGridLayout.addWidget(QLabel(picamera2_name, self), 1, 0, rowSpan, columnSpan0)
        infoGridLayout.addWidget(QLabel(version(picamera2_name), self), 1, 1, rowSpan, columnSpan1)
        
        infoGridLayout.addWidget(QLabel(' ', self), 2, 0, rowSpan, columnSpan0)        
        infoGridLayout.addWidget(QLabel('Camera Module:', self), 3, 0, rowSpan, columnSpan0)
        
        cam_properties = picam2.camera_properties
        cam_Model = cam_properties['Model']
        infoGridLayout.addWidget(QLabel('Model', self), 4, 0, rowSpan, columnSpan0)
        infoGridLayout.addWidget(QLabel(cam_Model, self), 4, 1, rowSpan, columnSpan1)
        cam_PixelArraySize = str(cam_properties['PixelArraySize'][0]) + " x " + str(cam_properties['PixelArraySize'][1])
        infoGridLayout.addWidget(QLabel('PixelArraySize', self), 5, 0, rowSpan, columnSpan0)
        infoGridLayout.addWidget(QLabel(cam_PixelArraySize, self), 5, 1, rowSpan, columnSpan1)
        
        infoGridLayout.addWidget(QLabel(' ', self), 6, 0, rowSpan, columnSpan0)
        infoGridLayout.addWidget(QLabel('Machine:', self), 7, 0, rowSpan, columnSpan0)
        infoGridLayout.addWidget(QLabel('Board', self), 8, 0, rowSpan, columnSpan0, Qt.AlignTop)
        board_def = "/proc/device-tree/model"
        board_info = self.read_f("/proc/device-tree/model") +"\n(" + board_def +")"
        infoGridLayout.addWidget(QLabel(board_info, self), 8, 1, rowSpan, columnSpan0)
        
        infoGridLayout.addWidget(QLabel('OS', self), 9, 0, rowSpan, columnSpan0, Qt.AlignTop)
        os_info = self.read_pretty_name() + "\n" + os.uname()[3]
        infoGridLayout.addWidget(QLabel(os_info, self), 9, 1, rowSpan, columnSpan1)
        
        self.tabInfo.layout.addLayout(infoGridLayout)
        self.tabInfo.layout.addStretch()
        
        self.tabInfo.setLayout(self.tabInfo.layout)
        
        #==================================
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        picam2.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())