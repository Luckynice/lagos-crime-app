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

## 📂 Project Structure

new_lagos_crime_predictor/
│
├── app.py # Main Streamlit app
├── data/
│ └── lagos_crime_data.csv
├── models/
│ └── crime_model.pkl
├── requirements.txt
├── generate_data.py # (Optional) Data generator with Faker
├── README.md


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
