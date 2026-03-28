from flask import request, render_template
import cv2
import numpy as np

from app.services.face_recognition import get_embeddings_from_image
from app.services.db_service import add_student, add_embedding


def enroll_route():
    if request.method == "GET":
        return render_template("enroll.html")
    
    name = request.form["name"]
    roll = request.form["roll"]
    files = request.files.getlist("images")

    student_id = add_student(name, roll)

    for file in files:
        file_bytes = np.frombuffer(file.read(), np.uint8)
        print(file_bytes)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        # print(img)
        if img is None:
            continue

        embeddings = get_embeddings_from_image(img)

        for emb in embeddings:
            add_embedding(student_id, emb)

    return f"{name} enrolled succesfully"
