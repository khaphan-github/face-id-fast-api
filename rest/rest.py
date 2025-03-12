from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from utils.html_client_socket import HTML_CLIENT_SOCKET
from funcs.register_fid import register_fid
from funcs.verify_fid import verify_fid
from funcs.remove_fid import remove_fid
from funcs.health_check import health_check
from funcs.read_time_detect import read_time_detect

app = FastAPI(
    version="12.1.0",
    title="Face Recognition API",
    description="Face recognition API using Milvus and DeepFace",
    docs_url="/",
)


@app.get("/mock-client")
async def get():
    return HTMLResponse(HTML_CLIENT_SOCKET)


@app.get("/api/v1/health")
async def health():
    return await health_check()


@app.post("/api/v1/fid-register")
async def register(file: UploadFile = File(...), renew: bool = False, metadata: str = None):
    return await register_fid(file, renew, metadata)


@app.post("/api/v1/fid-verify")
async def verify(file: UploadFile = File(...)):
    return await verify_fid(file)


@app.delete("/api/v2/fid-remove")
async def remove_face_id(face_id: str):
    return await remove_fid(face_id)


@app.delete("/api/v1/fid-remove")
async def remove_face_id(face_id: str):
    return await remove_fid(face_id)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    '''
        TODO: Implement message broker
    '''
    await websocket.accept()
    while True:
        data = await websocket.receive_text()  # base64 image
        verify = await read_time_detect(data)
        await websocket.send_json({"verify": verify})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
