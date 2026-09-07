"""
recognize.py — Live webcam face recognition against enrolled database.

Usage:
    python recognize.py

Shows webcam feed with recognized name (or "Unknown") over each detected face.
Press 'q' to quit.
"""

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from database import get_all_users

# --- Config ---
SIMILARITY_THRESHOLD = 0.55  # tune between 0.5-0.6 based on testing

# --- Setup ---
app = FaceAnalysis(name="buffalo_s", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(320, 320))

known_users = get_all_users()
if not known_users:
    print("No enrolled users found. Run enroll.py first.")
    exit()

print(f"Loaded {len(known_users)} enrolled user(s).")


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recognize_face(embedding):
    """Returns (name, score) of best match, or (None, best_score) if below threshold."""
    best_name = None
    best_score = -1

    for name, known_emb in known_users:
        score = cosine_similarity(embedding, known_emb)
        if score > best_score:
            best_score = score
            best_name = name

    if best_score >= SIMILARITY_THRESHOLD:
        return best_name, best_score
    return None, best_score


# --- Live loop ---
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = app.get(frame)

    for face in faces:
        box = face.bbox.astype(int)
        name, score = recognize_face(face.embedding)

        label = f"{name} ({score:.2f})" if name else f"Unknown ({score:.2f})"
        color = (0, 255, 0) if name else (0, 0, 255)

        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
        cv2.putText(
            frame, label, (box[0], box[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2,
        )

        # NOTE: this is where you'd hand off `name` to decision_engine.py
        # once vitals_processor.py is ready, to produce the final verdict.

    cv2.imshow("Recognize Face", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()