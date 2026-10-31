from pathlib import Path
from PIL import Image

image_folder = Path("backend/dataset")

for image_path in image_folder.glob("*.jpg"):
    try:
        with Image.open(image_path) as img:
            img.verify()

        print(f"Valid image: {image_path.name}")

    except Exception as error:
        print(f"Invalid image: {image_path.name}", error)