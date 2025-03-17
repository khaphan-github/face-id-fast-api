import cv2
import numpy as np
import base64
from infrastructure.zmq_detector import send_base64_image

def read_time_detect(base64_str):
    if "," in base64_img:
        base64_img = base64_img.split(",")[1]
    image_data = base64.b64decode(base64_str)

    np_arr = np.frombuffer(image_data, np.uint8)

    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if frame is None:
        print("Error: Decoded image is empty")
        return
    
    _, buffer = cv2.imencode('.jpg', frame)
    
    res = send_base64_image(buffer)
    return res
