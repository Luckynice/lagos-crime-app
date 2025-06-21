import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# Page config for sidebar + tab title
st.set_page_config(page_title="Crime Map", page_icon="🗺️")

def show_crime_map():
    st.title("🗺️ Lagos Crime Map")
    st.markdown("Explore reported crime incidents across Lagos on an interactive map.")

    # Load data
    df = load_data()

    if df.empty or 'latitude' not in df.columns or 'longitude' not in df.columns:
        st.error("No valid crime location data available.")
        return

    # Clean invalid coordinates
    df = df.dropna(subset=["latitude", "longitude", "crime_type"])
    df = df[(df["latitude"] != 0) & (df["longitude"] != 0)].copy()

    if df.empty:
        st.error("No valid coordinates to display on the map.")
        return

    # Filter by crime types
    crime_types = df['crime_type'].dropna().unique().tolist()
    crime_types.sort()
    selected_crimes = st.multiselect(
        "Select Crime Types",
        options=crime_types,
        default=crime_types[:3] if len(crime_types) >= 3 else crime_types
    )

    filtered_df = df[df['crime_type'].isin(selected_crimes)].copy()

    if filtered_df.empty:
        st.warning("No crimes match the selected filters.")
        return

    # Format datetime for hover
    if "date_time" in filtered_df.columns:
        filtered_df["date_time"] = pd.to_datetime(filtered_df["date_time"], errors="coerce")
        filtered_df["date_time"] = filtered_df["date_time"].dt.strftime("%b %d, %Y %I:%M %p")

    # Choose hover area field
    area_field = "area" if "area" in df.columns else "lga"

    # 🗺️ Map style toggle
    map_styles = {
        "Light (Carto)": "carto-positron",
        "Dark": "carto-darkmatter",
        "Open Street Map": "open-street-map",
        "Satellite": "satellite-streets",
        "Outdoors": "outdoors",
        "Basic": "streets"
    }

    selected_style = st.selectbox("Select Map Style", list(map_styles.keys()), index=0)
    mapbox_style = map_styles[selected_style]

    # 📍 Map rendering
    fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        hover_name="crime_type",
        hover_data=[area_field, "date_time"] if "date_time" in filtered_df.columns else [area_field],
        color="crime_type",
        zoom=10,
        height=600
    )

    fig.update_layout(
        mapbox_style=mapbox_style,
        mapbox_center={"lat": 6.5244, "lon": 3.3792},  # Lagos
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)

    # Optional data preview
    with st.expander("📄 View Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)

    st.markdown("### 📊 Map Insights")

# Optional: direct run
if __name__ == "__main__":
    show_crime_map()
