import threading
from Control import *
import os
import json
from roboflow import Roboflow
from picamera2 import Picamera2, Preview
import time

ROBOFLOW_API_KEY="aBfIRAFiL2x92BabVixf"
ROBOFLOW_API_VERSION=1
ROBOFLOW_WORKSPACE="workspace-bdfjh"
ROBOFLOW_PROJECT="robot-gesture"

class Robot:
    def __init__(self):
        self.c = Control()
        self.picam2 = None
        self.rf = None
        self.project = None
        self.model = None
        self.t = None
        self.stop_event = threading.Event()

    def init_picamera(self):
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_preview_configuration()
        self.picam2.configure(camera_config)
        self.picam2.start_preview(Preview.QTGL)
        self.picam2.start()
        print('Picamera initialized')

    def init_servos(self):
        for i in [1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 15, 17, 20]:
            self.c.position(0, 0, i)
        print('Servos initialized')

    def move_forward(self):
        while not self.stop_event.is_set():
            print('Moving forward')
            data=['CMD_MOVE', '1', '0', '35', '10', '0']
            self.c.run(data)

    def init_roboflow(self):
        self.rf = Roboflow(api_key=ROBOFLOW_API_KEY)
        self.project = self.rf.workspace(ROBOFLOW_WORKSPACE).project(ROBOFLOW_PROJECT)
        self.model = self.project.version(ROBOFLOW_API_VERSION, local="http://localhost:9001/").model
        print('Connected to Roboflow')

    def run(self):
        self.init_picamera()
        self.init_servos()
        self.init_roboflow()

        while True:
            print('Taking picture')
            image_path = "temp.jpg"
            self.picam2.capture_file(image_path)
            print('Getting predictions')
            result = self.model.predict(image_path, confidence=70, overlap=30)
            predictions = result.json()['predictions']
            print('Got predictions')

            count = 0

            for prediction in predictions:
                if prediction['class'].lower() == 'palm':
                    count += 1

            if count == 2: # Robot only moves if 2 palms are detected
                if self.t is None or not self.t.is_alive():
                    self.t = threading.Thread(target=self.move_forward)
                    self.t.start()
            else:
                print('Stopping')
                self.stop_event.set()
                if self.t is not None and self.t.is_alive():
                    self.t.join()
                self.stop_event.clear()


robot = Robot()
robot.run()
