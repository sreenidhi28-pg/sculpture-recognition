
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Connect to local Qdrant
client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "sculptures"

# Create collection if it doesn't already exist
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=512,
            distance=Distance.COSINE
        )
    )
    print("Sculptures collection created successfully!")
else:
    print("Sculptures collection already exists!")

# Display collection information
info = client.get_collection(COLLECTION_NAME)

print("Collection name:", COLLECTION_NAME)
print("Vector size:", info.config.params.vectors.size)
print("Distance:", info.config.params.vectors.distance)
