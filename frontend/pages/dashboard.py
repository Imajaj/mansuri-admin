"""
pages/dashboard.py
Dashboard – KPI metrics and visual summaries.
"""
import plotly.graph_objects as go
import streamlit as st

from utils.api import get_summary
from utils.auth import require_login


def render():
    require_login()
    st.title("📊 Dashboard")

    data = get_summary()
    if not data:
        st.warning("Could not load summary data.")
        return

    inv = data.get("inventory", {})
    ord_ = data.get("orders", {})

    # ── KPI row 1: Inventory ──────────────────────────────────────────────────
    st.subheader("📦 Inventory Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Records", inv.get("total", 0))
    c2.metric("✅ Received", inv.get("received", 0))
    c3.metric("⏳ Pending", inv.get("pending", 0))

    # ── KPI row 2: Orders ─────────────────────────────────────────────────────
    st.subheader("🚚 Orders Overview")
    c4, c5, c6 = st.columns(3)
    c4.metric("Total Orders", ord_.get("orders_total", 0))
    c5.metric("✅ Delivered", ord_.get("orders_delivered", 0))
    c6.metric("⏳ Pending", ord_.get("orders_pending", 0))

    # ── KPI row 3: Payments ───────────────────────────────────────────────────
    st.subheader("💰 Payment Status")
    p1, p2, p3 = st.columns(3)
    p1.metric("Done", ord_.get("payment_done", 0))
    p2.metric("Partial Pending", ord_.get("payment_partial", 0))
    p3.metric("Full Pending", ord_.get("payment_full_pending", 0))

    st.divider()

    # ── Charts ────────────────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Inventory Status**")
        fig = go.Figure(
            go.Pie(
                labels=["Received", "Pending"],
                values=[inv.get("received", 0), inv.get("pending", 0)],
                hole=0.4,
                marker_colors=["#4CAF50", "#FF9800"],
            )
        )
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("**Payment Status**")
        fig2 = go.Figure(
            go.Pie(
                labels=["Done", "Partial Pending", "Full Pending"],
                values=[
                    ord_.get("payment_done", 0),
                    ord_.get("payment_partial", 0),
                    ord_.get("payment_full_pending", 0),
                ],
                hole=0.4,
                marker_colors=["#2196F3", "#FFC107", "#F44336"],
            )
        )
        fig2.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260)
        st.plotly_chart(fig2, use_container_width=True)
