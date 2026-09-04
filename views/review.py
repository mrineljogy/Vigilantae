import streamlit as st

from core.scoring import rank_leads
from core.theme import render_face_scan_panel, render_hero


def render(store, operator):
    render_hero("ANALYSIS DESK / 03", "Ranked lead review", "Non-biometric evidence and photo signals are combined into an explainable review priority—not an identity decision.")
    render_face_scan_panel()
    reports = store.many("SELECT * FROM reports WHERE state = 'Pending' ORDER BY created_at ASC")
    cases = store.many("SELECT case_id, title, city, photo_path, evidence_terms FROM cases WHERE status = 'Open' ORDER BY created_at DESC")
    if not reports:
        st.success("No evidence submissions are waiting for review.")
        return
    if not cases:
        st.warning("Open a case before reviewing submitted evidence.")
        return

    for report in reports:
        leads = rank_leads(cases, report)
        with st.container(border=True):
            st.subheader(f"Evidence {report['report_id']} · {report['location']}")
            st.write(report["details"])
            if report["evidence_terms"]:
                st.caption("Observed clues: " + report["evidence_terms"])
            st.caption(f"Reporter: {report['observer']} · Submitted {report['created_at'][:16].replace('T', ' ')} UTC")
            st.markdown("#### Ranked leads")
            table = [{"Priority": index + 1, "Case": lead["title"], "Lead score": f"{lead['score']}%", "Why": " · ".join(lead["reasons"])} for index, lead in enumerate(leads)]
            st.dataframe(table, use_container_width=True, hide_index=True)
            selected = st.selectbox("Select a lead for human review", [f"{lead['case_id']} · {lead['title']} · {lead['score']}%" for lead in leads], key=f"lead-{report['report_id']}")
            selected_id = selected.split(" · ", 1)[0]
            lead = next(item for item in leads if item["case_id"] == selected_id)
            if lead["photo_score"] is None:
                st.caption("Photo signal unavailable: add clear, front-facing photos to both records. Non-biometric clues still contribute to the ranking.")
            else:
                st.metric("Photo comparison signal", f"{lead['photo_score']}%")
                st.caption(f"Detected faces — case: {lead['case_faces']}; submitted photo: {lead['report_faces']}. Verify manually.")
            with st.form(f"review-{report['report_id']}"):
                action = st.radio("Human review decision", ["Keep case open", "Resolve case"], horizontal=True)
                if st.form_submit_button("Record decision"):
                    store.assign_report(report["report_id"], selected_id)
                    if action == "Resolve case":
                        store.set_case_status(selected_id, "Resolved")
                    st.success("Human review decision recorded.")
                    st.rerun()
