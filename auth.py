import bcrypt
from pymongo import MongoClient
import os

# --- MongoDB Config ---
MONGO_URI = "mongodb+srv://luckynice02:Olaronke%402024%2B1@cluster-lagos-crime-pre.qqduxyz.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["lagos_crime"]
users_collection = db["users"]

# --- Register User ---
def register_user(email, password, name, role="user"):
    if users_collection.find_one({"email": email}):
        return False, "🚫 Email already registered."

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user_data = {
        "name": name,
        "email": email,
        "password_hash": hashed,
        "role": role
    }

    try:
        users_collection.insert_one(user_data)
        return True, "✅ Registration successful."
    except Exception as e:
        return False, f"❌ Registration failed: {e}"

# --- Login User ---
def login_user(email, password):
    user = users_collection.find_one({"email": email})
    if not user:
        return None

    if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
        return {
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "role": user.get("role", "user")
        }
    return None
