import streamlit as st
import pandas as pd
import joblib
from geopy.geocoders import Nominatim
from datetime import datetime
import holidays

def show_predictor():
    st.title("🔮 Lagos Crime Risk Predictor")
    st.markdown("Predict likely crime types based on location, time, and weather.")

    # Load model and encoder
    @st.cache_resource
    def load_model():
        return joblib.load("models/crime_model.pkl")  # (model, label_encoder)

    model, label_encoder = load_model()
    geolocator = Nominatim(user_agent="lagos-crime-app")

    # Initialize prediction history in session
    if "history" not in st.session_state:
        st.session_state.history = []

    def get_time_period(hour):
        if 0 <= hour < 6: return "Early Morning"
        elif 6 <= hour < 12: return "Morning"
        elif 12 <= hour < 18: return "Afternoon"
        return "Evening"

    def get_lga_from_location(location):
        keywords = {
            "ikeja": "Ikeja", "lekki": "Eti-Osa", "oshodi": "Oshodi-Isolo",
            "ajegunle": "Ajeromi-Ifelodun", "yaba": "Mainland", "surulere": "Surulere",
            "ikorodu": "Ikorodu", "epe": "Epe", "ajah": "Eti-Osa", "agege": "Agege",
        }
        location_lower = location.lower()
        for key in keywords:
            if key in location_lower:
                return keywords[key]
        return "Unknown"

    ng_holidays = holidays.CountryHoliday("NG")

    # --- UI: Prediction Form ---
    with st.form("prediction_form"):
        st.subheader("📍 Enter Crime Report Details")
        location = st.text_input("Location (e.g., Ikeja Under Bridge)")
        date = st.date_input("Date of Crime", value=datetime.today())
        time = st.time_input("Time of Crime", value=datetime.now().time())
        weather = st.selectbox("Weather Condition", ["Sunny", "Rainy", "Cloudy", "Harmattan"])
        submitted = st.form_submit_button("Predict Crime Type")

        if submitted and location:
            try:
                geo = geolocator.geocode(f"{location}, Lagos, Nigeria")
                if not geo:
                    st.warning("📍 Location not found. Try being more specific.")
                else:
                    latitude = geo.latitude
                    longitude = geo.longitude
                    hour = time.hour
                    day_of_week = date.strftime('%A')
                    is_holiday = int(date in ng_holidays)
                    time_period = get_time_period(hour)
                    lga = get_lga_from_location(location)

                    def encode_or_zero(val):
                        return label_encoder.transform([val])[0] if val in label_encoder.classes_ else 0

                    input_features = pd.DataFrame([{
                        'location': encode_or_zero(location),
                        'lga': encode_or_zero(lga),
                        'latitude': latitude,
                        'longitude': longitude,
                        'weather_condition': encode_or_zero(weather),
                        'is_holiday': is_holiday,
                        'time_period': encode_or_zero(time_period),
                        'day_of_week': encode_or_zero(day_of_week),
                    }])

                    prediction = model.predict(input_features)[0]
                    crime_predicted = label_encoder.inverse_transform([prediction])[0]

                    st.success(f"🚨 Predicted Crime Type: **{crime_predicted}**")

                    # ✅ Save to session state (local history)
                    prediction_record = {
                        "location": location,
                        "datetime": datetime.combine(date, time),
                        "lga": lga,
                        "latitude": latitude,
                        "longitude": longitude,
                        "weather_condition": weather,
                        "is_holiday": bool(is_holiday),
                        "time_period": time_period,
                        "day_of_week": day_of_week,
                        "predicted_crime": crime_predicted,
                    }
                    st.session_state.history.insert(0, prediction_record)

            except Exception as e:
                st.error(f"Prediction failed: {e}")

    # --- Show Recent History ---
    if st.session_state.history:
        st.markdown("### 🕘 Recent Predictions")
        history_df = pd.DataFrame(st.session_state.history)
        history_df["datetime"] = pd.to_datetime(history_df["datetime"])
        st.dataframe(history_df.head(10), use_container_width=True)

    st.markdown("""---  
This tool uses an AI model trained on historical crime data in Lagos to predict likely crime types based on real-world context.
""")
