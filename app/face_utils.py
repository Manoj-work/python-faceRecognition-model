from insightface.app import FaceAnalysis
import numpy as np
import cv2

# Load InsightFace model
app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

def get_face_embedding(image_path):
    img = cv2.imread(image_path)
    faces = app.get(img)
    if len(faces) > 0:
        return faces[0].embedding
    return None

def compare_embeddings(known_emb, new_emb, threshold=0.4):
    # Cosine similarity
    cosine_sim = np.dot(known_emb, new_emb) / (np.linalg.norm(known_emb) * np.linalg.norm(new_emb))
    return cosine_sim > (1 - threshold)
