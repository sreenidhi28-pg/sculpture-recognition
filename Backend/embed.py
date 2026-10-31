import json
import numpy as np
from pathlib import Path

from model import generate_embedding

# Project paths
DATASET_PATH = Path("backend/dataset")
METADATA_PATH = Path("backend/sculptures.json")
OUTPUT_PATH = Path("backend/embeddings.npz")

# Load sculpture metadata
with open(METADATA_PATH, "r", encoding="utf-8") as file:
    sculptures = json.load(file)

embeddings = []
object_ids = []

print("Generating sculpture embeddings...\n")

for sculpture in sculptures:

    object_id = sculpture["object_id"]
    image_path = DATASET_PATH / f"{object_id}.jpg"

    if not image_path.exists():
        print("Image not found:", object_id)
        continue

    try:
        embedding = generate_embedding(str(image_path))

        embeddings.append(embedding)
        object_ids.append(object_id)

        print("Embedding generated:", sculpture["title"])

    except Exception as error:
        print("Failed:", object_id, error)

# Save embeddings
if embeddings:
    np.savez_compressed(
        OUTPUT_PATH,
        embeddings=np.array(embeddings),
        object_ids=np.array(object_ids)
    )

    print("\nTotal embeddings:", len(embeddings))
    print("Embedding dimensions:", embeddings[0].shape)
    print("Saved to:", OUTPUT_PATH)
else:
    print("No embeddings were generated.")