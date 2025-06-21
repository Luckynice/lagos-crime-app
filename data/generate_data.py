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

# 37 LCDAs mapped to their LGAs (simplified)
lcda_to_lga = {
    'Agbado/Oke-Odo': 'Alimosho', 'Agboyi-Ketu': 'Kosofe', 'Ayobo-Ipaja': 'Alimosho',
    'Bariga': 'Somolu', 'Coker-Aguda': 'Surulere', 'Ejigbo': 'Oshodi-Isolo',
    'Egbe-Idimu': 'Alimosho', 'Eredo': 'Epe', 'Eti-Osa East': 'Eti-Osa',
    'Iba': 'Ojo', 'Ifelodun': 'Ajeromi-Ifelodun', 'Igando-Ikotun': 'Alimosho',
    'Igbogbo/Bayeku': 'Ikorodu', 'Ijede': 'Ikorodu', 'Ikorodu North': 'Ikorodu',
    'Ikorodu West': 'Ikorodu', 'Ikosi-Isheri': 'Kosofe', 'Ikoyi-Obalende': 'Eti-Osa',
    'Imota': 'Ikorodu', 'Iru-Victoria Island': 'Eti-Osa', 'Isolo': 'Oshodi-Isolo',
    'Itire-Ikate': 'Surulere', 'Lagos Island East': 'Lagos Island', 'Lekki': 'Eti-Osa',
    'Mosan-Okunola': 'Alimosho', 'Odi-Olowo/Ojuwoye': 'Mushin', 'Olorunda': 'Badagry',
    'Oriade': 'Amuwo-Odofin', 'Orile-Agege': 'Agege', 'Oto-Awori': 'Ojo',
    'Ojodu': 'Ikeja', 'Ojokoro': 'Ifako-Ijaiye', 'Onigbongbo': 'Ikeja',
    'Yaba': 'Lagos Mainland', 'Akinyele': 'Alimosho', 'Otun-Akute': 'Alimosho',
    'Ijanikin': 'Ojo', 'Festac': 'Amuwo-Odofin'
}

lcdas = list(lcda_to_lga.keys())
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
        lga = area if area_type == 'LGA' else lcda_to_lga.get(area, 'Unknown')
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
            'lga': lga,
            'latitude': lat,
            'longitude': lon,
            'weather_condition': weather,
            'is_holiday': is_holiday,
            'time_period': time_period
        })

    df = pd.DataFrame(data)
    df.to_csv('data/lagos_crime_data.csv', index=False)
    print("✅ Dataset regenerated and saved to 'data/lagos_crime_data.csv'.")

if __name__ == "__main__":
    generate_data()
