import streamlit as st
from auth import login_user, register_user  # ✅ from your working auth.py

def show_login_ui():
    st.title("🔐 Admin & User Login")

    # Initialize session state
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None

    # Already logged in
    if st.session_state.user:
        st.success(f"✅ Logged in as {st.session_state.user['name']} ({st.session_state.role})")
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.user_email = None
            st.rerun()
        return

    # Login Form
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.session_state.role = user.get("role", "user")
                st.session_state.user_email = user.get("email")

                st.success(f"✅ Welcome, {user['name']}!")
                if st.session_state.role == "admin":
                    st.switch_page("pages/Admin.py")
                else:
                    st.switch_page("App.py")
            else:
                st.error("❌ Invalid email or password")

    # Registration Form
    with st.expander("➕ Register New Admin/User"):
        with st.form("register_form"):
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("New Email")
            reg_password = st.text_input("New Password", type="password")
            reg_role = st.selectbox("Role", ["user", "admin"])
            reg_submit = st.form_submit_button("Register")

            if reg_submit:
                success, msg = register_user(reg_email, reg_password, reg_name, reg_role)
                st.success(msg) if success else st.error(msg)

# Run the login interface
show_login_ui()
