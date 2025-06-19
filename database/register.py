# pages/register.py
import streamlit as st
from db import init_db, add_user

init_db()

st.title("🧑‍💻 Register New Account")

username = st.text_input("Choose a username")
password = st.text_input("Choose a password", type="password")
role = st.selectbox("Select role", options=["public", "analyst", "admin"])

if st.button("Register"):
    if username and password:
        try:
            add_user(username, password, role)
            st.success(f"User '{username}' registered as '{role}'. You can now log in.")
        except Exception as e:
            st.error(f"Failed to register: {e}")
    else:
        st.error("Username and password are required.")
