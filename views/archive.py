import streamlit as st


def render(store, operator):
    st.title("Case archive")
    status = st.selectbox("Show", ["All", "Open", "Resolved"])
    sql = "SELECT case_id, title, age, city, last_known_location, status, created_at FROM cases"
    values = ()
    if status != "All":
        sql += " WHERE status = ?"
        values = (status,)
    records = store.many(sql + " ORDER BY created_at DESC", values)
    if not records:
        st.info("No cases match this view yet.")
        return
    st.dataframe(records, use_container_width=True, hide_index=True)
    st.divider()
    selected = st.selectbox("Case details", [f"{item['case_id']} · {item['title']}" for item in records])
    case_id = selected.split(" · ", 1)[0]
    record = store.one("SELECT * FROM cases WHERE case_id = ?", (case_id,))
    reports = store.many("SELECT report_id, observer, location, details, state, created_at FROM reports WHERE case_id = ? ORDER BY created_at DESC", (case_id,))
    left, right = st.columns([1, 2])
    with left:
        st.markdown(f"**Status:** {record['status']}")
        st.markdown(f"**City:** {record['city']}")
        st.markdown(f"**Last known:** {record['last_known_location']}")
        if record["notes"]:
            st.markdown(f"**Notes:** {record['notes']}")
    with right:
        st.markdown("**Linked reports**")
        st.dataframe(reports or [{"state": "No reports linked"}], use_container_width=True, hide_index=True)
