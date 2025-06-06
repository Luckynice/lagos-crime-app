# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import datetime

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/lagos_crime_data.csv")
    return df

# Load model
@st.cache_resource
def load_model():
    return joblib.load("models/crime_model.pkl")

data = load_data()
model = load_model()

st.set_page_config(page_title="Lagos Crime Predictor", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
        color: #333;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
    }
    .stDownloadButton>button {
        background-color: #28a745;
        color: white;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Lagos Crime Prediction & Intelligence Dashboard")
st.markdown("""
**Explore, understand, and predict crime patterns in Lagos using interactive maps, visualizations, and machine learning.**
""")

# ----- Sidebar Filters -----
st.sidebar.header("📊 Filter Crime Data")
filter_lga = st.sidebar.multiselect("Select LGA(s)", options=data['lga'].unique(), default=data['lga'].unique())
filter_crime = st.sidebar.multiselect("Select Crime Type(s)", options=data['crime_type'].unique(), default=data['crime_type'].unique())
filtered_data = data[(data['lga'].isin(filter_lga)) & (data['crime_type'].isin(filter_crime))]

# ----- Charts Section -----
st.markdown("## 📈 Crime Analysis Dashboard")
col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(filtered_data, x="lga", color="crime_type", title="📍 Crime Count by LGA", barmode='group',
                       color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    crime_trend = filtered_data['date'].value_counts().sort_index()
    fig2 = px.line(x=crime_trend.index, y=crime_trend.values,
                   labels={'x': 'Date', 'y': 'Reported Crimes'},
                   title="📆 Daily Crime Trend",
                   markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# ----- Heatmap -----
st.markdown("## 🔥 Weekly Crime Heatmap")
heatmap_data = filtered_data.copy()
heatmap_data['date'] = pd.to_datetime(heatmap_data['date'])
heatmap_data['Day'] = heatmap_data['date'].dt.day_name()
heatmap_data['Hour'] = heatmap_data['hour']
pivot = pd.pivot_table(heatmap_data, values='crime_type', index='Day', columns='Hour', aggfunc='count', fill_value=0)
fig3, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot, cmap="YlOrRd", ax=ax)
st.pyplot(fig3)

# ----- Map -----
st.markdown("## 🗺️ Lagos Crime Map")
map_fig = px.scatter_mapbox(filtered_data, lat="latitude", lon="longitude", color="crime_type", size_max=15, zoom=10,
                            mapbox_style="carto-positron", title="📍 Crime Locations Map",
                            color_discrete_sequence=px.colors.qualitative.Vivid)
st.plotly_chart(map_fig, use_container_width=True)

# ----- Download Dataset -----
st.markdown("## 📥 Download Filtered Dataset")
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')
csv = convert_df(filtered_data)
st.download_button("⬇️ Download CSV", csv, "filtered_lagos_crime.csv", "text/csv")

# ----- Prediction Section -----
st.markdown("## 🤖 Predict Crime Type")
with st.form("predict_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        hour = st.slider("Hour of Day", 0, 23, 12)
    with col2:
        lga = st.selectbox("LGA", data['lga'].unique())
    with col3:
        location = st.text_input("Location (Optional)", "Ikeja")

    submitted = st.form_submit_button("🔮 Predict Crime")
    if submitted:
        input_data = pd.DataFrame([[hour, lga, location]], columns=["hour", "lga", "location"])
        prediction = model.predict(input_data)[0]
        st.success(f"✅ Predicted Crime Type: **{prediction}**")

        # Export prediction
        prediction_df = input_data.copy()
        prediction_df['predicted_crime_type'] = prediction
        pred_csv = prediction_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Prediction", pred_csv, "crime_prediction.csv", "text/csv")

# ----- Footer -----
st.markdown("""
---
Created with ❤️ for smart security planning in Lagos.
Want to contribute real crime data or deploy this system? Contact us for collaboration.
""")
# ----- End of app.py -----
# Add a footer with contact information