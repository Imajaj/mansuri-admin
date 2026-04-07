"""
pages/inventory.py
Inventory management – Add records, View/Filter table, Admin delete.
"""
import datetime
import pandas as pd
import streamlit as st

from utils.api import get_inventory, create_inventory, update_inventory, delete_inventory
from utils.auth import require_login, is_admin

ENTITY_OPTIONS = {
    "Mansuri Enterprises": "mansuri_enterprises",
    "Aman Stone Crusher": "aman_stone_crusher",
}
STATUS_OPTIONS = ["Received", "Pending"]


def render():
    require_login()
    st.title("📦 Inventory Management")

    tab_view, tab_add = st.tabs(["📋 View Records", "➕ Add Record"])

    # ── VIEW / FILTER ─────────────────────────────────────────────────────────
    with tab_view:
        st.subheader("Filter Records")
        f1, f2, f3, f4 = st.columns([2, 2, 2, 2])

        with f1:
            entity_label = st.selectbox("Entity", ["All"] + list(ENTITY_OPTIONS.keys()), key="iv_entity")
        with f2:
            status_filter = st.selectbox("Status", ["All"] + STATUS_OPTIONS, key="iv_status")
        with f3:
            date_from = st.date_input("From Date", value=None, key="iv_from")
        with f4:
            date_to = st.date_input("To Date", value=None, key="iv_to")

        params = {}
        if entity_label != "All":
            params["entity_type"] = ENTITY_OPTIONS[entity_label]
        if status_filter != "All":
            params["status"] = status_filter
        if date_from:
            params["date_from"] = str(date_from)
        if date_to:
            params["date_to"] = str(date_to)

        if st.button("🔍 Search", key="iv_search"):
            st.session_state["iv_params"] = params

        active_params = st.session_state.get("iv_params", {})
        result = get_inventory(active_params)

        if result:
            st.caption(f"Showing **{result['total']}** record(s)")
            if result["items"]:
                df = pd.DataFrame(result["items"])
                # Friendly column names
                df.rename(columns={
                    "entity_type": "Entity", "material_name": "Material",
                    "material_type": "Type", "record_date": "Date",
                    "record_time": "Time", "status": "Status",
                    "vehicle_no": "Vehicle", "driver_name": "Driver",
                    "driver_phone": "Phone", "received_by": "Received By",
                    "dealer_name": "Dealer", "dealer_location": "Dealer Loc",
                    "incharge_name": "Incharge", "incharge_location": "Incharge Loc",
                }, inplace=True)

                display_cols = ["id", "Entity", "Material", "Type", "Date",
                                "Status", "Vehicle", "Driver", "Received By"]
                st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

                # Admin: delete
                if is_admin():
                    st.markdown("---")
                    st.subheader("🗑️ Delete Record")
                    del_id = st.number_input("Record ID to delete", min_value=1, step=1, key="iv_del_id")
                    if st.button("Delete", type="primary", key="iv_del_btn"):
                        ok = delete_inventory(int(del_id))
                        if ok:
                            st.success(f"Record {del_id} deleted.")
                            st.rerun()
            else:
                st.info("No records found for the selected filters.")

    # ── ADD RECORD ────────────────────────────────────────────────────────────
    with tab_add:
        st.subheader("Add New Inventory Record")

        entity_label_add = st.selectbox("Entity *", list(ENTITY_OPTIONS.keys()), key="ia_entity")
        entity_val = ENTITY_OPTIONS[entity_label_add]

        col1, col2 = st.columns(2)
        with col1:
            material_name = st.text_input("Material Name *")
            material_type = st.text_input("Material Type")
            record_date = st.date_input("Date *", value=datetime.date.today())
            record_time = st.time_input("Time", value=datetime.datetime.now().time())
            received_by = st.text_input("Received By")
            status = st.selectbox("Status *", STATUS_OPTIONS)
        with col2:
            vehicle_no = st.text_input("Vehicle No.")
            driver_name = st.text_input("Driver Name")
            driver_phone = st.text_input("Driver Phone")

            if entity_val == "mansuri_enterprises":
                dealer_name = st.text_input("Dealer Name")
                dealer_location = st.text_input("Dealer Location")
                incharge_name = incharge_location = None
            else:
                incharge_name = st.text_input("Incharge Name")
                incharge_location = st.text_input("Incharge Location")
                dealer_name = dealer_location = None

        if st.button("✅ Save Record", type="primary", key="ia_save"):
            if not material_name:
                st.error("Material Name is required.")
            else:
                payload = {
                    "entity_type": entity_val,
                    "material_name": material_name,
                    "material_type": material_type or None,
                    "record_date": str(record_date),
                    "record_time": str(record_time),
                    "received_by": received_by or None,
                    "vehicle_no": vehicle_no or None,
                    "driver_name": driver_name or None,
                    "driver_phone": driver_phone or None,
                    "status": status,
                    "dealer_name": dealer_name or None,
                    "dealer_location": dealer_location or None,
                    "incharge_name": incharge_name or None,
                    "incharge_location": incharge_location or None,
                }
                rec = create_inventory(payload)
                if rec:
                    st.success(f"✅ Inventory record #{rec['id']} created successfully!")
