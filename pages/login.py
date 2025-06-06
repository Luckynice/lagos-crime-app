# pages/login.py
import streamlit as st

# Hardcoded users for demo purposes
USERS = {
    "admin": "admin123",
    "analyst": "lagoscrime"
}

def login():
    st.title("🔐 Login to Lagos Crime Predictor")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success(f"Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    st.switch_page("pages/dashboard.py")


# pages/dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import base64

@st.cache_data
def load_data():
    return pd.read_csv("data/lagos_crime_data.csv")

@st.cache_resource
def load_model():
    return joblib.load("models/crime_model.pkl")

data = load_data()
model = load_model()

st.set_page_config(page_title="Lagos Crime Predictor Dashboard", layout="wide")
st.title("📊 Lagos Crime Dashboard")

# Filters
st.sidebar.header("Filter Data")
lga_filter = st.sidebar.multiselect("Select LGA", data["lga"].unique(), default=data["lga"].unique())
crime_filter = st.sidebar.multiselect("Select Crime Type", data["crime_type"].unique(), default=data["crime_type"].unique())
filtered = data[(data["lga"].isin(lga_filter)) & (data["crime_type"].isin(crime_filter))]

# Charts
col1, col2 = st.columns(2)
with col1:
    fig1 = px.histogram(filtered, x="lga", color="crime_type", title="Crime Count by LGA", barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    trend = filtered['date'].value_counts().sort_index()
    fig2 = px.line(x=trend.index, y=trend.values, labels={'x': 'Date', 'y': 'Reported Crimes'}, title="Crime Trend")
    st.plotly_chart(fig2, use_container_width=True)

# Heatmap
st.subheader("🔥 Weekly Crime Heatmap")
heat = filtered.copy()
heat['date'] = pd.to_datetime(heat['date'])
heat['Day'] = heat['date'].dt.day_name()
heat['Hour'] = heat['hour']
pivot = pd.pivot_table(heat, values='crime_type', index='Day', columns='Hour', aggfunc='count', fill_value=0)
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, cmap='YlOrRd')
st.pyplot(plt)

# Map
st.subheader("🗺️ Crime Map")
map_fig = px.scatter_mapbox(filtered, lat="latitude", lon="longitude", color="crime_type", zoom=9,
                            mapbox_style="open-street-map", title="Crime Occurrence Map")
st.plotly_chart(map_fig, use_container_width=True)

# Download Data
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")
csv = convert_df(filtered)
st.download_button("Download Filtered Dataset", csv, "filtered_lagos_crime.csv", "text/csv")

# Prediction
st.subheader("🔍 Predict Crime Type")
with st.form("predict_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        hour = st.slider("Hour", 0, 23, 12)
    with c2:
        lga = st.selectbox("LGA", data["lga"].unique())
    with c3:
        location = st.text_input("Street (Optional)", "Allen Avenue")

    if st.form_submit_button("Predict"):
        input_data = pd.DataFrame([[hour, lga, location]], columns=["hour", "lga", "location"])
        result = model.predict(input_data)[0]
        st.success(f"Predicted Crime Type: {result}")

        pred_df = input_data.copy()
        pred_df['predicted_crime_type'] = result
        pred_csv = pred_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Prediction Result", pred_csv, "prediction_result.csv", "text/csv")


# main app.py to serve as entry point
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Lagos Crime Predictor", layout="centered")

st.markdown("""
# 🚨 Welcome to the Lagos Crime Prediction System

This app helps visualize, analyze, and predict crime incidents in Lagos using historic data.

**Please login from the sidebar to access the dashboard.**

> Built with ❤️ using Streamlit, Scikit-Learn, and Plotly
""")
