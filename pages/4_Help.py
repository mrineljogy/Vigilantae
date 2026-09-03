import streamlit as st

from pages.helper.ui import apply_theme, page_header


st.set_page_config(page_title="Vigilantae — Help", page_icon="🛡️")
apply_theme()

if not st.session_state.get("login_status"):
    st.error("Secure access required. Please sign in from the Home page.")
else:
    page_header(
        "OPERATIONS GUIDE",
        "A quick reference for registering, reviewing, and validating case intelligence.",
        "SUPPORT / FIELD REFERENCE",
    )

    with st.expander("01  Register a case", expanded=True):
        st.markdown(
            "Upload one clear, front-facing photo, select the correct detected face, "
            "and complete the required case and complainant details. A submitted record "
            "starts as **Not Found**."
        )

    with st.expander("02  Review the case archive"):
        st.markdown(
            "Use **All Cases** to filter and review registered records. Admins can edit "
            "or delete records; officers only see records assigned to their own account."
        )

    with st.expander("03  Process public sightings"):
        st.markdown(
            "The public sighting desk runs separately in `mobile_app.py`. Review every "
            "possible match manually before taking action. A match score is a lead, not proof of identity."
        )

    with st.expander("04  Use the field map"):
        st.markdown(
            "Map marker size shows the number of records in a city. Red markers include "
            "unresolved cases; green markers are fully resolved."
        )

    with st.expander("05  Protect case data"):
        st.markdown(
            "Do not export or share photos, contact information, or face-match data without "
            "appropriate authorization. Use a managed database and private image storage before public deployment."
        )
