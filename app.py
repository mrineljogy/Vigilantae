"""Vigilantae — local case-review portfolio application."""

import streamlit as st

from core.auth import authenticate, bootstrap_admin, change_password
from core.store import CaseStore
from core.theme import apply_console_theme, render_hero
from views import archive, briefing, intake, map_view, public_report, review


st.set_page_config(page_title="Vigilantae", page_icon="V", layout="wide")
apply_console_theme()
store = CaseStore()
store.initialize()
bootstrap_admin(store)

if not st.session_state.get("operator"):
    render_hero("SECURE ACCESS / LOCAL ONLY", "Vigilantae", "A sleek local evidence-review console with photo analysis and human-led decisions.")
    st.html("<div class='status-pulse'>● LIVE LOCAL REVIEW CHANNEL · PHOTO-ONLY COMPARISON</div>")
    with st.form("access"):
        username = st.text_input("Operator ID")
        password = st.text_input("Passphrase", type="password")
        submitted = st.form_submit_button("Enter console")
    if submitted:
        operator = authenticate(store, username, password)
        if operator:
            st.session_state.operator = operator
            st.rerun()
        st.error("Access denied.")
    st.info("First run: use admin / ChangeMe!2026, then change the passphrase in Settings.")
    st.stop()

operator = st.session_state.operator
with st.sidebar:
    st.markdown("### VIGILANTAE")
    st.caption(f"SIGNED IN · {operator['display_name'].upper()}")
    page = st.radio("Navigation", ["Briefing", "Register case", "Review queue", "Case archive", "U.S. map", "Public report", "Settings"])
    if st.button("Sign out"):
        st.session_state.clear()
        st.rerun()

if page == "Briefing":
    briefing.render(store, operator)
elif page == "Register case":
    intake.render(store, operator)
elif page == "Review queue":
    review.render(store, operator)
elif page == "Case archive":
    archive.render(store, operator)
elif page == "U.S. map":
    map_view.render(store)
elif page == "Public report":
    public_report.render(store)
else:
    st.header("Operator settings")
    with st.form("password"):
        current = st.text_input("Current passphrase", type="password")
        new = st.text_input("New passphrase", type="password")
        if st.form_submit_button("Update passphrase"):
            if change_password(store, operator["username"], current, new):
                st.success("Passphrase updated.")
            else:
                st.error("Could not update passphrase. Check the current value and use at least 10 characters.")
