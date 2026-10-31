
import requests
import json
import time

SEARCH_URL = "https://collectionapi.metmuseum.org/public/collection/v1.1/search"
OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

SEARCH_TERMS = [
    "sculpture",
    "statue",
    "figurine",
    "statuette",
    "relief sculpture"
]

TARGET_COUNT = 100

session = requests.Session()

sculptures = []
all_object_ids = set()
checked_ids = set()

print("Collecting artwork IDs...\n")

for term in SEARCH_TERMS:
    try:
        response = session.get(
            SEARCH_URL,
            params={"q": term, "hasImages": "true"},
            timeout=30
        )
        response.raise_for_status()

        ids = response.json().get("objectIDs") or []

        print(f"{term}: {len(ids)} results")

        all_object_ids.update(ids)

    except requests.RequestException as error:
        print("Search failed:", term, error)

print("\nUnique object IDs:", len(all_object_ids))
print("\nChecking artwork details...\n")

for object_id in all_object_ids:

    if len(sculptures) >= TARGET_COUNT:
        break

    if object_id in checked_ids:
        continue

    checked_ids.add(object_id)

    try:
        response = session.get(
            f"{OBJECT_URL}/{object_id}",
            timeout=30
        )
        response.raise_for_status()

        artwork = response.json()

        classification = artwork.get("classification") or ""
        image_url = artwork.get("primaryImage")

        if "sculpture" in classification.lower() and image_url:

            sculpture = {
                "object_id": artwork.get("objectID"),
                "title": artwork.get("title"),
                "artist": artwork.get("artistDisplayName"),
                "classification": classification,
                "medium": artwork.get("medium"),
                "date": artwork.get("objectDate"),
                "image_url": image_url
            }

            sculptures.append(sculpture)

            print(
                f"{len(sculptures)}. Found: {sculpture['title']}"
            )

        time.sleep(0.1)

    except requests.RequestException as error:
        print("Skipping object:", object_id, error)

with open("backend/sculptures.json", "w", encoding="utf-8") as file:
    json.dump(sculptures, file, indent=4, ensure_ascii=False)

print("\n----------------------------")
print("Unique IDs checked:", len(checked_ids))
print("Total sculptures collected:", len(sculptures))
print("Saved to backend/sculptures.json")
print("----------------------------")

