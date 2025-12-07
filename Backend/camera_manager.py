# backend/camera_manager.py
import cv2
import threading

class CameraStream:
    def __init__(self, src, cam_id):
        self.stream = cv2.VideoCapture(src)
        self.cam_id = cam_id
        self.frame = None
        self.running = True
        thread = threading.Thread(target=self.update, daemon=True)
        thread.start()

    def update(self):
        while self.running:
            ret, frame = self.stream.read()
            if ret:
                self.frame = frame

    def get_frame(self):
        return self.frame

    def stop(self):
        self.running = False
        self.stream.release()
