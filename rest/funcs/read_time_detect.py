from detector.face_detector import face_detector_match_screen_size

async def read_time_detect(base64_img):
  res = await face_detector_match_screen_size(base64_img)
  return res