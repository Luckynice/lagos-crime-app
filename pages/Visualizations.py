import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

@st.cache_data(ttl=3600)
def load_lagos_crime_data():
    """Load synthetic crime prediction data from CSV"""
    try:
        df = pd.read_csv("data/lagos_crime_data.csv")

        # Parse datetime
        df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
        df['date'] = df['date_time'].dt.date
        df['hour'] = df['date_time'].dt.hour
        df['day_of_week'] = df['date_time'].dt.day_name()

        # Rename 'area' to 'lga' for visualization
        df.rename(columns={'area': 'lga'}, inplace=True)

        # Map severity
        severity_map = {
            "robbery": "High", "assault": "Medium", "theft": "Medium",
            "vandalism": "Low", "burglary": "High", "fraud": "Medium",
            "kidnapping": "High", "murder": "High"
        }
        df['severity'] = df['crime_type'].map(lambda x: severity_map.get(str(x).lower(), "Low"))

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def show_visualizations():
    st.header("📊 Lagos Crime Data Explorer")
    st.markdown("Explore patterns and trends in synthetic Lagos crime prediction data.")

    data = load_lagos_crime_data()
    if data.empty:
        st.warning("No data available.")
        return

    # Sidebar Filters
    with st.sidebar:
        st.header("🔍 Filter Crime Data")

        with st.expander("📍 Location Filters"):
            lgas = sorted(data['lga'].dropna().unique())
            selected_lgas = st.multiselect("Select LGAs", lgas, default=lgas[:5])

        with st.expander("🦹 Crime Type Filters"):
            crimes = sorted(data['crime_type'].dropna().unique())
            selected_crimes = st.multiselect("Select Crime Types", crimes, default=crimes)

        with st.expander("⚠️ Severity Filters"):
            severities = sorted(data['severity'].dropna().unique())
            selected_severity = st.multiselect("Select Severity", severities, default=severities)

        with st.expander("🕒 Time Filters"):
            hour_range = st.slider("Hour Range (24h)", 0, 23, (6, 20))
            if 'date' in data.columns:
                min_date = data['date'].min()
                max_date = data['date'].max()
                date_range = st.date_input("Date Range", [min_date, max_date])

    # Apply Filters
    filtered_data = data[
        (data['lga'].isin(selected_lgas)) &
        (data['crime_type'].isin(selected_crimes)) &
        (data['severity'].isin(selected_severity)) &
        (data['hour'] >= hour_range[0]) &
        (data['hour'] <= hour_range[1])
    ]

    if 'date' in data.columns and len(date_range) == 2:
        filtered_data = filtered_data[
            (filtered_data['date'] >= date_range[0]) &
            (filtered_data['date'] <= date_range[1])
        ]

    st.caption(f"📌 {len(filtered_data)} records match your filters")

    # Tabs for Visualizations
    tab1, tab2, tab3 = st.tabs(["📍 By Location", "📅 By Time", "🌡️ Heatmaps"])

    # ---- TAB 1: Location-based ----
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            if not filtered_data.empty:
                fig_lga = px.histogram(
                    filtered_data,
                    x="lga",
                    color="severity",
                    title="Crimes by LGA (Grouped by Severity)",
                    barmode='group',
                    labels={'count': 'Crime Count'},
                    color_discrete_map={
                        "High": "#EF553B",
                        "Medium": "#636EFA",
                        "Low": "#00CC96"
                    }
                )
                st.plotly_chart(fig_lga, use_container_width=True)

        with col2:
            if not filtered_data.empty:
                fig_map = px.density_mapbox(
                    filtered_data,
                    lat='latitude',
                    lon='longitude',
                    radius=10,
                    center=dict(lat=6.5244, lon=3.3792),
                    zoom=9.5,
                    mapbox_style="stamen-terrain",
                    title="Crime Density Map"
                )
                st.plotly_chart(fig_map, use_container_width=True)

    # ---- TAB 2: Time-based ----
    with tab2:
        if not filtered_data.empty:
            col1, col2 = st.columns(2)

            with col1:
                trend_data = filtered_data['date'].value_counts().sort_index()
                fig_trend = px.line(
                    x=trend_data.index,
                    y=trend_data.values,
                    title="Daily Crime Trend",
                    labels={'x': 'Date', 'y': 'Crime Count'},
                    markers=True
                )
                st.plotly_chart(fig_trend, use_container_width=True)

            with col2:
                hour_data = filtered_data['hour'].value_counts().sort_index()
                fig_hour = px.bar(
                    x=hour_data.index,
                    y=hour_data.values,
                    title="Crimes by Hour of Day",
                    labels={'x': 'Hour', 'y': 'Crime Count'}
                )
                st.plotly_chart(fig_hour, use_container_width=True)

    # ---- TAB 3: Heatmaps & Pie ----
    with tab3:
        st.markdown("### Weekly Crime Patterns")

        if 'day_of_week' in filtered_data.columns and 'hour' in filtered_data.columns:
            pivot = pd.pivot_table(
                filtered_data,
                values='crime_type',
                index='day_of_week',
                columns='hour',
                aggfunc='count',
                fill_value=0
            )
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            pivot = pivot.reindex(days_order)

            if not pivot.empty:
                fig, ax = plt.subplots(figsize=(12, 5))
                sns.heatmap(pivot, cmap="YlOrRd", linewidths=.5, ax=ax)
                ax.set_title("Crime Frequency by Day/Hour")
                st.pyplot(fig)

        st.markdown("### Severity Distribution")
        if not filtered_data.empty:
            fig_pie = px.pie(
                filtered_data,
                names='severity',
                title='Crime Severity Distribution',
                color='severity',
                color_discrete_map={
                    "High": "#EF553B",
                    "Medium": "#636EFA",
                    "Low": "#00CC96"
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    **ℹ️ About This Dashboard**
    - Visualizations based on synthetic predictions in `lagos_crime_data.csv`
    - Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
    """)

