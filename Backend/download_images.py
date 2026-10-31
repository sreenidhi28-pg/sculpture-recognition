
import json
from pathlib import Path
from PIL import Image

# Load sculpture metadata
with open("backend/sculptures.json", "r", encoding="utf-8") as file:
    sculptures = json.load(file)

image_folder = Path("backend/dataset")

valid = 0
invalid = 0
missing = 0

print("Verifying sculpture images...\n")

for sculpture in sculptures:
    object_id = sculpture["object_id"]
    image_path = image_folder / f"{object_id}.jpg"

    if not image_path.exists():
        print("Missing:", object_id)
        missing += 1
        continue

    try:
        with Image.open(image_path) as image:
            image.verify()

        print("Valid:", object_id)
        valid += 1

    except Exception as error:
        print("Invalid:", object_id, error)
        invalid += 1

print("\n----------------------------")
print("Total records:", len(sculptures))
print("Valid images:", valid)
print("Invalid images:", invalid)
print("Missing images:", missing)
print("----------------------------")

