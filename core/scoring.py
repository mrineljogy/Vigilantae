"""Explainable lead ranking for human case review."""

from core.vision import similarity


def _terms(value: str | None) -> set[str]:
    return {item.strip().lower() for item in (value or "").split(",") if item.strip()}


def assess_lead(case: dict, report: dict) -> dict:
    """Combine photo and non-biometric clues into an explainable review priority."""
    face_score, case_faces, report_faces = similarity(case.get("photo_path"), report.get("photo_path"))
    shared_terms = sorted(_terms(case.get("evidence_terms")) & _terms(report.get("evidence_terms")))
    location_score = 25 if case["city"] == report["location"] else 0
    evidence_score = min(30, len(shared_terms) * 10)
    photo_score = round((face_score or 0) * .45)
    total = min(100, location_score + evidence_score + photo_score)
    reasons = []
    if location_score:
        reasons.append("same city")
    if shared_terms:
        reasons.append("shared clues: " + ", ".join(shared_terms))
    if face_score is not None:
        reasons.append(f"photo signal: {face_score}%")
    return {
        "case_id": case["case_id"], "title": case["title"], "score": total,
        "photo_score": face_score, "shared_terms": shared_terms, "reasons": reasons or ["insufficient comparable evidence"],
        "case_faces": case_faces, "report_faces": report_faces,
    }


def rank_leads(cases: list[dict], report: dict) -> list[dict]:
    return sorted((assess_lead(case, report) for case in cases), key=lambda item: item["score"], reverse=True)
