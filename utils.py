# utils.py

import pandas as pd
import numpy as np

def load_data():
    """
    Loads and preprocesses the Lagos crime data.
    Expects a CSV file at data/lagos_crime_data.csv.
    """
    df = pd.read_csv("data/lagos_crime_data.csv")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Convert datetime column
    if 'date_time' in df.columns:
        df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
        df['date'] = df['date_time'].dt.date
        df['hour'] = df['date_time'].dt.hour
    else:
        raise ValueError("Missing 'date_time' column in the dataset.")

    # Fill in missing location values
    if 'latitude' in df.columns:
        df['latitude'] = df['latitude'].fillna(np.random.uniform(6.4, 6.7))
    if 'longitude' in df.columns:
        df['longitude'] = df['longitude'].fillna(np.random.uniform(3.2, 3.5))

    return df
