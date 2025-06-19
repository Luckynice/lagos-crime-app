# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

# Load data
df = pd.read_csv("data/lagos_crime_data.csv")

# Features and target
features = ['location', 'lga', 'latitude', 'longitude', 'weather_condition', 'is_holiday', 'time_period', 'day_of_week']
target = 'crime_type'

X = df[features]
y = df[target]

# Convert to list of dictionaries for DictVectorizer
X_dict = X.to_dict(orient="records")

# Pipeline: DictVectorizer + RandomForestClassifier
pipeline = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train model
X_train, X_test, y_train, y_test = train_test_split(X_dict, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# Save pipeline model
joblib.dump(pipeline, "models/crime_model.pkl")

print("✅ Model retrained and saved to 'models/crime_model.pkl'")
