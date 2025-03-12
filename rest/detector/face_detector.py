from deepface import DeepFace
import asyncio
import cv2
import base64
import numpy as np


async def face_detector_embedding(image):
    result = await asyncio.to_thread(
        DeepFace.represent,
        img_path=image,
        model_name="Facenet",
    )
    embeddings = [res["embedding"] for res in result]
    return embeddings


async def face_verify_embedding(user_embedding, stored_embeddings):
    tasks = [
        asyncio.to_thread(
            DeepFace.verify,
            user_embedding,
            stored_embedding,
            model_name="Facenet",
        )
        for stored_embedding in stored_embeddings
    ]
    results = await asyncio.gather(*tasks)
    return [result["verified"] for result in results]


async def face_detector(base64_img):
    try:
        if "," in base64_img:
            base64_img = base64_img.split(",")[1]
        img_data = base64.b64decode(base64_img)

        np_arr = np.frombuffer(img_data, np.uint8)

        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError(
                "Failed to decode image: Invalid or corrupted image data")

        # Load the face cascade classifier
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if face_cascade.empty():
            raise ValueError("Failed to load face cascade classifier")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = await asyncio.to_thread(face_cascade.detectMultiScale, gray, scaleFactor=1.1, minNeighbors=4)

        return faces, img

    except Exception as e:
        print(f"Error during face detection: {e}")
        return []
      
async def face_detector_match_screen_size(image):
  '''
  From detected face if this face is not center screen then return False
  Only return true if it center screen
  '''
  faces, img = await face_detector(image)
  if len(faces) == 0:
    return False

  img_height, img_width, _ = img.shape
  for (x, y, w, h) in faces:
    face_center_x = x + w / 2
    face_center_y = y + h / 2

    screen_center_x = img_width / 2
    screen_center_y = img_height / 2

    if abs(face_center_x - screen_center_x) <= img_width * 0.1 and abs(face_center_y - screen_center_y) <= img_height * 0.1:
      return True

  return False