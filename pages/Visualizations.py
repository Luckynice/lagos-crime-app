import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Crime Visualizations", page_icon="📊", layout="wide")

@st.cache_data(ttl=3600)
def load_lagos_crime_data():
    try:
        df = pd.read_csv("data/lagos_crime_data.csv")

        # Ensure lowercase, remove duplicate columns
        df.columns = df.columns.str.lower()
        df = df.loc[:, ~df.columns.duplicated()]

        # Parse datetime and extract components
        df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
        df = df.dropna(subset=['date_time'])
        df['date'] = df['date_time'].dt.date
        df['hour'] = df['date_time'].dt.hour
        df['day_of_week'] = df['date_time'].dt.day_name()

        # Rename area to lga if needed
        if 'area' in df.columns and 'lga' not in df.columns:
            df.rename(columns={'area': 'lga'}, inplace=True)

        # Map severity levels
        severity_map = {
            "robbery": "High", "assault": "Medium", "theft": "Medium",
            "vandalism": "Low", "burglary": "High", "fraud": "Medium",
            "kidnapping": "High", "murder": "High"
        }
        df['severity'] = df['crime_type'].map(lambda x: severity_map.get(str(x).lower(), "Low"))

        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

def show_visualizations():
    st.title("📊 Lagos Crime Data Explorer")
    st.markdown("Use the filters to explore visual trends in crime across Lagos.")

    data = load_lagos_crime_data()
    if data.empty:
        st.warning("⚠️ No data loaded.")
        return

    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filter Crime Data")

    # Fix lga selection if lga column is not a Series
    try:
        lgas = sorted(data['lga'].dropna().unique())
    except AttributeError:
        lgas = sorted(data['lga'].iloc[:, 0].dropna().unique())  # fallback if lga is a DataFrame

    selected_lgas = st.sidebar.multiselect("📍 LGAs", lgas, default=lgas[:5])

    crimes = sorted(data['crime_type'].dropna().unique())
    selected_crimes = st.sidebar.multiselect("🦹 Crime Types", crimes, default=crimes)

    severities = sorted(data['severity'].dropna().unique())
    selected_severity = st.sidebar.multiselect("⚠️ Severity Levels", severities, default=severities)

    hour_range = st.sidebar.slider("🕒 Hour Range", 0, 23, (6, 20))

    min_date = data['date'].min()
    max_date = data['date'].max()
    date_range = st.sidebar.date_input("📅 Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

    # --- Apply Filters ---
    filtered = data[
        (data['lga'].isin(selected_lgas)) &
        (data['crime_type'].isin(selected_crimes)) &
        (data['severity'].isin(selected_severity)) &
        (data['hour'] >= hour_range[0]) &
        (data['hour'] <= hour_range[1])
    ]

    if len(date_range) == 2:
        filtered = filtered[
            (filtered['date'] >= date_range[0]) &
            (filtered['date'] <= date_range[1])
        ]

    st.caption(f"🔎 Showing **{len(filtered)}** records based on selected filters")

    # ---------- TABS ----------
    tab1, tab2, tab3 = st.tabs(["📍 By Location", "📅 By Time", "🌡️ Heatmaps"])

    # ---------- TAB 1: Location ----------
    with tab1:
        st.subheader("📍 Crimes by Location & Map")

        col1, col2 = st.columns(2)

        with col1:
            if not filtered.empty:
                fig_lga = px.histogram(
                    filtered,
                    x="lga",
                    color="severity",
                    title="Crimes by LGA (Grouped by Severity)",
                    barmode='group',
                    labels={'count': 'Crime Count'},
                    color_discrete_map={"High": "#EF553B", "Medium": "#636EFA", "Low": "#00CC96"}
                )
                st.plotly_chart(fig_lga, use_container_width=True)
            else:
                st.info("No data to display for selected filters.")

        with col2:
            if not filtered.empty and 'latitude' in filtered.columns and 'longitude' in filtered.columns:
                fig_map = px.density_mapbox(
                    filtered.dropna(subset=['latitude', 'longitude']),
                    lat='latitude',
                    lon='longitude',
                    radius=10,
                    center=dict(lat=6.5244, lon=3.3792),
                    zoom=9.5,
                    mapbox_style="carto-positron",
                    title="Crime Density Map"
                )
                st.plotly_chart(fig_map, use_container_width=True)

    # ---------- TAB 2: Time ----------
    with tab2:
        st.subheader("📅 Crimes by Time")

        col1, col2 = st.columns(2)

        with col1:
            if not filtered.empty:
                trend_data = filtered['date'].value_counts().sort_index()
                fig_trend = px.line(
                    x=trend_data.index,
                    y=trend_data.values,
                    title="Daily Crime Trend",
                    labels={'x': 'Date', 'y': 'Crime Count'},
                    markers=True
                )
                st.plotly_chart(fig_trend, use_container_width=True)

        with col2:
            if not filtered.empty:
                hour_data = filtered['hour'].value_counts().sort_index()
                fig_hour = px.bar(
                    x=hour_data.index,
                    y=hour_data.values,
                    title="Crimes by Hour of Day",
                    labels={'x': 'Hour', 'y': 'Crime Count'}
                )
                st.plotly_chart(fig_hour, use_container_width=True)

    # ---------- TAB 3: Heatmap + Pie ----------
    with tab3:
        st.subheader("🌡️ Weekly Crime Heatmap")

        if 'day_of_week' in filtered.columns and 'hour' in filtered.columns:
            heatmap_data = pd.pivot_table(
                filtered,
                values='crime_type',
                index='day_of_week',
                columns='hour',
                aggfunc='count',
                fill_value=0
            )

            # Sort days for clarity
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = heatmap_data.reindex(day_order)

            fig, ax = plt.subplots(figsize=(12, 5))
            sns.heatmap(heatmap_data, cmap="YlOrRd", linewidths=0.5, ax=ax)
            ax.set_title("Crime Frequency by Day and Hour")
            st.pyplot(fig)

        st.markdown("### 🔄 Severity Distribution")
        if not filtered.empty:
            fig_pie = px.pie(
                filtered,
                names='severity',
                title='Crime Severity Distribution',
                color='severity',
                color_discrete_map={"High": "#EF553B", "Medium": "#636EFA", "Low": "#00CC96"}
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # ---------- Footer ----------
    st.markdown("---")
    st.markdown(f"""
    ℹ️ **About This Dashboard**  
    - Data is synthetic and used for demonstration only  
    - Last update: **{datetime.now().strftime("%Y-%m-%d %H:%M")}**
    """)

# Optional direct run
if __name__ == "__main__":
    show_visualizations()
