from flask import request, render_template
import cv2
import numpy as np
import os


from app.services.face_recognition import get_embeddings_from_image, find_best_match
from app.services.db_service import load_db


def attendance_route():
    if request.method == "GET":
        return render_template("attendance.html", present_list=None)


    file = request.files["video"]

    os.makedirs("uploads", exist_ok=True)
    video_path = os.path.join("uploads", file.filename)
    print(video_path)
    file.save(video_path)

    db = load_db()
    present = set()

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # process 1 frame per second
        if frame_count % int(fps) != 0:
            continue

        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        embeddings = get_embeddings_from_image(frame)

        for emb in embeddings:
            student_id, score = find_best_match(emb, db)

            if student_id:
                present.add(student_id)

    cap.release()

    present_list = [
        {
            "name": db[s]["name"],
            "roll": db[s]["roll"]
        }
        for s in present
    ]
    print(present_list)
    return render_template(
        "attendance.html",
        present_list=present_list,
        total=len(present_list)
    )