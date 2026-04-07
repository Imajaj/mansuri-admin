"""
utils/auth.py
Session state helpers for login/logout.
"""
import streamlit as st
from utils.api import login as api_login


def do_login(username: str, password: str) -> bool:
    result = api_login(username, password)
    if result and "access_token" in result:
        st.session_state["token"] = result["access_token"]
        st.session_state["role"] = result["role"]
        st.session_state["username"] = result["username"]
        return True
    st.error("Invalid username or password.")
    return False


def do_logout():
    st.session_state.clear()


def is_logged_in() -> bool:
    return bool(st.session_state.get("token"))


def is_admin() -> bool:
    return st.session_state.get("role") == "admin"


def require_login():
    if not is_logged_in():
        st.warning("You must be logged in to view this page.")
        st.stop()


def require_admin_role():
    require_login()
    if not is_admin():
        st.error("Admin access required.")
        st.stop()
