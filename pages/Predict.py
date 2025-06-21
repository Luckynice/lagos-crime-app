import streamlit as st
import pandas as pd
import joblib
import numpy as np
from geopy.geocoders import Nominatim
from datetime import datetime
import holidays
from pymongo import MongoClient
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import plotly.express as px
import json

# --- Config ---
st.set_page_config(page_title="Lagos Crime Predictor", page_icon="🔮", layout="wide")

# --- Auth Check ---
if "user_email" not in st.session_state:
    st.warning("🚫 Please log in first.")
    st.switch_page("pages/Login.py")

# --- Safe Dict Parser ---
def safe_parse_features(features):
    if isinstance(features, str):
        try:
            return json.loads(features)
        except json.JSONDecodeError:
            return {}
    elif isinstance(features, dict):
        return features
    return {}

# --- Load Model ---
@st.cache_resource
def load_model():
    return joblib.load("models/crime_model.pkl")

# --- Database ---
@st.cache_resource
def get_db():
    client = MongoClient("mongodb+srv://luckynice02:Olaronke%402024%2B1@cluster-lagos-crime-pre.qqduxyz.mongodb.net/?retryWrites=true&w=majority")
    return client["lagos_crime"]["predictions"]

# --- PDF Report ---
def export_to_pdf(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(50, 750, "🔮 Lagos Crime Prediction Report")
    c.drawString(50, 730, f"Prediction: {data['top_predictions'][0]['crime_type']}")
    c.drawString(50, 710, f"User: {data.get('user_email')}")
    c.drawString(50, 690, f"Location: {data.get('location')}")
    c.drawString(50, 670, f"Date: {data.get('timestamp')}")

    c.drawString(50, 640, "📊 Features:")
    y = 620
    features = data.get("features", {})
    if isinstance(features, str):
        try:
            features = json.loads(features)
        except:
            features = {}

    if isinstance(features, dict):
        for k, v in features.items():
            c.drawString(60, y, f"{k}: {v}")
            y -= 15

    c.save()
    buffer.seek(0)
    return buffer

# --- Time Period Helper ---
def get_time_period(hour):
    if hour < 12: return "Morning"
    elif hour < 17: return "Afternoon"
    elif hour < 20: return "Evening"
    return "Night"

# --- Main App ---
def main():
    st.title("🔮 Lagos Crime Predictor")
    st.markdown("Predict likely crime types based on location and conditions.")

    model = load_model()
    db = get_db()
    geolocator = Nominatim(user_agent="lagos-crime-app")
    ng_holidays = holidays.Nigeria()

    # --- Form Inputs ---
    with st.form("prediction_form"):
        st.subheader("📍 Enter Details")
        location = st.text_input("Location (e.g. Ikeja Under Bridge)")
        date = st.date_input("Date", datetime.today())
        time = st.time_input("Time", datetime.now().time())
        weather = st.selectbox("Weather", ["Clear", "Rainy", "Cloudy", "Sunny", "Stormy"])
        lga = st.text_input("LGA", "Ikeja")

        submitted = st.form_submit_button("🔮 Predict")

    # --- Handle Submission ---
    if submitted:
        try:
            dt = datetime.combine(date, time)
            hour = dt.hour
            geo = geolocator.geocode(f"{location}, Lagos, Nigeria")

            input_data = {
                "location": location,
                "lga": lga,
                "latitude": geo.latitude if geo else 6.5244,
                "longitude": geo.longitude if geo else 3.3792,
                "weather_condition": weather,
                "is_holiday": int(dt.date() in ng_holidays),
                "time_period": get_time_period(hour),
                "day_of_week": dt.strftime('%A'),
                "hour": hour,
                "month": dt.month
            }

            # Debug: Check input types
            st.write("🧪 Prediction Input Preview")
            st.json(input_data)
            st.write("Types:", {k: str(type(v)) for k, v in input_data.items()})

            # Predict
            pipeline = model
            proba = pipeline.predict_proba([input_data])[0]
            top_n = sorted(zip(pipeline.classes_, proba), key=lambda x: x[1], reverse=True)[:3]

            top_predictions = [
                {"crime_type": crime, "confidence": round(conf, 4)}
                for crime, conf in top_n
            ]

            result = {
                "user_email": st.session_state.get("user_email"),
                "location": location,
                "lga": lga,
                "top_predictions": top_predictions,
                "most_likely": top_predictions[0]["crime_type"],
                "features": input_data,
                "timestamp": datetime.now().isoformat(),
                "model_version": "1.0"
            }

            db.insert_one(result)

            st.session_state["last_result"] = {
                "result": result,
                "plot_df": pd.DataFrame(top_predictions),
                "pdf": export_to_pdf(result)
            }

            st.success("✅ Prediction successful!")

        except Exception as e:
            st.session_state["last_result"] = None
            st.error(f"❌ Prediction failed: {str(e)}")

    # --- Display Results ---
    if "last_result" in st.session_state and st.session_state["last_result"]:
        res = st.session_state["last_result"]
        st.success(f"🚨 Most Likely Crime: **{res['result']['most_likely']}**")
        st.plotly_chart(px.bar(res["plot_df"], x="crime_type", y="confidence", color="crime_type"))

        st.download_button(
            "📄 Download Report",
            data=res["pdf"],
            file_name="crime_prediction.pdf",
            mime="application/pdf"
        )

# --- Run App ---
if __name__ == "__main__":
    main()
