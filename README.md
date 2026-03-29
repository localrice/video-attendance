# Video attendance system
based on facial recognition

This is a flask app that uses insight face module to automate the attendance from videos.

> teacher takes video of the class at once
> upload the video here
> get attendance

### enrolling students
> teacher can add name, roll number and multiple images of a student
> then the images are converted into embeddings and saved into sqlite as blob


## Tech stack

- Python (Flask)
- OpenCV
- InsightFace
- SQLite

## notes

- works on CPU (no GPU required)
- performance depends on video resolution and FPS so having the fps at 10 and the video quality reduced to 0.5 is a must
- accuracy depends on quality of enrolled images and also the video as well