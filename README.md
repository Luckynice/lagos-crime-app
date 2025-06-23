# lagos-crime-app
# 🔍 Lagos Crime Prediction & Analysis App

This is a machine learning-powered web app for predicting and analyzing crime patterns in Lagos, Nigeria. Built using Python, Streamlit, and Plotly, the app allows users to explore historical crime data, visualize trends, and predict likely crimes based on location and time.

## 🚀 Features

- 📊 Crime distribution charts by LGA and date
- 🗺️ Interactive map showing crime hotspots
- 🔥 Weekly heatmap of crime frequency
- 📁 Downloadable filtered dataset
- 🤖 Predict crime type based on hour and LGA
- ✅ Professional UI/UX design
- 🧠 Built with machine learning (Random Forest)
- 🔒 Simple login screen (for project access control)

## 🧪 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Scikit-learn, Pandas, Plotly, Seaborn
- **Data**: Synthetic + Real Lagos crime data
- **Model**: Random Forest Classifier
- **Deployment**: Streamlit Local (can later be hosted on Streamlit Cloud or Hugging Face Spaces)


## 🧠 How It Works

1. Load dataset and ML model.
2. Filter data by crime type and LGA.
3. Show visual charts, heatmaps, and crime map.
4. Allow user to input time and LGA to predict most likely crime.
5. Users can download filtered data or prediction results.

## 🧑‍💻 Local Deployment (For Project Defense)

1. Clone this repo:
   ```bash
   git clone https://github.com/Luckynice/lagos-crime-app.git
   cd lagos-crime-app


📍 Lagos Crime Predictor

An AI-powered web app to predict, visualize, and manage crime trends in Lagos, Nigeria. Built with Streamlit, scikit-learn, MongoDB Atlas, and Plotly.

🚀 Features

🔐 User Authentication

Secure login & registration with hashed passwords

Role-based access for admin and user

🤖 Crime Prediction

Input: location, time, date, weather, LGA

Output: most likely crime + top 3 predictions with confidence scores

Location geocoding via OpenStreetMap

Holiday recognition using Nigeria's holiday calendar

Predictions stored in MongoDB

📊 Visualizations

Crime trends by time, date, weather, LGA

Interactive bar charts & pie charts

🗺️ Crime Map

Density map of all recorded predictions using Plotly Mapbox

👤 User Dashboard

View your own predictions

Delete or download them as PDFs

🧑‍💼 Admin Panel

View all users' predictions

Filter by user email

Delete or impersonate users

Admin-only access

📁 Project Structure

new_lagos_crime_predictor/
├── App.py                   # Main router
├── auth.py                 # Login/register backend
├── train_model.py          # ML model training
├── models/
│   └── crime_model.pkl     # Saved classifier
├── pages/
│   ├── Login.py            # Login and registration
│   ├── Predict.py          # Prediction form
│   ├── Admin.py            # Admin dashboard
│   ├── Profile.py          # User dashboard
│   ├── Visualizations.py   # Charts
│   ├── Map.py              # Crime density map
│   └── Home.py             # Landing page
├── data/
│   └── lagos_crime_data.csv

☁️ Deployment Instructions

✅ Prerequisites

Python 3.9+

MongoDB Atlas Cluster with a users and predictions collection

📦 Install dependencies

pip install -r requirements.txt

🔐 Environment Variables

Edit auth.py and replace MONGO_URI with your Atlas URI.

🧠 Train the model

python train_model.py

🚀 Run the app

streamlit run App.py

App will run at: http://localhost:8501

📌 Feature Roadmap

✅ Completed



🧪 In Progress / Future



🤝 Authors

Lucky Osehi

📃 License

MIT License - use freely for educational/non-commercial projects.

