"""
==============================================================
frontend/utils/api.py
==============================================================
This file is the ONLY place that talks to the FastAPI backend.

All HTTP calls go through here. This means:
  - If the backend URL changes, you change it in ONE place
  - Error handling is consistent across all pages
  - Easy to find and debug API issues

HOW THE STREAMLIT → FASTAPI COMMUNICATION WORKS:
  1. User clicks a button in Streamlit
  2. Streamlit calls a function in this file (e.g. create_inventory)
  3. This file sends an HTTP request to FastAPI
  4. FastAPI processes it and returns JSON
  5. This file returns the JSON to Streamlit
  6. Streamlit shows the result to the user

HOW TO ADD A NEW API CALL:
  1. Find the relevant section below (Auth, Inventory, Orders)
  2. Add a new function following the same pattern
  3. Call it from the relevant page in pages/

HOW AUTHENTICATION WORKS:
  After login, the JWT token is stored in st.session_state["token"].
  _headers() adds this token to every request automatically.
  If the token is missing → the backend returns 401 → user is logged out.
==============================================================
"""

import os
import requests
import streamlit as st

# ── Backend URL ───────────────────────────────────────────────────────────────
# This reads from the .env file (local) or Railway environment variable (production).
# Local development: http://localhost:8000
# Production:        https://your-backend.railway.app
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


def _headers() -> dict:
    """
    Returns the Authorization header with the JWT token.
    Called automatically before every API request.
    If not logged in, returns empty dict (backend will reject the request).
    """
    token = st.session_state.get("token", "")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _handle(resp: requests.Response):
    """
    Handles the HTTP response from FastAPI.
    - 401 = session expired → log out and stop
    - 204 = success with no content (e.g. delete) → return True
    - Error → show error message and return None
    - Success → return the JSON data
    """
    # Session expired — token invalid
    if resp.status_code == 401:
        st.session_state.clear()
        st.error("⚠️ Session expired. Please log in again.")
        st.stop()

    # Server error
    if not resp.ok:
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        st.error(f"❌ Error {resp.status_code}: {detail}")
        return None

    # Successful delete (no content returned)
    if resp.status_code == 204:
        return True

    # Successful response with JSON data
    return resp.json()


# ══════════════════════════════════════════════════════════════
# AUTH endpoints
# ══════════════════════════════════════════════════════════════

def login(username: str, password: str):
    """Send username + password, get back a JWT token."""
    resp = requests.post(
        f"{API_BASE}/auth/login",
        data={"username": username, "password": password},
    )
    return _handle(resp)


def get_me():
    """Get the currently logged-in user's profile."""
    return _handle(requests.get(f"{API_BASE}/auth/me", headers=_headers()))


def get_users():
    """Get list of all users. Admin only."""
    return _handle(requests.get(f"{API_BASE}/auth/users", headers=_headers()))


def create_user(payload: dict):
    """Create a new user. Admin only."""
    return _handle(requests.post(f"{API_BASE}/auth/users", json=payload, headers=_headers()))


def update_user(user_id: int, payload: dict):
    """Update a user's role, password, or active status. Admin only."""
    return _handle(requests.put(f"{API_BASE}/auth/users/{user_id}", json=payload, headers=_headers()))


# ══════════════════════════════════════════════════════════════
# DASHBOARD endpoint
# ══════════════════════════════════════════════════════════════

def get_summary():
    """
    Get summary statistics for the dashboard.
    Returns counts for inventory and orders by status.
    """
    return _handle(requests.get(f"{API_BASE}/orders/summary", headers=_headers()))


# ══════════════════════════════════════════════════════════════
# INVENTORY endpoints
# ══════════════════════════════════════════════════════════════

def get_inventory(params: dict = {}):
    """
    Get a list of inventory records with optional filters.
    params example: {"entity_type": "mansuri_enterprises", "status": "Pending"}
    """
    return _handle(requests.get(f"{API_BASE}/inventory/", params=params, headers=_headers()))


def create_inventory(payload: dict):
    """Create a new inventory (incoming stock) record."""
    return _handle(requests.post(f"{API_BASE}/inventory/", json=payload, headers=_headers()))


def update_inventory(record_id: int, payload: dict):
    """Update an existing inventory record. Admin only."""
    return _handle(requests.put(f"{API_BASE}/inventory/{record_id}", json=payload, headers=_headers()))


def delete_inventory(record_id: int):
    """Delete an inventory record. Admin only."""
    return _handle(requests.delete(f"{API_BASE}/inventory/{record_id}", headers=_headers()))


# ══════════════════════════════════════════════════════════════
# ORDERS endpoints
# ══════════════════════════════════════════════════════════════

def get_orders(params: dict = {}):
    """
    Get a list of orders with optional filters.
    params example: {"payment_status": "Full Pending", "entity_type": "aman_stone_crusher"}
    """
    return _handle(requests.get(f"{API_BASE}/orders/", params=params, headers=_headers()))


def create_order(payload: dict):
    """Create a new order/dispatch record."""
    return _handle(requests.post(f"{API_BASE}/orders/", json=payload, headers=_headers()))


def update_order(order_id: int, payload: dict):
    """Update an existing order (e.g. mark as delivered, update payment). Admin only."""
    return _handle(requests.put(f"{API_BASE}/orders/{order_id}", json=payload, headers=_headers()))


def delete_order(order_id: int):
    """Delete an order record. Admin only."""
    return _handle(requests.delete(f"{API_BASE}/orders/{order_id}", headers=_headers()))
