
import json
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# Connect to Qdrant
client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "sculptures"

# Load embeddings
data = np.load("backend/embeddings.npz")
embeddings = data["embeddings"]
object_ids = data["object_ids"]

# Load sculpture metadata
with open("backend/sculptures.json", "r", encoding="utf-8") as file:
    sculptures = json.load(file)

# Create a metadata lookup using object ID
metadata_lookup = {
    int(item["object_id"]): item for item in sculptures
}

points = []

for index, embedding in enumerate(embeddings):

    object_id = int(object_ids[index])
    metadata = metadata_lookup.get(object_id)

    if metadata is None:
        continue

    point = PointStruct(
        id=object_id,
        vector=embedding.tolist(),
        payload={
            "object_id": object_id,
            "title": metadata["title"],
            "artist": metadata["artist"],
            "classification": metadata["classification"],
            "medium": metadata["medium"],
            "date": metadata["date"],
            "image_url": metadata["image_url"]
        }
    )

    points.append(point)

# Upload vectors
client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print("Vectors uploaded successfully!")
print("Total vectors uploaded:", len(points))

# Verify collection
info = client.get_collection(COLLECTION_NAME)

print("Vectors stored in Qdrant:", info.points_count)
