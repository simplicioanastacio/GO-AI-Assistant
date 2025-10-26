# auth/session.py
import streamlit as st

def login_session(user: dict):
    st.session_state["user"] = user
    st.session_state["is_logged_in"] = True
    st.session_state["current_page"] = "dashboard"

def logout_session():
    st.session_state.pop("user", None)
    st.session_state["is_logged_in"] = False
    st.session_state["current_page"] = "home"

def current_user():
    return st.session_state.get("user")
