from uuid import uuid4

import streamlit as st

from core.geography import CITY_COORDINATES
from core.theme import render_face_scan_panel, render_hero
from core.vision import load_primary_face, save_photo


def render(store, operator):
    render_hero("CASE INTAKE / 01", "Register a case", "Create a local case record and provide optional reference evidence for structured review.")
    render_face_scan_panel()
    with st.form("case-intake", clear_on_submit=True):
        left, right = st.columns(2)
        with left:
            photo = st.file_uploader("Reference photo — JPG or PNG", type=["jpg", "jpeg", "png"])
            title = st.text_input("Case title *", placeholder="Example: Jordan Doe")
            age = st.number_input("Age", min_value=0, max_value=120, value=25)
            guardian = st.text_input("Contact person")
            phone = st.text_input("Contact number")
        with right:
            city = st.selectbox("U.S. city *", list(CITY_COORDINATES))
            last_known = st.text_input("Last known location *", placeholder="Transit station, neighborhood, landmark")
            evidence_terms = st.text_input("Known non-biometric clues", placeholder="red jacket, backpack, blue sedan")
            notes = st.text_area("Review notes", placeholder="Describe information useful to an operator.")
        submitted = st.form_submit_button("Create case")
    if submitted:
        if not title.strip() or not last_known.strip():
            st.error("Enter a case title and last known location.")
            return
        case_id = f"VC-{uuid4().hex[:8].upper()}"
        photo_path = save_photo(photo, case_id)
        _, faces = load_primary_face(photo_path)
        if photo and not faces:
            st.warning("The photo was stored, but no clear front-facing face was detected. Reviewers can still assess it manually.")
        store.create_case({
            "case_id": case_id, "title": title.strip(), "age": int(age), "guardian": guardian.strip(),
            "contact_phone": phone.strip(), "city": city, "last_known_location": last_known.strip(),
            "notes": notes.strip(), "photo_path": photo_path, "evidence_terms": evidence_terms.strip(), "created_by": operator["username"], "created_at": store.now(),
        })
        st.success(f"Case {case_id} is now open and appears in the archive and U.S. map.")
