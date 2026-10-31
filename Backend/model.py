import torch
import open_clip
from PIL import Image

# Select CPU because our laptop has Intel UHD Graphics
DEVICE = "cpu"

# Load pretrained OpenCLIP model
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)

model = model.to(DEVICE)
model.eval()

print("OpenCLIP model loaded successfully!")


def generate_embedding(image_path):

    # Open sculpture image
    image = Image.open(image_path).convert("RGB")

    # Preprocess image
    image_tensor = preprocess(image).unsqueeze(0).to(DEVICE)

    # Generate embedding
    with torch.no_grad():
        embedding = model.encode_image(image_tensor)

        # Normalize embedding
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)

    return embedding.cpu().numpy()[0]


if __name__ == "__main__":

    image_path = "backend/dataset/470879.jpg"

    embedding = generate_embedding(image_path)

    print("Embedding generated successfully!")
    print("Embedding shape:", embedding.shape)
    print("First 10 values:", embedding[:10])