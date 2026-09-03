import streamlit as st

from core.vision import similarity


def render(store, operator):
    st.title("Review queue")
    st.caption("Link a report to an open case after manual assessment.")
    reports = store.many("SELECT * FROM reports WHERE state = 'Pending' ORDER BY created_at ASC")
    cases = store.many("SELECT case_id, title, city, photo_path FROM cases WHERE status = 'Open' ORDER BY created_at DESC")
    if not reports:
        st.success("No reports are waiting for review.")
        return
    if not cases:
        st.warning("Open a case before reviewing reports.")
        return
    case_options = {f"{item['case_id']} · {item['title']} ({item['city']})": item['case_id'] for item in cases}
    for report in reports:
        with st.container(border=True):
            st.subheader(f"{report['report_id']} · {report['location']}")
            st.write(report["details"])
            st.caption(f"Reporter: {report['observer']} · Submitted {report['created_at'][:16].replace('T', ' ')} UTC")
            with st.form(f"review-{report['report_id']}"):
                target = st.selectbox("Link to case", list(case_options), key=f"target-{report['report_id']}")
                action = st.radio("Case decision", ["Keep case open", "Resolve case"], horizontal=True, key=f"action-{report['report_id']}")
                if st.form_submit_button("Confirm review"):
                    case_id = case_options[target]
                    store.assign_report(report["report_id"], case_id)
                    if action == "Resolve case":
                        store.set_case_status(case_id, "Resolved")
                    st.success("Review decision recorded.")
                    st.rerun()
            selected_case = next(item for item in cases if item["case_id"] == case_options[target])
            score, case_faces, report_faces = similarity(selected_case["photo_path"], report["photo_path"])
            if score is None:
                st.caption("Photo comparison unavailable: upload clear, front-facing photos to both records.")
            else:
                st.metric("Experimental visual similarity", f"{score}%")
                st.caption(f"Face detections — reference: {case_faces}; report: {report_faces}. Confirm every result manually.")
