# backend/camera_manager.py
import cv2
import threading
import logging

logger = logging.getLogger(__name__)

class CameraStream:
    def __init__(self, src, cam_id):
        try:
            self.stream = cv2.VideoCapture(src)
            self.cam_id = cam_id
            self.frame = None
            self.running = True
            if not self.stream.isOpened():
                logger.warning(f"Failed to open camera stream: {src}")
            thread = threading.Thread(target=self.update, daemon=True)
            thread.start()
            logger.info(f"Camera {cam_id} initialized")
        except Exception as e:
            logger.error(f"Error initializing camera {cam_id}: {str(e)}")

    def update(self):
        error_count = 0
        while self.running:
            try:
                ret, frame = self.stream.read()
                if ret:
                    self.frame = frame
                    error_count = 0
                else:
                    error_count += 1
                    if error_count > 10:
                        logger.warning(f"Too many read errors for camera {self.cam_id}")
                        break
            except Exception as e:
                error_count += 1
                logger.error(f"Error reading frame from {self.cam_id}: {str(e)}")
                if error_count > 10:
                    break

    def get_frame(self):
        return self.frame

    def stop(self):
        self.running = False
        self.stream.release()
