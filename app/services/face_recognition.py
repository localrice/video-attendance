import cv2
import numpy as np
import insightface

app = insightface.app.FaceAnalysis()
app.prepare(ctx_id=0, det_size=(320, 320))

def get_embeddings_from_image(image):
    """
    Input: cv2 image
    Output: list of embeddings
    """
    faces = app.get(image)
    return [face.embedding for face in faces]


# check for similarity of the faces
# even idk how this part works
# TODO: revisit this function
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


"""
db format:
{
  student_id: {
    "name": str,
    "roll": str,
    "embeddings": [np.ndarray]
  }
}

returns: (student_id, score)
"""
def find_best_match(embedding, db, threshold=0.6):
    best_id = None
    best_score = 0

    for student_id, data in db.items():
        for known_emb in data["embeddings"]:
            sim = cosine_similarity(embedding, known_emb)

            if sim > best_score:
                best_score = sim
                best_id = student_id

    if best_score > threshold:
        return best_id, best_score

    return None, best_score