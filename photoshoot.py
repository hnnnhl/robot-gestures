from picamera2 import Picamera2, Preview
import time
import uuid

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)


for i in range(5): # Update range to number of pictures desired per run
    image_path = "IMAGE/PATH/"+str(uuid.uuid4()) + ".jpg"
    picam2.capture_file(image_path)
    time.sleep(1)