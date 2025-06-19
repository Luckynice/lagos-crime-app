# data/generate_data.py

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

crime_types = ['Robbery', 'Assault', 'Kidnapping', 'Burglary', 'Fraud', 'Theft', 'Murder']
locations = ['Ikeja', 'Yaba', 'Lekki', 'Surulere', 'Agege', 'Ajah', 'Ikorodu', 'Epe', 'Victoria Island', 'Ojota']
weather_conditions = ['Clear', 'Rainy', 'Cloudy', 'Sunny', 'Stormy']

# 20 LGAs in Lagos State
lgas = [
    'Agege', 'Ajeromi-Ifelodun', 'Alimosho', 'Amuwo-Odofin',
    'Apapa', 'Badagry', 'Epe', 'Eti-Osa',
    'Ibeju-Lekki', 'Ifako-Ijaiye', 'Ikeja', 'Ikorodu',
    'Kosofe', 'Mushin', 'Oshodi-Isolo', 'Somolu',
    'Lagos Island', 'Lagos Mainland', 'Ojo', 'Surulere'
]

# 37 LCDAs in Lagos State
lcdas = [
    'Agbado/Oke-Odo', 'Agboyi-Ketu', 'Ayobo-Ipaja', 'Bariga', 'Coker-Aguda',
    'Ejigbo', 'Egbe-Idimu', 'Eredo', 'Eti-Osa East', 'Iba',
    'Ifelodun', 'Igando-Ikotun', 'Igbogbo/Bayeku', 'Ijede',
    'Ikorodu North', 'Ikorodu West', 'Ikosi-Isheri', 'Ikoyi-Obalende',
    'Imota', 'Iru-Victoria Island', 'Isolo', 'Itire-Ikate',
    'Lagos Island East', 'Lekki', 'Mosan-Okunola', 'Odi-Olowo/Ojuwoye',
    'Olorunda', 'Oriade', 'Orile-Agege', 'Oto-Awori', 'Ojodu',
    'Ojokoro', 'Onigbongbo', 'Yaba', 'Akinyele', 'Otun-Akute', 'Ijanikin', 'Festac'
]

# Combine into all local areas
all_areas = lgas + lcdas

time_periods = ['Morning', 'Afternoon', 'Evening', 'Night']

def generate_data(num_records=1000):
    data = []

    for _ in range(num_records):
        crime_time = fake.date_time_between(start_date='-2y', end_date='now')
        location = random.choice(locations)
        lat = fake.latitude()
        lon = fake.longitude()
        area = random.choice(all_areas)
        area_type = 'LGA' if area in lgas else 'LCDA'
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
            'area': area,
            'area_type': area_type,
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
