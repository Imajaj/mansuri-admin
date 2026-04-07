"""
app/routes/inventory.py
Inventory CRUD endpoints with filtering.
"""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, require_admin
from app.models.user import User
from app.schemas.inventory import InventoryCreate, InventoryListResponse, InventoryOut, InventoryUpdate
from app.services.inventory import (
    create_inventory,
    delete_inventory,
    get_inventory,
    list_inventory,
    update_inventory,
)

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/", response_model=InventoryOut)
def create(
    data: InventoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),  # any authenticated user
):
    return create_inventory(db, data)


@router.get("/", response_model=InventoryListResponse)
def read_list(
    entity_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total, items = list_inventory(db, entity_type, status, date_from, date_to, skip, limit)
    return {"total": total, "items": items}


@router.get("/{record_id}", response_model=InventoryOut)
def read_one(record_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_inventory(db, record_id)


@router.put("/{record_id}", response_model=InventoryOut)
def update(
    record_id: int,
    data: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),  # admin only
):
    return update_inventory(db, record_id, data)


@router.delete("/{record_id}", status_code=204)
def delete(
    record_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),  # admin only
):
    delete_inventory(db, record_id)
