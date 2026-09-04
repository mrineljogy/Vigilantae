from uuid import uuid4

import streamlit as st

from core.geography import CITY_COORDINATES
from core.vision import load_primary_face, save_photo


def render(store):
    st.title("Public report desk")
    st.caption("Record an observation for operator review. This demonstration does not contact authorities automatically.")
    cases = store.many("SELECT case_id, title FROM cases WHERE status = 'Open' ORDER BY created_at DESC")
    choices = {f"{item['case_id']} · {item['title']}": item['case_id'] for item in cases}
    with st.form("public-report", clear_on_submit=True):
        photo = st.file_uploader("Observation photo (JPG or PNG)", type=["jpg", "jpeg", "png"])
        observer = st.text_input("Reporter name *")
        contact = st.text_input("Contact detail (optional)")
        location = st.selectbox("U.S. city *", list(CITY_COORDINATES))
        case_label = st.selectbox("Related case (optional)", ["Unlinked"] + list(choices))
        evidence_terms = st.text_input("Observed non-biometric clues", placeholder="red jacket, backpack, blue sedan")
        details = st.text_area("What was observed? *")
        submitted = st.form_submit_button("Submit report")
    if submitted:
        if not observer.strip() or not details.strip():
            st.error("Enter the reporter name and observation details.")
            return
        report_id = f"VR-{uuid4().hex[:8].upper()}"
        photo_path = save_photo(photo, report_id)
        _, faces = load_primary_face(photo_path)
        if photo and not faces:
            st.warning("The photo was stored, but no clear front-facing face was detected. An operator can still review the report.")
        store.create_report({
            "report_id": report_id, "case_id": choices.get(case_label),
            "observer": observer.strip(), "contact": contact.strip(), "location": location,
            "details": details.strip(), "photo_path": photo_path, "evidence_terms": evidence_terms.strip(), "created_at": store.now(),
        })
        st.success("Report recorded. An operator can assess it in the review queue.")
