

import os
import tempfile
from io import BytesIO

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

from Backend.model import generate_embedding
from Backend.qdrant_store import client, COLLECTION_NAME

# Load environment variables from the project root
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the FastAPI application
app = FastAPI(title="AI Sculpture Recognition System")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home route
@app.get("/")
def home():
    return {
        "message": "AI Sculpture Recognition API is running!"
    }


# Health check route
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Retrieve sculpture metadata from PostgreSQL
def fetch_sculpture_metadata(object_ids):
    if not DATABASE_URL:
        raise HTTPException(
            status_code=500,
            detail="DATABASE_URL is missing from the .env file."
        )

    if not object_ids:
        return {}

    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        object_id,
                        title,
                        artist,
                        classification,
                        medium,
                        object_date,
                        image_url
                    FROM sculptures
                    WHERE object_id = ANY(%s)
                    """,
                    (object_ids,)
                )

                rows = cur.fetchall()

        # Convert database rows into a dictionary for quick lookup
        return {
            row[0]: {
                "object_id": row[0],
                "title": row[1],
                "artist": row[2],
                "classification": row[3],
                "medium": row[4],
                "date": row[5],
                "image_url": row[6]
            }
            for row in rows
        }

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve sculpture metadata from PostgreSQL."
        )


# Sculpture similarity search route
@app.post("/search")
async def search_sculpture(image: UploadFile = File(...)):

    # Validate uploaded file type
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image."
        )

    temp_path = None

    try:
        # Read the uploaded image
        image_data = await image.read()

        # Check whether the uploaded image is empty
        if not image_data:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty."
            )

        # Validate whether the uploaded file is a real image
        try:
            with Image.open(BytesIO(image_data)) as uploaded_image:
                uploaded_image.verify()

        except (UnidentifiedImageError, OSError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is not a valid image."
            )

        # Save the image temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as temp_file:
            temp_file.write(image_data)
            temp_path = temp_file.name

        # Generate the image embedding using OpenCLIP
        embedding = generate_embedding(temp_path)

        # Search Qdrant for the top 5 similar sculptures
        qdrant_results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=embedding.tolist(),
            limit=5,
            with_payload=True
        ).points

        # Get the sculpture IDs returned by Qdrant
        object_ids = [
            result.payload.get("object_id")
            for result in qdrant_results
            if result.payload and result.payload.get("object_id") is not None
        ]

        # Retrieve their metadata from PostgreSQL
        metadata_by_id = fetch_sculpture_metadata(object_ids)

        # Combine PostgreSQL metadata with Qdrant similarity scores
        matches = []

        for result in qdrant_results:
            if not result.payload:
                continue

            object_id = result.payload.get("object_id")
            metadata = metadata_by_id.get(object_id)

            if metadata is None:
                continue

            matches.append({
                **metadata,
                "similarity_score": result.score
            })

        return {
            "message": "Similar sculptures found!",
            "results": matches
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the image."
        )

    finally:
        # Delete the temporary image after processing
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
