# backend/face_utils.py
import face_recognition
import pickle
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

# Load embeddings database
# Try multiple path options
EMBEDDINGS_PATH = os.getenv("EMBEDDINGS_PATH", None)
if not EMBEDDINGS_PATH:
    # Try relative paths
    possible_paths = [
        "Backend/Data/embeddings.pkl",
        "Data/embeddings.pkl",
        "./Data/embeddings.pkl",
        os.path.join(os.path.dirname(__file__), "Data/embeddings.pkl")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            EMBEDDINGS_PATH = path
            break
    if not EMBEDDINGS_PATH:
        EMBEDDINGS_PATH = "Backend/Data/embeddings.pkl"

EMBEDDINGS_DB = {}

try:
    if os.path.exists(EMBEDDINGS_PATH):
        try:
            with open(EMBEDDINGS_PATH, "rb") as f:
                EMBEDDINGS_DB = pickle.load(f)
        except ModuleNotFoundError as mnf:
            # Handle numpy internal module name changes in some environments
            msg = str(mnf)
            if "numpy._core" in msg or "numpy._multiarray_umath" in msg:
                import importlib, sys
                try:
                    sys.modules.setdefault("numpy._core", importlib.import_module("numpy.core"))
                except Exception:
                    # fallback: try to ensure numpy is imported
                    try:
                        import numpy as _np  # noqa: F401
                    except Exception:
                        pass
                # Retry loading after mapping
                with open(EMBEDDINGS_PATH, "rb") as f:
                    EMBEDDINGS_DB = pickle.load(f)
            else:
                raise

        logger.info(f"Loaded {len(EMBEDDINGS_DB)} embeddings from {EMBEDDINGS_PATH}")
    else:
        logger.warning(f"Embeddings file not found at {EMBEDDINGS_PATH}. System will run without face recognition until embeddings are generated.")
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
