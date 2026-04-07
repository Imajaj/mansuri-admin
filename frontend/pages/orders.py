"""
pages/orders.py
Orders & Dispatch management – Add, View, Filter, Update, Delete.
"""
import datetime
import pandas as pd
import streamlit as st

from utils.api import get_orders, create_order, update_order, delete_order
from utils.auth import require_login, is_admin

ENTITY_OPTIONS = {
    "Mansuri Enterprises": "mansuri_enterprises",
    "Aman Stone Crusher": "aman_stone_crusher",
}
STATUS_OPTIONS = ["Delivered", "Pending"]
PAYMENT_STATUS_OPTIONS = ["Done", "Partial Pending", "Full Pending"]


def render():
    require_login()
    st.title("🚚 Orders & Dispatch Management")

    tab_view, tab_add, tab_edit = st.tabs(["📋 View Orders", "➕ Add Order", "✏️ Update Order"])

    # ── VIEW / FILTER ─────────────────────────────────────────────────────────
    with tab_view:
        st.subheader("Filter Orders")
        f1, f2, f3, f4, f5 = st.columns([2, 2, 2, 2, 2])

        with f1:
            entity_label = st.selectbox("Entity", ["All"] + list(ENTITY_OPTIONS.keys()), key="ov_entity")
        with f2:
            status_filter = st.selectbox("Delivery Status", ["All"] + STATUS_OPTIONS, key="ov_status")
        with f3:
            pay_filter = st.selectbox("Payment Status", ["All"] + PAYMENT_STATUS_OPTIONS, key="ov_pay")
        with f4:
            date_from = st.date_input("From Date", value=None, key="ov_from")
        with f5:
            date_to = st.date_input("To Date", value=None, key="ov_to")

        params = {}
        if entity_label != "All":
            params["entity_type"] = ENTITY_OPTIONS[entity_label]
        if status_filter != "All":
            params["status"] = status_filter
        if pay_filter != "All":
            params["payment_status"] = pay_filter
        if date_from:
            params["date_from"] = str(date_from)
        if date_to:
            params["date_to"] = str(date_to)

        if st.button("🔍 Search", key="ov_search"):
            st.session_state["ov_params"] = params

        active_params = st.session_state.get("ov_params", {})
        result = get_orders(active_params)

        if result:
            st.caption(f"Showing **{result['total']}** order(s)")
            if result["items"]:
                df = pd.DataFrame(result["items"])
                df.rename(columns={
                    "entity_type": "Entity", "material_name": "Material",
                    "material_type": "Type", "record_date": "Date",
                    "customer_name": "Customer", "customer_location": "Location",
                    "shopkeeper": "Shopkeeper", "vehicle_no": "Vehicle",
                    "driver_name": "Driver", "driver_phone": "Phone",
                    "status": "Delivery", "payment_amount": "Amount (₹)",
                    "payment_status": "Payment",
                }, inplace=True)

                display_cols = ["id", "Entity", "Material", "Date", "Customer",
                                "Vehicle", "Delivery", "Amount (₹)", "Payment"]
                st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

                if is_admin():
                    st.markdown("---")
                    st.subheader("🗑️ Delete Order")
                    del_id = st.number_input("Order ID to delete", min_value=1, step=1, key="ov_del_id")
                    if st.button("Delete", type="primary", key="ov_del_btn"):
                        ok = delete_order(int(del_id))
                        if ok:
                            st.success(f"Order {del_id} deleted.")
                            st.rerun()
            else:
                st.info("No orders found for the selected filters.")

    # ── ADD ORDER ─────────────────────────────────────────────────────────────
    with tab_add:
        st.subheader("Add New Order / Dispatch")

        entity_label_add = st.selectbox("Entity *", list(ENTITY_OPTIONS.keys()), key="oa_entity")
        entity_val = ENTITY_OPTIONS[entity_label_add]

        col1, col2 = st.columns(2)
        with col1:
            material_name = st.text_input("Material Name *", key="oa_mat")
            material_type = st.text_input("Material Type", key="oa_mtype")
            record_date = st.date_input("Date *", value=datetime.date.today(), key="oa_date")
            record_time = st.time_input("Time", value=datetime.datetime.now().time(), key="oa_time")
            customer_name = st.text_input("Customer Name *", key="oa_cust")
            customer_location = st.text_input("Customer Location", key="oa_cloc")
        with col2:
            shopkeeper = st.text_input("Shopkeeper", key="oa_shop")
            vehicle_no = st.text_input("Vehicle No.", key="oa_veh")
            driver_name = st.text_input("Driver Name", key="oa_drv")
            driver_phone = st.text_input("Driver Phone", key="oa_phn")
            status = st.selectbox("Delivery Status *", STATUS_OPTIONS, key="oa_stat")
            payment_amount = st.number_input("Payment Amount (₹)", min_value=0.0, step=100.0, key="oa_amt")
            payment_status = st.selectbox("Payment Status *", PAYMENT_STATUS_OPTIONS, key="oa_pstat")

        if st.button("✅ Save Order", type="primary", key="oa_save"):
            if not material_name or not customer_name:
                st.error("Material Name and Customer Name are required.")
            else:
                payload = {
                    "entity_type": entity_val,
                    "material_name": material_name,
                    "material_type": material_type or None,
                    "record_date": str(record_date),
                    "record_time": str(record_time),
                    "customer_name": customer_name,
                    "customer_location": customer_location or None,
                    "shopkeeper": shopkeeper or None,
                    "vehicle_no": vehicle_no or None,
                    "driver_name": driver_name or None,
                    "driver_phone": driver_phone or None,
                    "status": status,
                    "payment_amount": payment_amount if payment_amount > 0 else None,
                    "payment_status": payment_status,
                }
                rec = create_order(payload)
                if rec:
                    st.success(f"✅ Order #{rec['id']} created successfully!")

    # ── UPDATE ORDER (Admin only) ─────────────────────────────────────────────
    with tab_edit:
        if not is_admin():
            st.info("Only admins can update existing orders.")
            return

        st.subheader("Update Existing Order")
        upd_id = st.number_input("Order ID to update", min_value=1, step=1, key="ou_id")

        upd_status = st.selectbox("New Delivery Status", STATUS_OPTIONS, key="ou_stat")
        upd_pay_status = st.selectbox("New Payment Status", PAYMENT_STATUS_OPTIONS, key="ou_pstat")
        upd_pay_amount = st.number_input("New Payment Amount (₹)", min_value=0.0, step=100.0, key="ou_amt")

        if st.button("💾 Update", type="primary", key="ou_save"):
            payload = {
                "status": upd_status,
                "payment_status": upd_pay_status,
            }
            if upd_pay_amount > 0:
                payload["payment_amount"] = upd_pay_amount
            rec = update_order(int(upd_id), payload)
            if rec:
                st.success(f"✅ Order #{rec['id']} updated.")
