from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Enable CORS
CORS(app, origins=os.getenv("CORS_ORIGINS", "http://localhost:5000").split(","))

# Lazy import face_utils and camera to avoid startup issues
def get_face_utils():
    global face_utils_module
    if 'face_utils_module' not in globals():
        try:
            from face_utils import recognize_face
            face_utils_module = recognize_face
        except Exception as e:
            logger.error(f"Could not load face_utils: {e}")
            face_utils_module = None
    return face_utils_module

def get_cameras():
    global CAMERAS_DICT
    if 'CAMERAS_DICT' not in globals():
        CAMERAS_DICT = {}
        try:
            from camera_manager import CameraStream
            cam1 = CameraStream(0, "cam1")
            CAMERAS_DICT["cam1"] = cam1
            logger.info("Webcam initialized")
        except Exception as e:
            logger.warning(f"Could not initialize camera: {e}")
    return CAMERAS_DICT


# ============ ROUTES ============

@app.route('/')
def index():
    """Serve main dashboard"""
    return render_template('index.html')


@app.route('/api/health')
def health():
    """Health check endpoint"""
    logger.info("Health check request received")
    return jsonify({"status": "running", "message": "Airport Surveillance Backend"})


@app.route('/api/cameras')
def list_cameras():
    """List all available cameras"""
    try:
        cameras_dict = get_cameras()
        logger.info(f"Listing {len(cameras_dict)} cameras")
        return jsonify({"cameras": list(cameras_dict.keys()), "total": len(cameras_dict)})
    except Exception as e:
        logger.error(f"Error listing cameras: {str(e)}")
        return jsonify({"cameras": [], "error": str(e)}), 500


@app.route('/api/stream/<cam_id>')
def stream_camera(cam_id):
    """Stream live video from camera"""
    try:
        cameras_dict = get_cameras()
        camera = cameras_dict.get(cam_id)
        if not camera:
            logger.warning(f"Camera not found: {cam_id}")
            return jsonify({"error": "Camera not found"}), 404

        recognize_face = get_face_utils()
        logger.info(f"Starting stream for camera: {cam_id}")
        
        def generate_frames():
            error_count = 0
            while True:
                try:
                    frame = camera.get_frame()
                    if frame is None:
                        continue

                    # Detect faces and draw boxes
                    detections = recognize_face(frame) if recognize_face else []
                    for det in detections:
                        top, right, bottom, left = det["bbox"]
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        # Draw detection info
                        confidence = int((1 - det["distance"]) * 100)
                        cv2.putText(frame, f"{confidence}%", (left, top - 10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Encode frame to JPEG
                    _, jpeg = cv2.imencode(".jpg", frame)
                    yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
                           jpeg.tobytes() + b"\r\n")
                    error_count = 0
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error in stream generation: {str(e)}")
                    if error_count > 10:
                        break

        return generate_frames(), 200, {
            'Content-Type': 'multipart/x-mixed-replace; boundary=frame',
            'Cache-Control': 'no-cache, no-store, must-revalidate'
        }
    except Exception as e:
        logger.error(f"Error starting stream: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/upload_suspicious', methods=['POST'])
def upload_suspicious():
    """Upload image to match against database"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        logger.info(f"Processing upload: {file.filename}")
        
        # Read file into numpy array
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            logger.error(f"Invalid image file: {file.filename}")
            return jsonify({"error": "Invalid image format"}), 400

        # Recognize faces in image
        recognize_face = get_face_utils()
        if recognize_face is None:
            return jsonify({"error": "Face recognition not available", "matches": []}), 503
            
        detections = recognize_face(img)
        logger.info(f"Found {len(detections)} matches for {file.filename}")
        
        return jsonify({
            "matches": detections,
            "count": len(detections)
        })
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        return jsonify({"error": str(e), "matches": []}), 500


@app.route('/api/status')
def get_status():
    """Get system status"""
    try:
        cameras_dict = get_cameras()
        return jsonify({
            "active_cameras": len(cameras_dict),
            "system_status": "running",
            "embeddings_loaded": True,
            "timestamp": str(__import__('datetime').datetime.now())
        })
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host='127.0.0.1', port=port, debug=debug)