"""
app/schemas/order.py
Pydantic v2 schemas for Order/Dispatch endpoints.
"""
from datetime import date, datetime, time
from typing import Literal, Optional

from pydantic import BaseModel, Field


EntityType = Literal["mansuri_enterprises", "aman_stone_crusher"]
OrderStatus = Literal["Delivered", "Pending"]
PaymentStatus = Literal["Done", "Partial Pending", "Full Pending"]


class OrderCreate(BaseModel):
    entity_type: EntityType
    material_name: str = Field(..., min_length=1, max_length=120)
    material_type: Optional[str] = None
    record_date: date
    record_time: Optional[time] = None
    customer_name: str = Field(..., min_length=1, max_length=120)
    customer_location: Optional[str] = None
    shopkeeper: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    status: OrderStatus = "Pending"
    payment_amount: Optional[float] = None
    payment_status: PaymentStatus = "Full Pending"


class OrderUpdate(BaseModel):
    material_name: Optional[str] = None
    material_type: Optional[str] = None
    record_date: Optional[date] = None
    record_time: Optional[time] = None
    customer_name: Optional[str] = None
    customer_location: Optional[str] = None
    shopkeeper: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    status: Optional[OrderStatus] = None
    payment_amount: Optional[float] = None
    payment_status: Optional[PaymentStatus] = None


class OrderOut(BaseModel):
    id: int
    entity_type: str
    material_name: str
    material_type: Optional[str]
    record_date: date
    record_time: Optional[time]
    customer_name: str
    customer_location: Optional[str]
    shopkeeper: Optional[str]
    vehicle_no: Optional[str]
    driver_name: Optional[str]
    driver_phone: Optional[str]
    status: str
    payment_amount: Optional[float]
    payment_status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    total: int
    items: list[OrderOut]
