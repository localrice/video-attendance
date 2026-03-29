from flask import request, render_template
import cv2
import numpy as np

from app.services.face_recognition import get_embeddings_from_image
from app.services.db_service import add_student, add_embedding, get_all_students

def enroll_route():
    if request.method == "GET":
        students = get_all_students()
        return render_template("enroll.html", students=students, message=None)
    
    name = request.form["name"]
    roll = request.form["roll"]
    files = request.files.getlist("images")

    student_id = add_student(name, roll)

    for file in files:
        # read raw file bytes ( compressed image: JPED/PNG)
        file_bytes = np.frombuffer(file.read(), np.uint8)
        # decode into image array (Height x Width x 3 color channels, uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        # print(img)
        if img is None:
            continue

        embeddings = get_embeddings_from_image(img)

        for emb in embeddings:
            add_embedding(student_id, emb)

    students = get_all_students()
    return render_template(
        "enroll.html",
        students=students,
        message=f"{name} enrolled successfully"
    )
