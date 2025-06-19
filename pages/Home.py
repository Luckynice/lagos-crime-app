import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("data/lagos_crime_data.csv")
    df.columns = df.columns.str.strip().str.lower()
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')

    # Assign severity if not already present
    if 'severity' not in df.columns and 'crime_type' in df.columns:
        severity_map = {
            "robbery": "High",
            "assault": "Medium",
            "theft": "Medium",
            "vandalism": "Low",
            "burglary": "High",
            "fraud": "Medium",
            "arson": "High",
            "kidnapping": "High",
            "murder": "High"
        }
        df['severity'] = df['crime_type'].map(lambda x: severity_map.get(str(x).lower(), "Low"))
    
    return df

def show_home():
    df = load_data()

    # Welcome admin
    admin_name = st.session_state.get("user", {}).get("name", "Admin")
    st.markdown(f"## 👋 Welcome, **{admin_name}**")
    st.markdown("Explore, understand, and predict crime patterns in Lagos using interactive maps, analytics, and machine learning.")

    # Banner image
    try:
        st.image("static/Banner.svg", use_container_width=True)
    except:
        st.info("🖼️ You can add a banner at `static/Banner.svg`")

    # Overview stats
    st.markdown("### 📊 Crime Overview")
    total_crimes = len(df)
    total_lgas = df['area'].nunique() if 'area' in df.columns else df['lga'].nunique()
    try:
        date_range = f"{df['date_time'].min().date()} to {df['date_time'].max().date()}"
    except:
        date_range = "Date data unavailable"

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Crimes", f"{total_crimes:,}")
    col2.metric("Areas Covered", f"{total_lgas}")
    col3.metric("Date Range", date_range)

    # Filter section
    st.divider()
    st.markdown("### 🎯 Filter Crime Data for Pie Chart")
    lga_column = 'area' if 'area' in df.columns else 'lga'
    lgas = df[lga_column].dropna().unique().tolist()
    selected_lgas = st.multiselect("Select Area(s)", options=sorted(lgas), default=sorted(lgas))

    severity_options = df['severity'].dropna().unique().tolist() if 'severity' in df.columns else []
    selected_severity = st.multiselect("Select Severity Level(s)", options=sorted(severity_options), default=sorted(severity_options)) if severity_options else []

    filtered_df = df[df[lga_column].isin(selected_lgas)]
    if selected_severity:
        filtered_df = filtered_df[filtered_df['severity'].isin(selected_severity)]

    # Pie chart
    st.markdown("### 🧩 Crime Type Distribution")
    if not filtered_df.empty and 'crime_type' in filtered_df.columns:
        pie_data = filtered_df['crime_type'].value_counts().reset_index()
        pie_data.columns = ['Crime Type', 'Count']
        fig = px.pie(pie_data, values='Count', names='Crime Type', title='Crime Type Breakdown (Filtered)', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data to display. Please adjust your filters or check if `crime_type` exists.")

    # Capabilities
    st.divider()
    st.markdown("### 🚀 What You Can Do")
    st.markdown("""
    - 📊 **Visualize** crime trends across LGAs/LCDAs  
    - 🗺️ **Map** crime hotspots interactively  
    - 🤖 **Predict** potential crime locations  
    - 🔐 **Administer** users & access levels  
    """)

    # Navigation buttons
    st.markdown("### 🔗 Quick Navigation")
    colA, colB, colC = st.columns(3)
    with colA:
        if st.button("🗺️ View Crime Map"):
            st.switch_page("pages/Map.py")
    with colB:
        if st.button("🔮 Launch Predictor"):
            st.switch_page("pages/Predict.py")
    with colC:
        if st.button("📊 Open Visualizations"):
            st.switch_page("pages/Visualizations.py")

    colX, colY = st.columns(2)
    with colX:
        if st.button("ℹ️ About"):
            st.switch_page("pages/About.py")
    with colY:
        if st.button("🛠️ Admin Panel"):
            st.switch_page("pages/Admin.py")

    # Footer
    st.markdown("---")
    st.caption("Built with ❤️ by Lucky Osehi | Powered by Streamlit & Python")
    st.markdown("For issues or suggestions, please contact the admin.")
    st.markdown("### 📞 Contact: [Luckynize24@gmail.com](mailto:Luckynize24@gmail.com)")
    st.markdown("### 📄 License: [MIT License](https://opensource.org/license/mit/)")
# This code is part of the Streamlit app for the Lagos Crime Data Analysis project.
# It provides the home page functionality, including data loading, overview statistics,