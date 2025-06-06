# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load data
df = pd.read_csv('data/lagos_crime_data.csv')

# Encode categorical features
le = LabelEncoder()
df['location'] = le.fit_transform(df['location'])
df['lga'] = le.fit_transform(df['lga'])
df['weather_condition'] = le.fit_transform(df['weather_condition'])
df['time_period'] = le.fit_transform(df['time_period'])
df['day_of_week'] = le.fit_transform(df['day_of_week'])
df['crime_type'] = le.fit_transform(df['crime_type'])

# Features and label
features = ['location', 'lga', 'latitude', 'longitude', 'weather_condition', 'is_holiday', 'time_period', 'day_of_week']
X = df[features]
y = df['crime_type']

# Split & train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
with open('models/crime_model.pkl', 'wb') as f:
    pickle.dump((model, le), f)

print("✅ Model trained and saved to 'models/crime_model.pkl'")
