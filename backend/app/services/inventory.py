"""
app/services/inventory.py
CRUD and filter logic for Inventory records.
"""
from datetime import date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate


def create_inventory(db: Session, data: InventoryCreate) -> Inventory:
    record = Inventory(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_inventory(db: Session, record_id: int) -> Inventory:
    record = db.query(Inventory).filter(Inventory.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return record


def list_inventory(
    db: Session,
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
):
    q = db.query(Inventory)
    if entity_type:
        q = q.filter(Inventory.entity_type == entity_type)
    if status:
        q = q.filter(Inventory.status == status)
    if date_from:
        q = q.filter(Inventory.record_date >= date_from)
    if date_to:
        q = q.filter(Inventory.record_date <= date_to)
    total = q.count()
    items = q.order_by(Inventory.record_date.desc()).offset(skip).limit(limit).all()
    return total, items


def update_inventory(db: Session, record_id: int, data: InventoryUpdate) -> Inventory:
    record = get_inventory(db, record_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


def delete_inventory(db: Session, record_id: int) -> None:
    record = get_inventory(db, record_id)
    db.delete(record)
    db.commit()
