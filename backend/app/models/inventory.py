"""
==============================================================
backend/app/models/inventory.py
==============================================================
This file defines the 'inventory' TABLE — for INCOMING STOCK.

When materials arrive at a location, staff creates a record here.

ONE TABLE FOR TWO BUSINESSES:
  We use the 'entity_type' column to tell them apart:
    "mansuri_enterprises"  → has dealer_name + dealer_location
    "aman_stone_crusher"   → has incharge_name + incharge_location
  All other fields are shared.

  WHY ONE TABLE? Simpler to manage, filter, and report.

HOW TO ADD A NEW FIELD (example: quantity in tonnes):
  1. Add here:  quantity_tonnes: Mapped[float] = mapped_column(Float, nullable=True)
  2. Add to schemas/inventory.py in InventoryCreate, InventoryUpdate, InventoryOut
  3. Restart server
  NOTE: For existing DB, run in Supabase SQL Editor:
        ALTER TABLE inventory ADD COLUMN quantity_tonnes FLOAT;

STATUS VALUES (what to put in the 'status' field):
  "Received" → material has arrived and been checked in
  "Pending"  → expected but not yet arrived
==============================================================
"""

from datetime import date, datetime, time, timezone

from sqlalchemy import Date, DateTime, Index, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    # ── Primary key ──────────────────────────────────────────
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # ── Which business this record belongs to ────────────────
    # Values: "mansuri_enterprises" or "aman_stone_crusher"
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # ── What material arrived ─────────────────────────────────
    material_name: Mapped[str] = mapped_column(String(120), nullable=False)
    material_type: Mapped[str] = mapped_column(String(80), nullable=True)   # e.g. "Grade A", "Fine"

    # ── When it arrived ───────────────────────────────────────
    record_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    record_time: Mapped[time] = mapped_column(Time, nullable=True)

    # ── Who handled it ────────────────────────────────────────
    received_by: Mapped[str] = mapped_column(String(100), nullable=True)    # staff member name

    # ── Transport details ─────────────────────────────────────
    vehicle_no: Mapped[str] = mapped_column(String(30), nullable=True)      # e.g. "GJ05AB1234"
    driver_name: Mapped[str] = mapped_column(String(100), nullable=True)
    driver_phone: Mapped[str] = mapped_column(String(20), nullable=True)

    # ── Status of this delivery ───────────────────────────────
    # "Received" = arrived and checked in   |   "Pending" = not yet arrived
    status: Mapped[str] = mapped_column(String(20), default="Pending", nullable=False)

    # ── Mansuri Enterprises only ──────────────────────────────
    # These are NULL (empty) for Aman Stone Crusher records
    dealer_name: Mapped[str] = mapped_column(String(120), nullable=True)
    dealer_location: Mapped[str] = mapped_column(String(200), nullable=True)

    # ── Aman Stone Crusher only ───────────────────────────────
    # These are NULL (empty) for Mansuri Enterprises records
    incharge_name: Mapped[str] = mapped_column(String(120), nullable=True)
    incharge_location: Mapped[str] = mapped_column(String(200), nullable=True)

    # ── Audit timestamps (set automatically) ─────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ── Database index for fast filtering ────────────────────
    # This makes "show me all records for entity X in month Y" very fast
    # even with thousands of records
    __table_args__ = (
        Index("ix_inventory_entity_date", "entity_type", "record_date"),
    )
