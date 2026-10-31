
import numpy as np
from qdrant_client import QdrantClient

# Connect to Qdrant
client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "sculptures"

# Load saved embeddings
data = np.load("backend/embeddings.npz")
embeddings = data["embeddings"]

# Use the first sculpture as the query image
query_embedding = embeddings[0].tolist()

# Search for similar sculptures
results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_embedding,
    limit=5,
    with_payload=True
).points

print("\n--- TOP 5 SIMILAR SCULPTURES ---")

for rank, result in enumerate(results, start=1):
    print(f"\nRank: {rank}")
    print("Object ID:", result.payload["object_id"])
    print("Title:", result.payload["title"])
    print("Artist:", result.payload["artist"])
    print("Similarity:", round(result.score, 4))
