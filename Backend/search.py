import numpy as np

# Load saved embeddings
data = np.load("backend/embeddings.npz")

embeddings = data["embeddings"]
object_ids = data["object_ids"]


def find_similar(query_embedding, query_id, top_k=5):
    # Calculate cosine similarity
    scores = embeddings @ query_embedding

    # Sort from highest similarity to lowest
    ranked_indices = np.argsort(scores)[::-1]

    results = []

    for index in ranked_indices:
        object_id = int(object_ids[index])

        # Skip the query image itself
        if object_id == query_id:
            continue

        results.append({
            "object_id": object_id,
            "similarity": float(scores[index])
        })

        if len(results) == top_k:
            break

    return results


# Select the first sculpture as the query image
query_embedding = embeddings[0]
query_id = int(object_ids[0])

results = find_similar(query_embedding, query_id)

print("\n--- TOP SIMILAR SCULPTURES ---")

for rank, result in enumerate(results, start=1):
    print(f"\nRank: {rank}")
    print("Object ID:", result["object_id"])
    print("Similarity:", round(result["similarity"], 4))