from infrastructure.vector_store_persistents import *
from infrastructure.object_store_persistents import *
from utils.res import Response

async def remove_fid(face_id: str):
    try:
        delete_face_embedding(face_id)
        return Response(200, None, f"fid {face_id} removed").to_dict()
    except Exception as e:
        return Response(500, None, str(e)).to_dict()
