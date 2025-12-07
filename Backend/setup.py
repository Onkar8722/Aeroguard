# backend/setup.py
import os
import pickle
import face_recognition
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = os.getenv("DATA_DIR", "Backend/Data/Images")
PROFILE_FILE = os.getenv("PROFILE_FILE", "Backend/Data/profile.xlsx")
EMBEDDINGS_FILE = os.getenv("EMBEDDINGS_FILE", "Backend/Data/embeddings.pkl")

def generate_embeddings():
    try:
        logger.info(f"Loading profiles from {PROFILE_FILE}")
        profile_df = pd.read_excel(PROFILE_FILE)
        embeddings = {}
        success_count = 0
        error_count = 0

        for _, row in profile_df.iterrows():
            try:
                img_path = os.path.join(DATA_DIR, row["Image Address"])
                urn = row["URN"]

                if not os.path.exists(img_path):
                    logger.warning(f"Image not found for URN={urn}: {img_path}")
                    error_count += 1
                    continue

                image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(image)

                if len(encodings) == 0:
                    logger.warning(f"No face detected for URN={urn}: {img_path}")
                    error_count += 1
                    continue

                embeddings[urn] = {
                    "embedding": encodings[0],
                    "details": row.to_dict()
                }
                success_count += 1
                logger.info(f"Processed {img_path}")
            except Exception as e:
                logger.error(f"Error processing row {urn}: {str(e)}")
                error_count += 1
                continue

        os.makedirs(os.path.dirname(EMBEDDINGS_FILE), exist_ok=True)
        with open(EMBEDDINGS_FILE, "wb") as f:
            pickle.dump(embeddings, f)

        logger.info(f"Saved {success_count} embeddings to {EMBEDDINGS_FILE} ({error_count} errors)")
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")

if __name__ == "__main__":
    generate_embeddings()
# This script generates facial embeddings from images and saves them along with profile details.