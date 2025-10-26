# app/router.py
import streamlit as st
from auth.auth import register_user, login_user
from auth.session import login_session, logout_session, current_user
from app.dashboard import dashboard

def login_form():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_btn"):
        user = login_user(email, password)
        if user:
            login_session(user)
            st.success(f"Welcome back {user['username']}")
            st.rerun()
        else:
            st.error("Invalid email or password.")

def register_form():
    st.subheader("Register")
    username = st.text_input("Username", key="reg_username")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    if st.button("Register", key="register_btn"):
        if register_user(username, email, password):
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Registration failed. Email may already exist.")

def show_login_register():
    col1, col2 = st.columns(2)
    with col1:
        login_form()
    with col2:
        register_form()

def run_router():
    if current_user():
        dashboard()
    else:
        show_login_register()
