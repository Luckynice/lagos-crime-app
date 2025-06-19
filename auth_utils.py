import requests

BASE_URL = "http://localhost:5000/api/auth"

def login_user(username, password):
    response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    return response.json() if response.status_code == 200 else None

def register_user(username, email, password, role):
    response = requests.post(f"{BASE_URL}/register", json={"username": username, "email": email, "password": password, "role": role})
    return response.json() if response.status_code == 201 else None
