import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import json

# ✅ Safely parse features (dict or JSON string)
def safe_parse_features(features):
    if isinstance(features, str):
        try:
            return json.loads(features)
        except json.JSONDecodeError:
            st.error(f"❌ Failed to decode features: {features}")
            return {}
    elif isinstance(features, dict):
        return features
    return {}  # Return empty dict if not a string or dict

@st.cache_resource
def get_db():
    uri = "mongodb+srv://luckynice02:Olaronke%402024%2B1@cluster-lagos-crime-pre.qqduxyz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-Lagos-Crime-Predict"
    client = MongoClient(uri)
    db = client["lagos_crime"]
    return db["predictions"]

def export_prediction_to_pdf(prediction):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(50, 750, "Lagos Crime Prediction Report")
    c.drawString(50, 730, f"Prediction: {prediction.get('crime_type', '')}")
    c.drawString(50, 710, f"LGA: {prediction.get('lga', '')}")
    c.drawString(50, 690, f"Date: {prediction.get('timestamp', '')}")

    c.drawString(50, 660, "Features:")
    y = 640
    features = safe_parse_features(prediction.get("processed_features", {}))
    for k, v in features.items():
        c.drawString(60, y, f"{k}: {v}")
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer

def show_user_profile():
    st.title("👤 My Profile & History")

    user_email = st.session_state.get("user_email")
    if not user_email:
        st.warning("⚠️ Please log in to view your profile.")
        return

    col = get_db()
    data = list(col.find({"user_email": user_email}))

    if not data:
        st.info("No predictions found for your account.")
        return

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df.get("timestamp"), errors="coerce")

    # Debugging: Check the types of `processed_features`
    if "processed_features" in df.columns:
        st.write("Types of processed_features in your data:")
        st.write(df["processed_features"].apply(type))

    if "predicted_crime" in df.columns:
        df["crime_type"] = df["predicted_crime"]
    elif "prediction" in df.columns:
        df["crime_type"] = df["prediction"]
    else:
        df["crime_type"] = "Unknown"

    st.write(f"Found **{len(df)}** predictions for: `{user_email}`")
    df = df.sort_values(by="timestamp", ascending=False)

    st.download_button(
        "⬇️ Download My Predictions",
        data=df.to_csv(index=False),
        file_name="my_predictions.csv",
        mime="text/csv"
    )

    st.subheader("📈 My Most Frequent Predictions")
    chart_df = df["crime_type"].value_counts().reset_index()
    chart_df.columns = ["Crime Type", "Count"]
    st.plotly_chart(px.bar(chart_df, x="Crime Type", y="Count", color="Crime Type"))

    st.subheader("📂 My Prediction History")
    for i, row in df.iterrows():
        with st.expander(f"🕒 {row.get('timestamp', '')} — {row.get('crime_type', 'Unknown')} @ {row.get('lga', 'N/A')}"):
            st.write("📍 Location:", row.get("location", "N/A"))
            st.write("🧠 Features:")
            features = safe_parse_features(row.get("processed_features", {}))
            st.json(features)

            pdf_buf = export_prediction_to_pdf(row)
            st.download_button(
                "🧾 Download PDF",
                data=pdf_buf,
                file_name=f"prediction_{i}.pdf",
                mime="application/pdf",
                key=f"user_pdf_{i}"
            )

if __name__ == "__main__":
    show_user_profile()
