"""
face_service.py — Reusable single-shot face scan function.
Used by app.py (Flask) instead of the standalone recognize.py loop.
"""

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from database import get_all_users

_engine = None  # loaded once, reused across requests


def _get_engine():
    global _engine
    if _engine is None:
        _engine = FaceAnalysis(name="buffalo_s", providers=["CPUExecutionProvider"])
        _engine.prepare(ctx_id=0, det_size=(320, 320))
    return _engine


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def scan_face(threshold=0.55, camera_index=0, warmup_frames=8):
    """
    Opens the webcam, grabs a few frames until a face is found, matches it
    against the enrolled DB, and returns a plain dict (JSON-safe).
    """
    engine = _get_engine()
    known_users = get_all_users()

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return {"success": False, "error": "Could not open webcam"}

    detected_face = None
    try:
        for _ in range(warmup_frames):
            ret, frame = cap.read()
            if not ret:
                continue
            faces = engine.get(frame)
            if faces:
                detected_face = faces[0]
                break
    finally:
        cap.release()

    if detected_face is None:
        return {"success": False, "error": "No face detected"}

    if not known_users:
        return {"success": True, "recognized": False, "name": None, "score": 0.0}

    best_name, best_score = None, -1.0
    for name, known_embedding in known_users:
        score = cosine_similarity(detected_face.embedding, known_embedding)
        if score > best_score:
            best_score, best_name = score, name

    recognized = best_score >= threshold
    return {
        "success": True,
        "recognized": recognized,
        "name": best_name if recognized else None,
        "score": round(best_score, 3),
    }