"""
schemas/segment.py — Pydantic v2 schemas for Segment endpoints.

SegmentRules / SegmentCondition are also used by the AI service
to validate the JSON returned by OpenAI before saving to DB.
Using Any for condition values lets the rules engine handle
strings, numbers, lists, and date-relative integers uniformly.
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, List, Literal, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.schemas.customer import CustomerResponse


class SegmentCondition(BaseModel):
    field: str
    op: str
    value: Any


class SegmentRules(BaseModel):
    operator: Literal["AND", "OR"]
    conditions: List[SegmentCondition]


class SegmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    rules: SegmentRules
    ai_generated: bool = False


class SegmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: Optional[str]
    rules: Any  # Raw JSON from DB
    ai_generated: bool
    customer_count: int
    created_at: datetime


class SegmentPreviewResponse(BaseModel):
    count: int
    sample_customers: List[CustomerResponse]
