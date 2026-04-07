"""
app/routes/order.py
Orders & Dispatch CRUD endpoints with filtering.
"""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, require_admin
from app.models.user import User
from app.schemas.order import OrderCreate, OrderListResponse, OrderOut, OrderUpdate
from app.services.order import (
    create_order,
    delete_order,
    get_order,
    get_summary,
    list_orders,
    update_order,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut)
def create(
    data: OrderCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return create_order(db, data)


@router.get("/summary")
def summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Dashboard summary stats."""
    from app.models.inventory import Inventory

    inv_total = db.query(Inventory).count()
    inv_pending = db.query(Inventory).filter(Inventory.status == "Pending").count()
    inv_received = db.query(Inventory).filter(Inventory.status == "Received").count()

    order_stats = get_summary(db)
    return {
        "inventory": {
            "total": inv_total,
            "pending": inv_pending,
            "received": inv_received,
        },
        "orders": order_stats,
    }


@router.get("/", response_model=OrderListResponse)
def read_list(
    entity_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    payment_status: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total, items = list_orders(db, entity_type, status, payment_status, date_from, date_to, skip, limit)
    return {"total": total, "items": items}


@router.get("/{order_id}", response_model=OrderOut)
def read_one(order_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_order(db, order_id)


@router.put("/{order_id}", response_model=OrderOut)
def update(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return update_order(db, order_id, data)


@router.delete("/{order_id}", status_code=204)
def delete(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    delete_order(db, order_id)
