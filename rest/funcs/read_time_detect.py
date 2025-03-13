from infrastructure.zmq_detector import send_base64_image

def read_time_detect(base64_img):
    if "," in base64_img:
        base64_img = base64_img.split(",")[1]
    res = send_base64_image(base64_img)
    return res
