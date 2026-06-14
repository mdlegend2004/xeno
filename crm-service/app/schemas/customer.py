"""
schemas/customer.py — Pydantic v2 schemas for Customer endpoints.

Using model_config = ConfigDict(from_attributes=True) instead of
the deprecated Pydantic v1 class Config: orm_mode = True.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    city: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    tags: Optional[List[str]] = None


class OrderSummary(BaseModel):
    """Lightweight order summary embedded in CustomerResponse."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_name: Optional[str]
    product_category: Optional[str]
    amount: float
    status: str
    ordered_at: datetime


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str
    phone: Optional[str]
    city: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    total_spent: float
    purchase_count: int
    last_purchase_date: Optional[datetime]
    tags: Optional[List[str]]
    created_at: datetime
    orders: Optional[List[OrderSummary]] = None


class CustomerListResponse(BaseModel):
    items: List[CustomerResponse]
    total: int
    page: int
    limit: int
