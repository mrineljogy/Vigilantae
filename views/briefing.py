import streamlit as st


def render(store, operator):
    st.title("Operations briefing")
    st.caption("LOCAL REVIEW CONSOLE · U.S. CASEWORK DEMONSTRATION")
    open_cases = store.one("SELECT COUNT(*) AS total FROM cases WHERE status = 'Open'")["total"]
    pending_reports = store.one("SELECT COUNT(*) AS total FROM reports WHERE state = 'Pending'")["total"]
    resolved = store.one("SELECT COUNT(*) AS total FROM cases WHERE status = 'Resolved'")["total"]
    linked = store.one("SELECT COUNT(*) AS total FROM reports WHERE state = 'Reviewed'")["total"]
    columns = st.columns(4)
    for column, label, value in zip(columns, ["Open cases", "Pending reports", "Linked reports", "Resolved cases"], [open_cases, pending_reports, linked, resolved]):
        column.metric(label, value)

    st.divider()
    st.subheader(f"Welcome back, {operator['display_name']}")
    st.markdown("**Review pipeline**")
    st.code("Case created → evidence submitted → non-biometric evidence analysis → photo comparison signal → ranked leads → human review", language=None)
    st.write("Use Register case to add a record, Public report to log an observation, and Review queue to assess ranked leads. This is a local portfolio demo: no police, federal, or emergency-service affiliation is implied.")
    st.info("For an actual emergency or missing-person report, contact local emergency services or the appropriate official agency.")
