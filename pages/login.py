import streamlit as st
from auth import login_user, register_user

def show_login():
    st.title("🔐 Login")

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        st.success(f"Logged in as {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
        return

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if login_user(email, password):
                st.session_state.user = email
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid email or password")

    with st.expander("Register New Account"):
        with st.form("register_form"):
            reg_email = st.text_input("New Email")
            reg_password = st.text_input("New Password", type="password")
            reg_submit = st.form_submit_button("Register")
            if reg_submit:
                success, msg = register_user(reg_email, reg_password)
                st.success(msg) if success else st.error(msg)
