import zmq
import cv2
import numpy as np
import base64

# ZeroMQ setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")  # Ensure server is running
print('Connected to server detector socket')
def send_base64_image(base64_str):
    """ Sends a Base64 encoded image to the C++ server for face detection """
    
    # Decode Base64 string to bytes
    image_data = base64.b64decode(base64_str)

    # Convert bytes to NumPy array
    np_arr = np.frombuffer(image_data, np.uint8)

    # Decode image from array
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if frame is None:
        print("Error: Decoded image is empty")
        return
    
    # Encode the image as JPEG before sending
    _, buffer = cv2.imencode('.jpg', frame)
    
    # Send image data to C++ server
    socket.send(buffer.tobytes())

    # Receive response from server
    return socket.recv().decode()

