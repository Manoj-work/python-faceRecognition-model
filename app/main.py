from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.database import users_col
from app.face_utils import get_face_embedding, compare_embeddings
import numpy as np

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Flutter app URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# 1. Register New Employee
# ----------------------------------------
@app.post("/register")
async def register_user(
    file: UploadFile = File(...),
    name: str = Form(...),
    empId: str = Form(...),
    imgUrl: str = Form(...)
):
    if users_col.find_one({"empId": empId}):
        return {"status": "error", "message": "Employee ID already registered"}

    embedding = get_face_embedding(file.file)
    if embedding is None:
        return {"status": "error", "message": "No face detected in the image"}

    user_data = {
        "name": name,
        "empId": empId,
        "embedding": embedding.tolist(),
        "imgUrl": imgUrl
    }
    users_col.insert_one(user_data)
    return {"status": "success", "message": "User registered successfully"}

# ----------------------------------------
# 2. Verify by Single Emp ID
# ----------------------------------------
@app.post("/verify/by-empid")
async def verify_by_empid(
    empId: str = Form(...),
    file: UploadFile = File(...)
):
    user = users_col.find_one({"empId": empId})
    if not user:
        return {"status": "error", "message": "Employee not found"}

    new_emb = get_face_embedding(file.file)
    if new_emb is None:
        return {"status": "error", "message": "No face detected in the image"}

    known_emb = np.array(user["embedding"])
    if compare_embeddings(known_emb, new_emb):
        return {
            "status": "match",
            "empId": user["empId"],
            "employee": user["name"],
            "imgUrl": user["imgUrl"]
        }

    return {"status": "no_match", "empId": empId}

# ----------------------------------------
# 3. Verify by List of Emp IDs
# ----------------------------------------
@app.post("/verify/by-empid-list")
async def verify_by_empid_list(
    empIds: str = Form(...),  # Comma-separated empIds
    file: UploadFile = File(...)
):
    id_list = [eid.strip() for eid in empIds.split(",") if eid.strip()]
    users = users_col.find({"empId": {"$in": id_list}})

    new_emb = get_face_embedding(file.file)
    if new_emb is None:
        return {"status": "error", "message": "No face detected in the image"}

    for user in users:
        known_emb = np.array(user["embedding"])
        if compare_embeddings(known_emb, new_emb):
            return {
                "status": "match",
                "empId": user["empId"],
                "employee": user["name"],
                "imgUrl": user["imgUrl"]
            }

    return {"status": "no_match"}

# ----------------------------------------
# 4. Verify Against All Employees
# ----------------------------------------
@app.post("/verify/all")
async def verify_against_all(file: UploadFile = File(...)):
    new_emb = get_face_embedding(file.file)
    if new_emb is None:
        return {"status": "error", "message": "No face detected in the image"}

    for user in users_col.find():
        known_emb = np.array(user["embedding"])
        if compare_embeddings(known_emb, new_emb):
            return {
                "status": "match",
                "empId": user["empId"],
                "employee": user["name"],
                "imgUrl": user["imgUrl"]
            }

    return {"status": "no_match"}
