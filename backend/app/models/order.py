"""
==============================================================
backend/app/models/order.py
==============================================================
This file defines the 'orders' TABLE — for OUTGOING DISPATCH.

When materials are sold/sent out to a customer, staff creates
a record here.

DELIVERY STATUS:
  "Delivered" → material has been delivered to customer
  "Pending"   → dispatch created but not yet delivered

PAYMENT STATUS:
  "Done"            → full payment received
  "Partial Pending" → some payment received, rest due
  "Full Pending"    → no payment received yet

HOW TO ADD A NEW FIELD (example: invoice number):
  1. Add here:  invoice_no: Mapped[str] = mapped_column(String(50), nullable=True)
  2. Add to schemas/order.py in OrderCreate, OrderUpdate, OrderOut
  3. Run in Supabase SQL Editor (if DB already exists):
     ALTER TABLE orders ADD COLUMN invoice_no VARCHAR(50);
==============================================================
"""

from datetime import date, datetime, time, timezone

from sqlalchemy import Date, DateTime, Index, Numeric, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Order(Base):
    __tablename__ = "orders"

    # ── Primary key ──────────────────────────────────────────
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # ── Which business this order belongs to ─────────────────
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # ── What was dispatched ───────────────────────────────────
    material_name: Mapped[str] = mapped_column(String(120), nullable=False)
    material_type: Mapped[str] = mapped_column(String(80), nullable=True)

    # ── When it was dispatched ────────────────────────────────
    record_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    record_time: Mapped[time] = mapped_column(Time, nullable=True)

    # ── Customer details ──────────────────────────────────────
    customer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    customer_location: Mapped[str] = mapped_column(String(200), nullable=True)
    shopkeeper: Mapped[str] = mapped_column(String(120), nullable=True)     # middleman/shop

    # ── Transport details ─────────────────────────────────────
    vehicle_no: Mapped[str] = mapped_column(String(30), nullable=True)
    driver_name: Mapped[str] = mapped_column(String(100), nullable=True)
    driver_phone: Mapped[str] = mapped_column(String(20), nullable=True)

    # ── Delivery status ───────────────────────────────────────
    status: Mapped[str] = mapped_column(String(20), default="Pending", nullable=False)

    # ── Payment details ───────────────────────────────────────
    # Numeric(12, 2) = up to 12 digits total, 2 decimal places
    # Example: 999999999.99 (nine hundred ninety-nine million)
    payment_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    payment_status: Mapped[str] = mapped_column(
        String(30), default="Full Pending", nullable=False
    )

    # ── Audit timestamps ──────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Index for fast date + entity filtering
    __table_args__ = (
        Index("ix_orders_entity_date", "entity_type", "record_date"),
    )
