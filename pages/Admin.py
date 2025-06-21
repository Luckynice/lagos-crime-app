import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
from bson.objectid import ObjectId
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import json

# --- Safe feature parser ---
def safe_parse_features(features):
    if isinstance(features, str):
        try:
            return json.loads(features)
        except json.JSONDecodeError:
            return {}
    elif isinstance(features, dict):
        return features
    return {}

# --- MongoDB connection ---
@st.cache_resource
def get_db():
    uri = "mongodb+srv://luckynice02:Olaronke%402024%2B1@cluster-lagos-crime-pre.qqduxyz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-Lagos-Crime-Predict"
    client = MongoClient(uri)
    db = client["lagos_crime"]
    return db["predictions"]

# --- PDF Export ---
def export_prediction_to_pdf(prediction):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(50, 750, "Lagos Crime Prediction Report")
    c.drawString(50, 730, f"Prediction: {prediction.get('crime_type', '')}")
    c.drawString(50, 710, f"User: {prediction.get('user_email', '')}")
    c.drawString(50, 690, f"LGA: {prediction.get('lga', '')}")
    c.drawString(50, 670, f"Date: {prediction.get('timestamp', '')}")

    c.drawString(50, 640, "Features:")
    y = 620
    features = safe_parse_features(prediction.get("processed_features", {}))
    for k, v in features.items():
        c.drawString(60, y, f"{k}: {v}")
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer

# --- Admin Dashboard ---
def show_admin_dashboard():
    st.title("🛡️ Admin Dashboard")

    if st.session_state.get("role") != "admin":
        st.warning("🚫 Access denied. Admins only.")
        return

    try:
        col = get_db()
        data = list(col.find())

        if not data:
            st.info("No predictions found.")
            return

        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df.get("timestamp"), errors='coerce')

        # Set crime_type
        if "predicted_crime" in df.columns:
            df["crime_type"] = df["predicted_crime"]
        elif "prediction" in df.columns:
            df["crime_type"] = df["prediction"]
        else:
            df["crime_type"] = "Unknown"

        df["user_email"] = df.get("user_email", "anonymous").fillna("anonymous")

        st.subheader("📊 Overview")
        st.write(f"Total Predictions: **{len(df)}**")

        with st.expander("🔍 Filter"):
            email_filter = st.text_input("Filter by Email")
            lga_filter = st.text_input("Filter by LGA")
            crime_filter = st.text_input("Filter by Crime Type")

            if email_filter:
                df = df[df["user_email"].str.contains(email_filter, case=False, na=False)]
            if lga_filter:
                df = df[df["lga"].astype(str).str.contains(lga_filter, case=False, na=False)]
            if crime_filter:
                df = df[df["crime_type"].astype(str).str.contains(crime_filter, case=False, na=False)]

        st.subheader("🧑‍💼 Impersonate a User")
        users = df["user_email"].dropna().unique().tolist()
        selected_user = st.selectbox("Choose User", ["All Users"] + users)
        if selected_user != "All Users":
            df = df[df["user_email"] == selected_user]

        st.download_button(
            "⬇️ Download CSV", 
            data=df.to_csv(index=False),
            file_name="all_predictions.csv", 
            mime="text/csv"
        )

        st.subheader("📈 Top Crimes")
        crime_counts = df["crime_type"].value_counts().reset_index()
        crime_counts.columns = ["Crime Type", "Count"]
        st.plotly_chart(px.bar(crime_counts, x="Crime Type", y="Count", color="Crime Type"))

        st.subheader("📂 All Predictions")
        for i, row in df.iterrows():
            with st.expander(f"📌 {row.get('timestamp', '')} — {row.get('crime_type')} @ {row.get('lga', 'N/A')}"):
                st.write("👤 User:", row.get("user_email"))
                st.write("📍 Location:", row.get("location", "N/A"))

                features = safe_parse_features(row.get("processed_features", {}))
                st.write("🧠 Features:")
                st.json(features)

                pdf_buf = export_prediction_to_pdf(row)
                st.download_button(
                    "🧾 Download PDF", 
                    data=pdf_buf,
                    file_name=f"prediction_{i}.pdf", 
                    mime="application/pdf",
                    key=f"pdf_{i}"
                )

                if st.button(f"❌ Delete Prediction", key=f"delete_{i}"):
                    col.delete_one({"_id": ObjectId(row["_id"])})
                    st.success("✅ Prediction deleted.")
                    st.rerun()

    except Exception as e:
        st.error(f"❌ Database error: {str(e)}")
        st.info("Please verify your MongoDB connection and the format of stored data.")

if __name__ == "__main__":
    show_admin_dashboard()
# This code is part of a Streamlit application for an admin dashboard that allows administrators to view and manage crime predictions.
# It includes features for filtering predictions, impersonating users, downloading data, and exporting reports to PDF.