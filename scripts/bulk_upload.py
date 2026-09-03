"""
Bulk upload script for seeding the missing persons database.

Usage (run from project root):
    python scripts/bulk_upload.py                        # uses 'admin' as officer
    python scripts/bulk_upload.py --officer <username>   # match your login username

Directory layout:
    scripts/bulk_data/reported/        → images of missing persons (RegisteredCases)
    scripts/bulk_data/publicly_seen/   → images of sighted persons (PublicSubmissions)

Images can be jpg, jpeg, or png. The script generates realistic metadata for
each image and skips any image where no face is detected.
"""

import argparse
import json
import os
import random
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# ── Allow imports from project root ──────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import PIL.Image
import numpy as np

from pages.helper.data_models import RegisteredCases, PublicSubmissions
from pages.helper import db_queries
from pages.helper.utils import _ensure_model_silent, extract_face_mesh_from_frame

# ── Seed data ─────────────────────────────────────────────────────────────────

CITIES = [
    "Atlanta", "Boston", "Chicago", "Dallas", "Denver", "Houston",
    "Los Angeles", "Miami", "New York", "Philadelphia", "Phoenix",
    "San Francisco", "Seattle", "Washington, DC",
]

FIRST_NAMES_MALE = [
    "Alex", "Cameron", "Casey", "Drew", "Elliot", "Jordan", "Morgan", "Riley",
]

FIRST_NAMES_FEMALE = [
    "Avery", "Blake", "Harper", "Jamie", "Morgan", "Peyton", "Quinn", "Taylor",
]

LAST_NAMES = ["Anderson", "Bennett", "Carter", "Davis", "Ellis", "Foster", "Hayes", "Parker"]

AREAS = [
    "Block {n} near {landmark} station",
    "near {landmark} transit center",
    "{landmark} downtown district",
    "near {landmark} community center",
    "{landmark} neighborhood",
]

AREA_LANDMARKS = [
    "Central", "Riverside", "North", "South", "East", "West",
]

BIRTH_MARKS = [
    "Small mole on left cheek",
    "Scar on right forehead",
    "Dark birthmark near right ear",
    "Small scar below left eye",
    "Mole on chin",
    "",
    "",
    "Cut mark on left eyebrow",
    "Small mole on right cheek",
    "",
]

