# train_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib
import holidays
from datetime import datetime
import os

# Configuration
MODEL_PATH = "models/crime_model.pkl"
DATA_PATH = "data/lagos_crime_data.csv"

def load_and_preprocess_data():
    """Load and prepare the crime dataset with proper type conversion"""
    df = pd.read_csv(DATA_PATH)

    # Standardize column names and types
    df.columns = df.columns.str.lower()

    # Ensure required columns exist
    required_cols = ['crime_type', 'location', 'lga', 'latitude', 'longitude',
                     'weather_condition', 'time_period', 'day_of_week']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Convert to datetime
    if 'date_time' not in df.columns and 'date' in df.columns:
        df['date_time'] = df['date']
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')

    # Detect holidays
    df['is_holiday'] = df['date_time'].apply(
        lambda x: int(x.date() in holidays.Nigeria()) if pd.notnull(x) else 0
    )

    # Ensure numerical fields are properly typed
    for col in ['latitude', 'longitude']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with missing critical data
    df = df.dropna(subset=['crime_type', 'latitude', 'longitude'])

    return df

def build_feature_pipeline():
    """Create preprocessing and modeling pipeline"""
    return Pipeline([
        ('vectorizer', DictVectorizer(sparse=False)),
        ('classifier', RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            min_samples_leaf=2,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        ))
    ])

def verify_model_format(model):
    """Ensure the model can handle prediction inputs"""
    test_input = pd.DataFrame([{
        'location': 'Test Location',
        'lga': 'Ikeja',
        'latitude': 6.5244,
        'longitude': 3.3792,
        'weather_condition': 'Clear',
        'is_holiday': 0,
        'time_period': 'Morning',
        'day_of_week': 'Monday'
    }])

    try:
        # Convert to dictionary records
        test_dict = test_input.to_dict(orient='records')
        prediction = model.predict(test_dict)
        print(f"✅ Model verification passed. Test prediction: {prediction[0]}")
    except Exception as e:
        print(f"❌ Model verification failed: {str(e)}")
        raise

def main():
    print("🚀 Starting model training process...")

    try:
        # 1. Load and prepare data
        print("📊 Loading and preprocessing data...")
        df = load_and_preprocess_data()
        print(f"✅ Loaded {len(df)} records")

        # 2. Prepare features and target
        features = ['location', 'lga', 'latitude', 'longitude',
                    'weather_condition', 'is_holiday', 'time_period', 'day_of_week']
        X = df[features].to_dict(orient='records')
        y = df['crime_type']

        # 3. Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # 4. Build and train model
        print("⚙️ Training model pipeline...")
        model = build_feature_pipeline()
        model.fit(X_train, y_train)

        # 5. Verify model format
        print("🔍 Verifying model format...")
        verify_model_format(model)

        # 6. Save model
        print("💾 Saving model...")
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)

        print(f"🎉 Model successfully trained and saved to {MODEL_PATH}")
        print("✨ Training complete!")

    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
