# backend/face_utils.py
import face_recognition
import pickle
import numpy as np

with open("backend/data/embeddings.pkl", "rb") as f:
    EMBEDDINGS_DB = pickle.load(f)

def recognize_face(frame, threshold=0.6):
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    results = []
    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        best_match = None
        best_distance = 1.0

        for urn, data in EMBEDDINGS_DB.items():
            known_encoding = data["embedding"]
            distance = np.linalg.norm(face_encoding - known_encoding)

            if distance < best_distance:
                best_distance = distance
                best_match = (urn, data)

        if best_match and best_distance <= threshold:
            results.append({
                "urn": best_match[0],
                "details": best_match[1]["details"],
                "bbox": (top, right, bottom, left),
                "distance": float(best_distance)
            })

    return results
