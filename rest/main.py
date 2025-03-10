from fastapi import FastAPI, File, UploadFile
from pre_processing.cv2_img_reader import cv2_img_reader
from detector.face_detector import face_detector_embedding, face_verify_embedding
from infrastructure.persistents import *
from utils.res import Response

app = FastAPI(
    version="12.1.0",
    title="Face Recognition API",
    description="Face recognition API using Milvus and DeepFace",
    openapi_prefix='/api/v1',
    docs_url="/",
)


@app.post("/fid-register")
async def register(file: UploadFile = File(...), renew=False, metadata: str = None):
    '''
    Register a new user by uploading an image file.
    - file: image file
    - renew: if True, renew the user's embedding
    - metadata (optional): user's metadata

    '''
    try:
        image = await cv2_img_reader(file)
        embedding = await face_detector_embedding(image)

        search_result = search_face_embedding(embedding[0], top_k=3)
        if len(search_result) > 0:
            return Response(409, None, f'User already registered: {search_result}').to_dict()

        insert_result = insert_face_embedding(metadata, embedding[0])
        return Response(200, insert_result, "User registered").to_dict()

    except Exception as e:
        return Response(500, None, str(e)).to_dict()


@app.post("/fid-verify")
async def login(file: UploadFile = File(...)):
    '''
    Login by uploading an image file.
    - file: image file
    '''
    try:
        image = await cv2_img_reader(file)
        embedding = await face_detector_embedding(image)

        search_result = search_face_embedding(embedding[0], top_k=1, pick=[
                                              '_id', 'metadata', 'embedding'])
        if len(search_result) == 0:
            return Response(401, None, "User not found").to_dict()

        embedding_lst = [res['embedding'] for res in search_result]
        verify_result = await face_verify_embedding(embedding[0], embedding_lst)

        if not verify_result[0]:
            return Response(401, None, "User not verified").to_dict()

        return Response(200, search_result[0]['metadata'], 'Login success - user checked').to_dict()

    except Exception as e:
        return Response(500, None, str(e)).to_dict()


@app.delete("/fid-remove")
async def remove_face_id(face_id: str):
    try:
        delete_face_embedding(face_id)
        return Response(200, None, f"fid {face_id} removed").to_dict()
    except Exception as e:
        return Response(500, None, str(e)).to_dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
