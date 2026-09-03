import streamlit as st

from core.geography import locate


def render(store):
    st.title("U.S. field map")
    st.caption("Open and resolved case records by selected city. City-level data is intentionally coarse for this local demo.")
    cases = store.many("SELECT case_id, title, city, status, last_known_location FROM cases ORDER BY created_at DESC")
    points = []
    unresolved = []
    for case in cases:
        coordinate = locate(case["city"])
        if coordinate:
            points.append({"lat": coordinate[0], "lon": coordinate[1], "label": f"{case['case_id']} · {case['title']} · {case['status']}"})
        else:
            unresolved.append(case["city"])
    if points:
        st.map(points, latitude="lat", longitude="lon", size=80, color="#dc2833", zoom=3)
        st.dataframe(points, use_container_width=True, hide_index=True)
    else:
        st.info("Add a case to place a marker on the map.")
    if unresolved:
        st.warning("No coordinate is configured for: " + ", ".join(sorted(set(unresolved))))
