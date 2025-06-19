import bcrypt
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client["lagos_crime"]
users_col = db["users"]

def register_user(name, email, password, role="analyst"):
    if users_col.find_one({"email": email}):
        return False, "User already exists"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_col.insert_one({"name": name, "email": email, "password": hashed, "role": role})
    return True, "User registered successfully"

def login_user(email, password):
    user = users_col.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        return user
    return None
