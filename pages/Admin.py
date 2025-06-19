import streamlit as st
import pandas as pd
import datetime
from pymongo import MongoClient
import plotly.express as px

def show_admin_panel():
    st.title("🔐 Admin Panel")
    st.markdown("Manage prediction logs and analyze crime trends.")

    # Session-based login check
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            username = st.text_input("Admin Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if (
                    username == st.secrets["admin"]["username"]
                    and password == st.secrets["admin"]["password"]
                ):
                    st.session_state.admin_logged_in = True
                    st.success("✅ Login successful.")
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid credentials.")
        return

    # ✅ Admin is logged in
    st.success("✅ Logged in as admin.")
    if st.button("🚪 Logout"):
        st.session_state.admin_logged_in = False
        st.experimental_rerun()

    # 📡 Connect to MongoDB (only after login)
    try:
        client = MongoClient(st.secrets["mongo"]["uri"])
        db = client["lagos_crime"]
        collection = db["predictions"]
    except Exception as e:
        st.error(f"❌ MongoDB connection failed: {e}")
        return

    # 📅 Date Range Filter
    st.markdown("### 📅 Filter Logs by Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.date.today())

    if start_date > end_date:
        st.error("⚠️ Start date must be before end date.")
        return

    query = {
        "timestamp": {
            "$gte": datetime.datetime.combine(start_date, datetime.time.min),
            "$lte": datetime.datetime.combine(end_date, datetime.time.max)
        }
    }

    logs = list(collection.find(query, {"_id": 0}))
    if not logs:
        st.info("No logs found for the selected date range.")
        return

    logs_df = pd.DataFrame(logs)

    # 📋 Display Logs Table
    st.markdown(f"### 📋 Logs ({len(logs_df)} records)")
    st.dataframe(logs_df, use_container_width=True)

    # ⬇️ Download CSV
    csv = logs_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "crime_logs.csv", "text/csv")

    # 📊 Analytics
    st.markdown("### 📊 Analytics")

    col1, col2 = st.columns(2)
    with col1:
        if 'lga' in logs_df.columns:
            top_lgas = logs_df['lga'].value_counts().nlargest(5).reset_index()
            top_lgas.columns = ['LGA', 'Count']
            fig1 = px.bar(top_lgas, x='LGA', y='Count', title="Top LGAs by Predictions")
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if 'predicted_crime_type' in logs_df.columns:
            top_crimes = logs_df['predicted_crime_type'].value_counts().nlargest(5).reset_index()
            top_crimes.columns = ['Crime Type', 'Count']
            fig2 = px.pie(top_crimes, names='Crime Type', values='Count', title="Crime Type Distribution")
            st.plotly_chart(fig2, use_container_width=True)

    # 📈 Trend Line
    if 'timestamp' in logs_df.columns:
        logs_df['date'] = pd.to_datetime(logs_df['timestamp']).dt.date
        trend = logs_df.groupby('date').size().reset_index(name='Count')
        fig3 = px.line(trend, x='date', y='Count', title="Prediction Trend Over Time", markers=True)
        st.plotly_chart(fig3, use_container_width=True)

    # 🔥 Heatmap: Day vs Hour
    if 'hour' in logs_df.columns and 'day_of_week' in logs_df.columns:
        st.markdown("### 🔥 Prediction Heatmap (Day vs Hour)")
        heatmap_df = logs_df.copy()
        heatmap_df['hour'] = pd.to_numeric(heatmap_df['hour'], errors='coerce').fillna(0).astype(int)
        heatmap_df['day_of_week'] = heatmap_df['day_of_week'].astype(str)

        pivot = pd.pivot_table(
            heatmap_df,
            values='predicted_crime_type',
            index='day_of_week',
            columns='hour',
            aggfunc='count',
            fill_value=0
        )

        fig4 = px.imshow(
            pivot,
            labels=dict(x="Hour", y="Day of Week", color="Predictions"),
            title="Heatmap of Predictions by Hour and Day"
        )
        st.plotly_chart(fig4, use_container_width=True)
