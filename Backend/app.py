from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import os
import logging
from camera_manager import CameraStream
from face_utils import recognize_face

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for frontend
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    logger.info("Health check request received")
    return {"status": "running", "message": "Airport Surveillance Backend"}

@app.get("/cameras")
def list_cameras():
    try:
        logger.info(f"Listing {len(CAMERAS)} cameras")
        return {"cameras": list(CAMERAS.keys())}
    except Exception as e:
        logger.error(f"Error listing cameras: {str(e)}")
        return JSONResponse({"cameras": [], "error": str(e)}, status_code=500)

@app.get("/stream/{cam_id}")
def stream_camera(cam_id: str):
    try:
        camera = CAMERAS.get(cam_id)
        if not camera:
            logger.warning(f"Camera not found: {cam_id}")
            return JSONResponse({"error": "Camera not found"}, status_code=404)

        logger.info(f"Starting stream for camera: {cam_id}")
        
        def generate():
            error_count = 0
            while True:
                try:
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
                    error_count = 0
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error in stream generation: {str(e)}")
                    if error_count > 10:
                        break

        return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")
    except Exception as e:
        logger.error(f"Error starting stream: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/upload_suspicious")
async def upload_suspicious(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing upload: {file.filename}")
        contents = await file.read()
        if not contents:
            return JSONResponse({"error": "Empty file"}, status_code=400)
        
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            logger.error(f"Invalid image file: {file.filename}")
            return JSONResponse({"error": "Invalid image format"}, status_code=400)

        detections = recognize_face(img)
        logger.info(f"Found {len(detections)} matches for {file.filename}")
        return {"matches": detections}
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        return JSONResponse({"error": str(e), "matches": []}, status_code=500)
# This FastAPI backend serves camera streams and processes uploaded images for face recognition.