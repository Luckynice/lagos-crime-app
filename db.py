# db.py
from pymongo import MongoClient
import certifi
import os
from pymongo.server_api import ServerApi
from datetime import datetime

def save_prediction(data):
    from streamlit.runtime.secrets import secrets
    uri = secrets["mongo"]["uri"]
    db_name = secrets["mongo"]["db_name"]
    collection_name = secrets["mongo"]["collection_name"]

    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    db = client[db_name]
    collection = db[collection_name]

    # Ensure datetime is in ISO format
    data["date_time"] = data.pop("datetime", datetime.utcnow())
    collection.insert_one(data)
