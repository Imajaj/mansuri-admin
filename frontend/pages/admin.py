"""
pages/admin.py
Admin Panel – user management (create, view, update role/password).
Admin access required.
"""
import pandas as pd
import streamlit as st

from utils.api import get_users, create_user, update_user
from utils.auth import require_admin_role


def render():
    require_admin_role()
    st.title("⚙️ Admin Panel")

    tab_list, tab_create, tab_edit = st.tabs(["👥 All Users", "➕ Create User", "✏️ Update User"])

    # ── LIST USERS ────────────────────────────────────────────────────────────
    with tab_list:
        st.subheader("All Users")
        users = get_users()
        if users:
            df = pd.DataFrame(users)
            df.rename(columns={
                "id": "ID", "username": "Username", "email": "Email",
                "role": "Role", "is_active": "Active", "created_at": "Created",
            }, inplace=True)
            st.dataframe(
                df[["ID", "Username", "Email", "Role", "Active", "Created"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No users found.")

    # ── CREATE USER ───────────────────────────────────────────────────────────
    with tab_create:
        st.subheader("Create New User")

        with st.form("create_user_form"):
            username = st.text_input("Username *")
            email = st.text_input("Email *")
            password = st.text_input("Password *", type="password")
            role = st.selectbox("Role *", ["member", "admin"])
            submitted = st.form_submit_button("Create User", use_container_width=True)

        if submitted:
            if not username or not email or not password:
                st.error("Username, email, and password are required.")
            else:
                result = create_user({
                    "username": username,
                    "email": email,
                    "password": password,
                    "role": role,
                })
                if result:
                    st.success(f"✅ User **{result['username']}** created with role **{result['role']}**.")

    # ── UPDATE USER ───────────────────────────────────────────────────────────
    with tab_edit:
        st.subheader("Update User")

        with st.form("update_user_form"):
            user_id = st.number_input("User ID *", min_value=1, step=1)
            new_role = st.selectbox("New Role", ["member", "admin"])
            new_password = st.text_input("New Password (leave blank to keep current)", type="password")
            is_active = st.checkbox("Active", value=True)
            submitted2 = st.form_submit_button("Update User", use_container_width=True)

        if submitted2:
            payload = {"role": new_role, "is_active": is_active}
            if new_password:
                payload["password"] = new_password
            result = update_user(int(user_id), payload)
            if result:
                st.success(f"✅ User **{result['username']}** updated.")
