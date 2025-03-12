from fastapi import  File, UploadFile
from pre_processing.cv2_img_reader import cv2_img_reader
from detector.face_detector import face_detector_embedding, face_verify_embedding
from infrastructure.vector_store_persistents import *
from infrastructure.object_store_persistents import *
from utils.res import Response

async def verify_fid(file: UploadFile = File(...)):
    '''
    Login by uploading an image file.
    - file: image file
    '''
    try:
        image = await cv2_img_reader(file)
        embedding = await face_detector_embedding(image)

        search_result = search_face_embedding(embedding[0], top_k=1, pick=[
                                              '_id', 'metadata', 'embedding', 'obj_storage_path'])
        if len(search_result) == 0:
            return Response(401, None, "User not found").to_dict()

        embedding_lst = [res['embedding'] for res in search_result]
        verify_result = await face_verify_embedding(embedding[0], embedding_lst)

        if not verify_result[0]:
            return Response(401, None, "Face not match").to_dict()

        search_result[0].pop('embedding', None)
        return Response(200, search_result[0], 'Success').to_dict()

    except Exception as e:
        return Response(500, None, str(e)).to_dict()
