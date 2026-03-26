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