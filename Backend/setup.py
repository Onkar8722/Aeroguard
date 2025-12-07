# backend/setup.py
import os
import pickle
import face_recognition
import pandas as pd

DATA_DIR = ""
PROFILE_FILE = "Backend/Data/profile.xlsx"
EMBEDDINGS_FILE = "Backend/Data/embeddings.pkl"

def generate_embeddings():
    profile_df = pd.read_excel(PROFILE_FILE)
    embeddings = {}

    # inside generate_embeddings() loop
    for _, row in profile_df.iterrows():
        img_path = os.path.join(DATA_DIR, row["Image Address"])
        urn = row["URN"]

        if not os.path.exists(img_path):
            print(f"[WARN] Image not found for URN={urn}: {img_path}")
            continue

        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            print(f"[WARN] No face detected in image for URN={urn}: {img_path}")
            continue

        embeddings[urn] = {
            "embedding": encodings[0],
            "details": row.to_dict()
        }
        print(f"[OK] Processed {img_path}")


    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(embeddings, f)

    print(f"[INFO] Saved {len(embeddings)} embeddings to {EMBEDDINGS_FILE}")

if __name__ == "__main__":
    generate_embeddings()
# This script generates facial embeddings from images and saves them along with profile details.