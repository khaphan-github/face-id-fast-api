import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MinIO configuration
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')

# Milvus configuration
MILVUS_HOST = os.getenv('MILVUS_HOST')
MILVUS_PORT = os.getenv('MILVUS_PORT')
MILVUS_COLLECTION_NAME = os.getenv('MILVUS_COLLECTION_NAME')


# Socket conf
SOCKET_ALLOW_ORIGINS = os.getenv('SOCKET_ALLOW_ORIGINS')

ZMQ_FACE_DETECTION_ENDPOINT = os.getenv('ZMQ_FACE_DETECTION_ENDPOINT')
