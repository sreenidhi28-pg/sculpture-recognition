# AI-Powered Sculpture Recognition System

## 1. Project Overview

The AI-Powered Sculpture Recognition System is an image-based visual similarity search application that identifies sculptures by finding visually similar artworks from The Metropolitan Museum of Art's Open Access collection.

Users can upload an image or capture a sculpture using their computer's webcam. The system uses a pretrained OpenCLIP model to generate image embeddings and Qdrant to identify the top 5 visually similar sculptures.

PostgreSQL is used to retrieve the metadata of the matching sculptures, which is displayed through a React frontend.

## 2. Features

- Upload images for sculpture recognition.
- Capture images using a computer webcam.
- Generate image embeddings using OpenCLIP.
- Perform vector similarity search using Qdrant.
- Retrieve the top 5 visually similar sculptures.
- Display similarity scores.
- Retrieve sculpture metadata from PostgreSQL.
- Display artwork images, titles, artists, medium and dates.
- Validate uploaded image files.

## 3. Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python |
| Image Embedding Model | OpenCLIP ViT-B-32 |
| Backend Framework | FastAPI |
| Frontend | React.js |
| Vector Database | Qdrant |
| Relational Database | PostgreSQL |
| Image Processing | Pillow |
| API Source | The Metropolitan Museum of Art Open Access API |
| Containerization | Docker |

## 4. Dataset

The project uses sculpture data obtained from The Metropolitan Museum of Art Open Access API.

- Number of indexed sculptures: 92
- Image format: JPG
- Image embedding dimensions: 512
- Pretrained model: OpenCLIP ViT-B-32
- Similarity metric: Cosine similarity

The dataset contains sculpture images and associated metadata such as object ID, title, artist, classification, medium, date and image URL.

## 5. System Architecture

The application follows this workflow:

1. The user uploads an image or captures an image using the webcam.
2. React sends the image to the FastAPI backend.
3. FastAPI validates the uploaded image.
4. OpenCLIP converts the image into a 512-dimensional embedding.
5. The embedding is sent to Qdrant.
6. Qdrant performs cosine similarity search and returns the top 5 matching sculpture IDs and similarity scores.
7. FastAPI uses the returned object IDs to retrieve sculpture metadata from PostgreSQL.
8. FastAPI combines the metadata and similarity scores.
9. React displays the matching sculptures and their details.

## 6. Project Structure

```text
sculpture-recognition/
|
|-- Backend/
|   |-- dataset/
|   |-- download_images.py
|   |-- embed.py
|   |-- model.py
|   |-- main.py
|   |-- search.py
|   |-- qdrant_store.py
|   |-- postgres_store.py
|   |-- upload_vectors.py
|   |-- sculptures.json
|   |-- embeddings.npz
|
|-- frontend/
|   |-- src/
|   |   |-- assets/
|   |   |-- App.jsx
|   |   |-- App.css
|   |   |-- index.css
|   |   |-- main.jsx
|
|-- venv/
|-- .env
|-- .gitignore
|-- README.md
```

Note: The virtual environment, .env file and generated embeddings are excluded from Git where appropriate.

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- Docker Desktop
- Git

### Step 1: Clone the Repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd sculpture-recognition
```

### Step 2: Backend Setup

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install fastapi uvicorn python-multipart open_clip_torch qdrant-client "psycopg[binary]" pillow numpy python-dotenv
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:<YOUR_PASSWORD>@localhost:5432/sculpture_db
```

Replace `<YOUR_PASSWORD>` with your own PostgreSQL password.

Do not upload the `.env` file or expose database credentials publicly.

### Step 4: Start Database Services

Start the existing Docker containers:

```powershell
docker start qdrant
docker start sculpture-postgres
```

Qdrant dashboard:

`http://localhost:6333/dashboard`

PostgreSQL database:

`localhost:5432`

### Step 5: Start the Backend

From the project root:

```powershell
python -m uvicorn Backend.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### Step 6: Frontend Setup

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

`http://localhost:5173`

## 8. Database Design

### Qdrant

Qdrant stores the 512-dimensional image embeddings and associated object identifiers.

- Collection name: sculptures
- Vector dimension: 512
- Distance metric: Cosine

It performs nearest-neighbor searches to identify visually similar sculptures.

### PostgreSQL

PostgreSQL stores the sculpture metadata.

The sculptures table contains:

- object_id
- title
- artist
- classification
- medium
- object_date
- image_url

The object ID returned by Qdrant is used to retrieve the corresponding metadata from PostgreSQL.

## 9. Expected Output

For an uploaded or captured sculpture image, the application displays:

- Top 5 visually similar sculptures.
- Sculpture reference images.
- Object IDs and artwork titles.
- Artist information.
- Classification and medium.
- Artwork dates, when available.
- Similarity scores.

## 10. Objective

The objective is to develop an end-to-end AI-powered visual recognition system that enables users to discover sculptures through image similarity search.

The application integrates computer vision, pretrained deep learning models, vector databases, relational databases and a web-based camera interface.