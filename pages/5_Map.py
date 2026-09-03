import pandas as pd
import streamlit as st

from pages.helper import db_queries
from pages.helper.locations import US_CENTER, US_ZOOM, city_coordinates
from pages.helper.ui import apply_theme, page_header


st.set_page_config(page_title="Vigilantae — Case Map", page_icon="🛡️")
apply_theme()

if not st.session_state.get("login_status"):
    st.error("Secure access required. Please sign in from the Home page.")
else:
    page_header(
        "FIELD MAP",
        "Geographic overview of active and resolved cases across the United States.",
        "INTELLIGENCE / LOCATION",
    )

    try:
        import folium
        from streamlit_folium import st_folium
    except ImportError:
        st.error("Map dependencies are missing. Install folium and streamlit-folium.")
        st.stop()

    counts = db_queries.get_case_counts_by_city()
    if not counts:
        st.info("No cases with city data registered yet. Add a U.S. city when registering a case.")
        st.stop()

    # OpenStreetMap is key-free, so the portfolio demo works for every clone.
    m = folium.Map(
        location=US_CENTER,
        zoom_start=US_ZOOM,
        min_zoom=3,
        tiles="OpenStreetMap",
        control_scale=True,
    )
    skipped = []
    for city, data in counts.items():
        coords = city_coordinates(city)
        if coords is None:
            skipped.append(city)
            continue

        total = data["found"] + data["not_found"]
        color = "#e74c3c" if data["not_found"] > 0 else "#27ae60"
        tooltip = (
            f"<b>{city}</b><br>Total: {total}<br>"
            f"Not Found: {data['not_found']}<br>Found: {data['found']}"
        )
        folium.CircleMarker(
            location=coords,
            radius=max(8, min(40, total * 5)),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.65,
            tooltip=folium.Tooltip(tooltip),
        ).add_to(m)

    st_folium(m, width="100%", height=550, returned_objects=[])
    st.caption("Red: unresolved cases · Green: all cases resolved · Marker size: number of cases")

    if skipped:
        st.warning(
            "These cities are not yet in the U.S. coordinate directory: "
            f"{', '.join(skipped)}. Add them to pages/helper/locations.py."
        )

    rows = [
        {
            "City": city,
            "Total": data["found"] + data["not_found"],
            "Found": data["found"],
            "Unresolved": data["not_found"],
            "Resolution rate": (
                f"{(data['found'] / (data['found'] + data['not_found']) * 100):.0f}%"
                if data["found"] + data["not_found"]
                else "—"
            ),
        }
        for city, data in counts.items()
    ]
    st.subheader("City Summary")
    st.dataframe(
        pd.DataFrame(rows).sort_values("Total", ascending=False).reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )
