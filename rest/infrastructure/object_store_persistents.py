from minio import Minio
from conf.env import MINIO_BUCKET_NAME, MINIO_ENDPOINT, MINIO_SECRET_KEY, MINIO_ACCESS_KEY
from fastapi import File, UploadFile
from PIL import Image
import io
import asyncio
from thread.thread_handler import *

# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Set to True if using HTTPS
)

# Bucket name
BUCKET_NAME = MINIO_BUCKET_NAME

# Ensure the bucket exists
if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)
    print(f"Bucket '{BUCKET_NAME}' created successfully.")
else:
    print(f"Bucket '{BUCKET_NAME}' already exists.")


def create_presigned_url(object_name: str, expiry: int = 3600) -> str:
    """
    Generate a presigned URL for uploading an image to MinIO.

    :param object_name: The name of the object (file) in the MinIO bucket.
    :param expiry: Expiration time in seconds (default: 3600 seconds).
    :return: Presigned URL for uploading.
    """
    try:
        presigned_url = minio_client.presigned_put_object(
            BUCKET_NAME, object_name, expires=expiry)
        return presigned_url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None



def save_file_with_preprocess(object_name: str, file: UploadFile = File(...), format='webp', metadata: dict = None) -> str:
  '''
  Save the uploaded file to MinIO.
  - file: the uploaded file
  - object_name: the name of the object in MinIO
  - format: the format to save the file in (default: 'webp')
  - metadata: optional metadata to include with the file
  '''
  try:
    # Read the uploaded file
    image = Image.open(file.file)
    
    # Convert the image to the specified format
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format)
    img_byte_arr.seek(0)
    
    # Save the file to MinIO
    minio_client.put_object(
      BUCKET_NAME,
      object_name,
      img_byte_arr,
      img_byte_arr.getbuffer().nbytes,
      metadata=metadata
    )
    return f"{BUCKET_NAME}/{object_name}"
  except Exception as e:
    print(f"Error saving file to MinIO: {e}")
    return None
