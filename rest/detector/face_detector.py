from deepface import DeepFace
import asyncio


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
