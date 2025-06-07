from insightface.app import FaceAnalysis
import numpy as np
import cv2
import io

# Initialize face analysis
app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

def get_face_embedding(file_obj):
    # Read image from file object
    contents = file_obj.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Detect faces
    faces = app.get(img)
    if len(faces) == 0:
        return None
    
    # Get embedding of the first face
    return faces[0].embedding

def compare_embeddings(emb1, emb2, threshold=0.5):
    # Calculate cosine similarity
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return similarity > threshold
