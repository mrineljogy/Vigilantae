"""Photo-only face detection and visual similarity helpers for operator review."""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


UPLOADS = Path("data/uploads")
CASCADE_PATH = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
DETECTOR = cv2.CascadeClassifier(str(CASCADE_PATH)) if CASCADE_PATH.is_file() else None


def save_photo(uploaded_file, record_id: str) -> str | None:
    if not uploaded_file:
        return None
    image = Image.open(uploaded_file).convert("RGB")
    UPLOADS.mkdir(parents=True, exist_ok=True)
    target = UPLOADS / f"{record_id}.jpg"
    image.thumbnail((1600, 1600))
    image.save(target, format="JPEG", quality=88)
    return str(target)


def load_primary_face(path: str | None):
    if DETECTOR is None or not path or not Path(path).is_file():
        return None, 0
    image = cv2.imread(path)
    if image is None:
        return None, 0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = DETECTOR.detectMultiScale(gray, scaleFactor=1.12, minNeighbors=5, minSize=(48, 48))
    if len(faces) == 0:
        return None, 0
    x, y, width, height = max(faces, key=lambda box: box[2] * box[3])
    return gray[y:y + height, x:x + width], len(faces)


def similarity(reference_path: str | None, candidate_path: str | None):
    reference, reference_count = load_primary_face(reference_path)
    candidate, candidate_count = load_primary_face(candidate_path)
    if reference is None or candidate is None:
        return None, reference_count, candidate_count
    reference = cv2.resize(reference, (96, 96)).astype(np.float32).ravel()
    candidate = cv2.resize(candidate, (96, 96)).astype(np.float32).ravel()
    score = float(np.dot(reference, candidate) / (np.linalg.norm(reference) * np.linalg.norm(candidate) + 1e-9))
    return round(max(0.0, min(1.0, score)) * 100, 1), reference_count, candidate_count
