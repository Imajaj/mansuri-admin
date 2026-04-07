"""
app/services/order.py
CRUD and filter logic for Order/Dispatch records.
"""
from datetime import date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate


def create_order(db: Session, data: OrderCreate) -> Order:
    record = Order(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_order(db: Session, order_id: int) -> Order:
    record = db.query(Order).filter(Order.id == order_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Order not found")
    return record


def list_orders(
    db: Session,
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    payment_status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(Order)
    if entity_type:
        q = q.filter(Order.entity_type == entity_type)
    if status:
        q = q.filter(Order.status == status)
    if payment_status:
        q = q.filter(Order.payment_status == payment_status)
    if date_from:
        q = q.filter(Order.record_date >= date_from)
    if date_to:
        q = q.filter(Order.record_date <= date_to)
    total = q.count()
    items = q.order_by(Order.record_date.desc()).offset(skip).limit(limit).all()
    return total, items


def update_order(db: Session, order_id: int, data: OrderUpdate) -> Order:
    record = get_order(db, order_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


def delete_order(db: Session, order_id: int) -> None:
    record = get_order(db, order_id)
    db.delete(record)
    db.commit()


def get_summary(db: Session):
    """Return high-level stats for the dashboard."""
    from sqlalchemy import func

    inv_total = db.query(func.count(Order.id)).scalar()
    return {
        "orders_total": db.query(Order).count(),
        "orders_pending": db.query(Order).filter(Order.status == "Pending").count(),
        "orders_delivered": db.query(Order).filter(Order.status == "Delivered").count(),
        "payment_done": db.query(Order).filter(Order.payment_status == "Done").count(),
        "payment_partial": db.query(Order).filter(Order.payment_status == "Partial Pending").count(),
        "payment_full_pending": db.query(Order).filter(Order.payment_status == "Full Pending").count(),
    }
