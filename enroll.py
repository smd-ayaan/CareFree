"""
enroll.py — Capture a person's face and save their ArcFace embedding to the DB.

Usage:
    python enroll.py

Press SPACE to capture a face sample (do this 3-5 times from slightly
different angles for a more robust average embedding). Press 'q' when done.
"""

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from database import init_db, add_user

# --- Setup ---
init_db()

app = FaceAnalysis(name="buffalo_s", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(320, 320))

name = input("Enter the person's name to enroll: ").strip()
if not name:
    print("Name cannot be empty. Exiting.")
    exit()

cap = cv2.VideoCapture(0)
captured_embeddings = []

print("\nPress SPACE to capture a sample (do 3-5 from different angles).")
print("Press 'q' to finish and save.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Webcam read failed.")
        break

    faces = app.get(frame)
    display = frame.copy()

    for face in faces:
        box = face.bbox.astype(int)
        cv2.rectangle(display, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

    cv2.putText(
        display,
        f"Samples captured: {len(captured_embeddings)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )
    cv2.imshow("Enroll Face", display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(" "):
        if len(faces) == 1:
            captured_embeddings.append(faces[0].embedding)
            print(f"Sample {len(captured_embeddings)} captured.")
        elif len(faces) == 0:
            print("No face detected — try again.")
        else:
            print("Multiple faces detected — only one person at a time.")

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

if len(captured_embeddings) == 0:
    print("No samples captured. Nothing saved.")
else:
    avg_embedding = np.mean(captured_embeddings, axis=0)
    add_user(name, avg_embedding)
    print(f"\nSaved '{name}' to database with {len(captured_embeddings)} samples averaged.")