DESCRIPTIONS = [
    "Portfolio demo record — not a real case.",
    "Synthetic data for interface demonstration only.",
    "Demo profile used to validate the case workflow.",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _random_name(gender: str = None) -> str:
    if gender == "female":
        first = random.choice(FIRST_NAMES_FEMALE)
    elif gender == "male":
        first = random.choice(FIRST_NAMES_MALE)
    else:
        first = random.choice(FIRST_NAMES_MALE + FIRST_NAMES_FEMALE)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"


def _random_mobile() -> str:
    prefixes = ["98", "97", "96", "95", "94", "93", "80", "81", "70", "99"]
    return random.choice(prefixes) + str(random.randint(10000000, 99999999))


def _demo_case_reference() -> str:
    """Return a fictional internal reference for portfolio-only seed records."""
    return f"VIG-DEMO-{random.randint(10000, 99999)}"


def _random_area(city: str) -> str:
    template = random.choice(AREAS)
    landmark = random.choice(AREA_LANDMARKS)
    n = random.randint(3, 25)
    return template.format(landmark=landmark, n=n) + f", {city}"


def _random_last_seen(city: str) -> str:
    days_ago = random.randint(1, 90)
    past_date = datetime.now() - timedelta(days=days_ago)
    date_str = past_date.strftime("%d %b %Y")
    area = _random_area(city)
    return f"{area} on {date_str}"


def _load_image_as_numpy(path: str) -> np.ndarray:
    img = PIL.Image.open(path).convert("RGB")
    return np.array(img)


def _image_files(folder: Path) -> list:
    exts = {".jpg", ".jpeg", ".png"}
    return [f for f in sorted(folder.iterdir()) if f.suffix.lower() in exts]


# ── Main upload routines ──────────────────────────────────────────────────────

def upload_reported(folder: Path, officer: str = "admin") -> tuple[int, int]:
    """Process images in reported/ and insert RegisteredCases rows."""
    files = _image_files(folder)
    if not files:
        print("  No image files found in reported/")
        return 0, 0

    ok = skip = 0
    resources_dir = ROOT / "resources"
    resources_dir.mkdir(exist_ok=True)

    for img_path in files:
        print(f"  [{img_path.name}] ", end="", flush=True)
        try:
            image_np = _load_image_as_numpy(str(img_path))
            landmarks = extract_face_mesh_from_frame(image_np)
        except Exception as e:
            print(f"ERROR loading image: {e}")
            skip += 1
            continue

        if landmarks is None:
            print("no face detected — skipped")
            skip += 1
            continue

        case_id = str(uuid.uuid4())

        # Copy image to resources/
        dest = resources_dir / f"{case_id}.jpg"
        try:
            PIL.Image.open(img_path).convert("RGB").save(str(dest), "JPEG")
        except Exception as e:
            print(f"ERROR saving image: {e}")
            skip += 1
            continue

        city = random.choice(CITIES)
        age = random.randint(5, 75)

        case = RegisteredCases(
            id=case_id,
            submitted_by=officer,
            name=_random_name(),
            guardian_name=_random_name(gender="male"),
            age=str(age),
            complainant_name=_random_name(),
            complainant_mobile=_random_mobile(),
            complainant_email=None,
            case_reference=_demo_case_reference(),
            last_seen=_random_last_seen(city),
            address=_random_area(city),
            city=city,
            description=random.choice(DESCRIPTIONS),
            face_mesh=json.dumps(landmarks),
            status="NF",
            birth_marks=random.choice(BIRTH_MARKS),
            matched_with="",
        )

        try:
            db_queries.register_new_case(case)
            print(f"registered as {case_id[:8]}…")
            ok += 1
        except Exception as e:
            print(f"DB ERROR: {e}")
            if dest.exists():
                dest.unlink()
            skip += 1

    return ok, skip


def upload_publicly_seen(folder: Path) -> tuple[int, int]:
    """Process images in publicly_seen/ and insert PublicSubmissions rows."""
    files = _image_files(folder)
    if not files:
        print("  No image files found in publicly_seen/")
        return 0, 0

    ok = skip = 0
    resources_dir = ROOT / "resources"
    resources_dir.mkdir(exist_ok=True)

    for img_path in files:
        print(f"  [{img_path.name}] ", end="", flush=True)
        try:
            image_np = _load_image_as_numpy(str(img_path))
            landmarks = extract_face_mesh_from_frame(image_np)
        except Exception as e:
            print(f"ERROR loading image: {e}")
            skip += 1
            continue

        if landmarks is None:
            print("no face detected — skipped")
            skip += 1
            continue

        sub_id = str(uuid.uuid4())

        # Copy image to resources/ so the app can display it
        dest = resources_dir / f"{sub_id}.jpg"
        try:
            PIL.Image.open(img_path).convert("RGB").save(str(dest), "JPEG")
        except Exception as e:
            print(f"ERROR saving image: {e}")
            skip += 1
            continue

        city = random.choice(CITIES)

        submission = PublicSubmissions(
            id=sub_id,
            submitted_by=_random_name(),
            face_mesh=json.dumps(landmarks),
            location=_random_area(city),
            mobile=_random_mobile(),
            email=None,
            status="NF",
            birth_marks=random.choice(BIRTH_MARKS),
        )

        try:
            db_queries.new_public_case(submission)
            print(f"submitted as {sub_id[:8]}…")
            ok += 1
        except Exception as e:
            print(f"DB ERROR: {e}")
            if dest.exists():
                dest.unlink()
            skip += 1

    return ok, skip


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Bulk upload images into the missing persons DB.")
    parser.add_argument(
        "--officer",
        default="admin",
        help="Login username to assign as submitted_by for reported cases (default: admin)",
    )
    args = parser.parse_args()

    # Change to project root so relative DB path resolves correctly
    os.chdir(ROOT)

    db_queries.create_db()

    _ensure_model_silent()

    bulk_dir = Path(__file__).parent / "bulk_data"
    reported_dir = bulk_dir / "reported"
    seen_dir = bulk_dir / "publicly_seen"

    print(f"\n=== Bulk upload — Reported (missing persons) [officer: {args.officer}] ===")
    ok_r, skip_r = upload_reported(reported_dir, officer=args.officer)
    print(f"  Done: {ok_r} registered, {skip_r} skipped\n")

    print("=== Bulk upload — Publicly Seen (sightings) ===")
    ok_s, skip_s = upload_publicly_seen(seen_dir)
    print(f"  Done: {ok_s} submitted, {skip_s} skipped\n")

    total_ok = ok_r + ok_s
    total_skip = skip_r + skip_s
    print(f"=== Summary: {total_ok} uploaded, {total_skip} skipped ===\n")


if __name__ == "__main__":
    main()
