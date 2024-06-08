# Gesture Detection with Roboflow
This project uses a local Roboflow Inference server to detect hand gestures to trigger movement in a robot. The robot moves if it detects two palms. It stops if it does not detect two palms.

## Hardware
- Rasberry Pi 4 Model B - 8GB RAM
- [Freenove Hexapod Robot Kit](https://github.com/Freenove/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi)

## Setup

### Computer Vision Model
- This project uses this model of my hands: https://universe.roboflow.com/workspace-bdfjh/robot-gesture
- If you want to train your own model, you can run [photoshoot.py](https://github.com/hnnnhl/robot-gestures/blob/master/photoshoot.py) to take pictures from your robot.
  - Update Roboflow variables [here](https://github.com/hnnnhl/robot-gestures/blob/0287ce8a19fadd2d64727404ff7f869b5a7e3b47/palm_detection.py#L9) for your new project.
    
### Robot 
- Follow Freenove instructions to setup the robot ([docs](https://github.com/Freenove/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi/blob/master/Tutorial.pdf))
  - The robot files in this repo were taken directly from Freenove's repository [here](https://github.com/Freenove/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi/tree/master/Code/Server).
  Look for the latest updates for these files there:
    - Command.py
    - Control.py
    - IMU.py
    - Kalman.py
    - PCA9685.py
    - PID.py
    - Servo.py
    - point.txt
- Setup Rasbperry Pi OS Bookworm ([docs](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system))
- Pull down this repo on the Raspberry Pi.
  - Install global packages:
    - `sudo apt install -y python3-picamera2 python3-libcamera`
    - `curl -fsSL https://get.docker.com -o get-docker.sh`
    - `sudo sh get-docker.sh`
  - In the project directory:
    - Setup the virtual environment:
      - `python3 -m venv --system-site-packages venv`
        - *** `--system-site-packages` gives your venv access to `libcamera`. This will not work without it.  
      - `source venv/bin/activate`
      - `pip install -r requirements.txt`
     
## Run
- Start the local inference server:
  - `sudo docker run -it --rm -p 9001:9001 roboflow/roboflow-inference-server-arm-cpu`
- In this project directory, ensure the virtual environment is activated:
  - `source venv/bin/activate`
- Run the robot:
  - `python palm_detection.py`
- Put your palms out and see if it works. There will be some lag. The print statements will tell you if there is delay in fetching the
inference return, or if the object detection just isn't working.

## Performance Improvements
- This could be a good candidate for a Raspberry Pi cluster. This could be split up into several nodes, e.g.:
  - Inference server node
  - Camera controller node
  - Robot controller node
- Some of the lag may be due to the camera needing to write the image to the disk so that the image path can be passed to Roboflow's `predict()`
function ([example](https://github.com/hnnnhl/robot-gestures/blob/0287ce8a19fadd2d64727404ff7f869b5a7e3b47/palm_detection.py#L59)). Performance may
be improved if a binary stream (e.g. with `io.BytesIO()`) could be passed to Roboflow, instead of an image path, so that the image could be serialized
in-memory instead of needing to be written to the disk.
