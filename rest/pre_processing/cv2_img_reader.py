import cv2
import numpy as np

async def cv2_img_reader(file):
  nparr = np.frombuffer(await file.read(), np.uint8)
  image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  return image