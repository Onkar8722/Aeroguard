from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from camera_manager import CameraStream
from face_utils import recognize_face

app = FastAPI()

# ✅ Enable CORS for frontend (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Cameras (add more if needed)
CAMERAS = {
    "cam1": CameraStream(0, "cam1"),   # default webcam
    # "cam2": CameraStream("rtsp://...", "cam2"),
    # "cam3": CameraStream("backend/data/camera1.mp4", "cam3")
}

@app.get("/")
def root():
    return {"message": "Airport Surveillance Backend is running"}

@app.get("/cameras")
def list_cameras():
    return {"cameras": list(CAMERAS.keys())}

@app.get("/stream/{cam_id}")
def stream_camera(cam_id: str):
    camera = CAMERAS.get(cam_id)
    if not camera:
        return JSONResponse({"error": "Camera not found"}, status_code=404)

    def generate():
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            detections = recognize_face(frame)
            for det in detections:
                top, right, bottom, left = det["bbox"]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            _, jpeg = cv2.imencode(".jpg", frame)
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
                   jpeg.tobytes() + b"\r\n")

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.post("/upload_suspicious")
async def upload_suspicious(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detections = recognize_face(img)
    return {"matches": detections}
# This FastAPI backend serves camera streams and processes uploaded images for face recognition.