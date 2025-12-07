# backend/face_utils.py
import face_recognition
import pickle
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

# Load embeddings database
EMBEDDINGS_PATH = os.getenv("EMBEDDINGS_PATH", "Backend/Data/embeddings.pkl")
EMBEDDINGS_DB = {}

try:
    if os.path.exists(EMBEDDINGS_PATH):
        with open(EMBEDDINGS_PATH, "rb") as f:
            EMBEDDINGS_DB = pickle.load(f)
        logger.info(f"Loaded {len(EMBEDDINGS_DB)} embeddings from {EMBEDDINGS_PATH}")
    else:
        logger.warning(f"Embeddings file not found at {EMBEDDINGS_PATH}")
except Exception as e:
    logger.error(f"Error loading embeddings: {str(e)}")

def recognize_face(frame, threshold=0.6):
    try:
        if frame is None:
            logger.warning("Received None frame for recognition")
            return []
        
        if len(EMBEDDINGS_DB) == 0:
            logger.debug("Embeddings database is empty")
            return []
        
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        results = []
        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            best_match = None
            best_distance = 1.0

            for urn, data in EMBEDDINGS_DB.items():
                try:
                    known_encoding = data["embedding"]
                    distance = np.linalg.norm(face_encoding - known_encoding)

                    if distance < best_distance:
                        best_distance = distance
                        best_match = (urn, data)
                except Exception as e:
                    logger.error(f"Error processing embedding for {urn}: {str(e)}")
                    continue

            if best_match and best_distance <= threshold:
                results.append({
                    "urn": best_match[0],
                    "details": best_match[1]["details"],
                    "bbox": (top, right, bottom, left),
                    "distance": float(best_distance)
                })

        return results
    except Exception as e:
        logger.error(f"Error in recognize_face: {str(e)}")
        return []
