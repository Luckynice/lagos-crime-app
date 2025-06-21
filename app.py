import streamlit as st
import pandas as pd
import joblib
import numpy as np
from geopy.geocoders import Nominatim
from datetime import datetime
import holidays
from pymongo import MongoClient
import plotly.express as px

# --- Configuration ---
st.set_page_config(page_title="Lagos Crime Predictor", page_icon="🔮", layout="wide")

# --- Authentication Check ---
if "user" not in st.session_state or not st.session_state.user:
    st.warning("🚫 Please log in to access this page")
    st.switch_page("pages/Login.py")

# --- Model Loading ---
@st.cache_resource
def load_model():
    try:
        model = joblib.load("models/crime_model.pkl")
        if isinstance(model, tuple):  # Handle if accidentally saved as tuple
            model = model[0]
        return model
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        st.stop()

# --- Data Processing ---
def prepare_input(location, date, time, weather, lga, ng_holidays, geo):
    """Convert user input to model-ready format"""
    hour = time.hour
    return {
        'location': str(location),
        'lga': str(lga),
        'latitude': float(geo.latitude) if geo else 0.0,
        'longitude': float(geo.longitude) if geo else 0.0,
        'weather_condition': str(weather),
        'is_holiday': int(date in ng_holidays),
        'time_period': get_time_period(hour),
        'day_of_week': date.strftime('%A'),
        'hour': hour
    }

def get_time_period(hour):
    if hour < 12: return "Morning"
    elif hour < 17: return "Afternoon"
    elif hour < 20: return "Evening"
    return "Night"

# --- Main App ---
def main():
    st.title("🔮 Lagos Crime Risk Predictor")
    st.markdown("Predict likely crime types based on location and conditions")

    # Initialize services
    model = load_model()
    geolocator = Nominatim(user_agent="crime-app")
    ng_holidays = holidays.Nigeria()

    with st.form("prediction_form"):
        st.subheader("📍 Enter Details")
        location = st.text_input("Location (e.g. Ikeja Under Bridge)")
        date = st.date_input("Date", datetime.today())
        time = st.time_input("Time", datetime.now().time())
        weather = st.selectbox("Weather", ["Clear", "Rainy", "Cloudy", "Sunny", "Stormy"])
        
        if st.form_submit_button("Predict"):
            try:
                # Geocode location
                geo = geolocator.geocode(f"{location}, Lagos, Nigeria") if location else None
                
                if not geo:
                    st.warning("Location not found. Using default coordinates")
                
                # Prepare input data
                input_data = prepare_input(
                    location=location,
                    date=date,
                    time=time,
                    weather=weather,
                    lga="Unknown",  # You should add LGA detection logic
                    ng_holidays=ng_holidays,
                    geo=geo
                )
                
                # Convert to DataFrame for the model
                input_df = pd.DataFrame([input_data])
                
                # Make prediction
                prediction = model.predict(input_df)[0]
                st.success(f"🚨 Predicted Crime Type: **{prediction}**")
                
                # Store in session
                st.session_state.last_prediction = {
                    **input_data,
                    "prediction": prediction,
                    "timestamp": datetime.now()
                }
                
            except Exception as e:
                st.error(f"❌ Prediction failed: {str(e)}")

if __name__ == "__main__":
    main()