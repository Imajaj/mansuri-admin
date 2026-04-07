"""
app/schemas/inventory.py
Pydantic v2 schemas for Inventory endpoints.
"""
from datetime import date, datetime, time
from typing import Literal, Optional

from pydantic import BaseModel, Field


EntityType = Literal["mansuri_enterprises", "aman_stone_crusher"]
InventoryStatus = Literal["Received", "Pending"]


class InventoryCreate(BaseModel):
    entity_type: EntityType
    material_name: str = Field(..., min_length=1, max_length=120)
    material_type: Optional[str] = None
    record_date: date
    record_time: Optional[time] = None
    received_by: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    status: InventoryStatus = "Pending"

    # Mansuri Enterprises
    dealer_name: Optional[str] = None
    dealer_location: Optional[str] = None

    # Aman Stone Crusher
    incharge_name: Optional[str] = None
    incharge_location: Optional[str] = None


class InventoryUpdate(BaseModel):
    material_name: Optional[str] = None
    material_type: Optional[str] = None
    record_date: Optional[date] = None
    record_time: Optional[time] = None
    received_by: Optional[str] = None
    vehicle_no: Optional[str] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    status: Optional[InventoryStatus] = None
    dealer_name: Optional[str] = None
    dealer_location: Optional[str] = None
    incharge_name: Optional[str] = None
    incharge_location: Optional[str] = None


class InventoryOut(BaseModel):
    id: int
    entity_type: str
    material_name: str
    material_type: Optional[str]
    record_date: date
    record_time: Optional[time]
    received_by: Optional[str]
    vehicle_no: Optional[str]
    driver_name: Optional[str]
    driver_phone: Optional[str]
    status: str
    dealer_name: Optional[str]
    dealer_location: Optional[str]
    incharge_name: Optional[str]
    incharge_location: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class InventoryListResponse(BaseModel):
    total: int
    items: list[InventoryOut]
