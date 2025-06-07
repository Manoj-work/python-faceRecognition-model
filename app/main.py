from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, uuid
from app.database import users_col
from app.face_utils import get_face_embedding, compare_embeddings
import numpy as np
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with Flutter app domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
async def register_user(file: UploadFile = File(...), name: str = Form(...)):
    filename = f"{uuid.uuid4()}.jpg"
    filepath = f"images/{filename}"
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Get face embedding
    embedding = get_face_embedding(filepath)
    if embedding is None:
        return {"status": "error", "message": "No face detected in the image"}

    # Save user data to database
    user_data = {
        "name": name,
        "embedding": embedding.tolist(),
        "image_path": filepath
    }
    users_col.insert_one(user_data)

    return {"status": "success", "message": "User registered successfully"}

@app.post("/upload/")
async def upload_photo(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}.jpg"
    filepath = f"images/{filename}"
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_emb = get_face_embedding(filepath)
    if new_emb is None:
        return {"status": "error", "message": "No face detected"}

    # Compare with all saved embeddings
    for user in users_col.find():
        known_emb = np.array(user["embedding"])
        if compare_embeddings(known_emb, new_emb):
            return {"status": "present", "employee": user["name"]}

    return {"status": "not found"}
