import zmq
from conf.env import ZMQ_FACE_DETECTION_ENDPOINT


# ZeroMQ setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(ZMQ_FACE_DETECTION_ENDPOINT)  # Ensure server is running
print('[ZMQ] Connected to server detector socket...')

def send_base64_image(buffer):
    """ Sends a Base64 encoded image to the C++ server for face detection """
    socket.send(buffer.tobytes())
    return socket.recv().decode()
