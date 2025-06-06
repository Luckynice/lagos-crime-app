# data/generate_data.py
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

crime_types = ['Robbery', 'Assault', 'Kidnapping', 'Burglary', 'Fraud', 'Theft', 'Murder']
locations = ['Ikeja', 'Yaba', 'Lekki', 'Surulere', 'Agege', 'Ajah', 'Ikorodu', 'Epe', 'Victoria Island', 'Ojota']
lgas = ['Ikeja', 'Eti-Osa', 'Kosofe', 'Surulere', 'Agege', 'Ifako-Ijaiye', 'Ikorodu', 'Epe']
weather_conditions = ['Clear', 'Rainy', 'Cloudy', 'Sunny', 'Stormy']
time_periods = ['Morning', 'Afternoon', 'Evening', 'Night']

def generate_data(num_records=1000):
    data = []

    for _ in range(num_records):
        crime_time = fake.date_time_between(start_date='-2y', end_date='now')
        location = random.choice(locations)
        lat = fake.latitude()
        lon = fake.longitude()
        lga = random.choice(lgas)
        weather = random.choice(weather_conditions)
        crime_type = random.choice(crime_types)
        day_of_week = crime_time.strftime('%A')
        is_holiday = np.random.choice([0, 1], p=[0.9, 0.1])
        hour = crime_time.hour

        if hour < 12:
            time_period = 'Morning'
        elif hour < 17:
            time_period = 'Afternoon'
        elif hour < 20:
            time_period = 'Evening'
        else:
            time_period = 'Night'

        data.append({
            'crime_id': fake.uuid4(),
            'date_time': crime_time,
            'day_of_week': day_of_week,
            'crime_type': crime_type,
            'location': location,
            'lga': lga,
            'latitude': lat,
            'longitude': lon,
            'weather_condition': weather,
            'is_holiday': is_holiday,
            'time_period': time_period
        })

    df = pd.DataFrame(data)
    df.to_csv('data/lagos_crime_data.csv', index=False)
    print("✅ Dataset generated and saved to 'data/lagos_crime_data.csv'.")

if __name__ == "__main__":
    generate_data()
