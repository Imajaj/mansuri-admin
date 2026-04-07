"""
app.py  ──  Streamlit application root
Run with:  streamlit run app.py
"""
import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Mansuri Admin Portal",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom global CSS ─────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { background: #1a1a2e; }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    .block-container { padding-top: 1.5rem; }
    div[data-testid="metric-container"] {
        background: #f0f4ff;
        border: 1px solid #d0d9f0;
        border-radius: 10px;
        padding: 0.8rem 1rem;
    }
    .stButton > button { border-radius: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

from utils.auth import is_logged_in, do_login, do_logout  # noqa: E402

# ── Login gate ────────────────────────────────────────────────────────────────
if not is_logged_in():
    st.title("🏗️ Mansuri Admin Portal")
    st.subheader("Please log in to continue")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if do_login(username, password):
            st.rerun()
    st.stop()

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏗️ Mansuri Portal")
    st.markdown(f"**User:** {st.session_state.get('username', '')}  \n**Role:** {st.session_state.get('role', '').capitalize()}")
    st.divider()

    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "📦 Inventory", "🚚 Orders", "⚙️ Admin Panel"],
        label_visibility="collapsed",
    )

    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        do_logout()
        st.rerun()

# ── Route to pages ────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    from pages.dashboard import render
    render()
elif page == "📦 Inventory":
    from pages.inventory import render
    render()
elif page == "🚚 Orders":
    from pages.orders import render
    render()
elif page == "⚙️ Admin Panel":
    from pages.admin import render
    render()
