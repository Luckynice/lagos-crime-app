import streamlit as st
from pages.Home import show_home
from pages.Visualizations import show_visualizations
from pages.Map import show_crime_map
from pages.Predict import show_predictor
from pages.Admin import show_admin_panel
from pages.About import show_about

st.set_page_config(page_title="Lagos Crime Predictor", layout="wide")

st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to", (
    "🏠 Home",
    "📊 Visualizations",
    "🗺️ Crime Map",
    "🤖 Predict Crime",
    "🔐 Admin Panel",
    "ℹ️ About"
))

if page == "🏠 Home":
    show_home()
elif page == "📊 Visualizations":
    show_visualizations()
elif page == "🗺️ Crime Map":
    show_crime_map()
elif page == "🤖 Predict Crime":
    show_predictor()
elif page == "🔐 Admin Panel":
    show_admin_panel()
elif page == "ℹ️ About":
    show_about()
