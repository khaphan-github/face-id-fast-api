from fastapi import File, UploadFile
from pre_processing.cv2_img_reader import cv2_img_reader
from detector.face_detector import face_detector_embedding
from infrastructure.vector_store_persistents import *
from infrastructure.object_store_persistents import *
from utils.res import Response
import uuid


async def register_fid(file: UploadFile = File(...), renew=False, metadata: str = None):
    '''
    Register a new user by uploading an image file.
    - file: image file
    - renew: if True, renew the user's embedding
    - metadata (optional): user's metadata

    '''
    try:
        image = await cv2_img_reader(file)
        embedding = await face_detector_embedding(image)
        if embedding is None:
            return Response(400, None, "No face detected - try again please").to_dict()

        search_result = search_face_embedding(embedding[0], top_k=5)

        if len(search_result) > 0:
            return Response(409, search_result, f'User already exist').to_dict()

        obj_name = 'register-fid' + '-' + str(uuid.uuid4()) + '.webp'

        url = save_file_with_preprocess(
            object_name=obj_name,
            file=file,
            format='webp'
        )
        insert_result = await insert_face_embedding(metadata, embedding[0], url)
        obj_res = {
            'id': insert_result,
            'obj_storage_path': url,
            'metadata': metadata
        }
        return Response(200, obj_res, "Success").to_dict()

    except Exception as e:
        return Response(500, None, str(e)).to_dict()
