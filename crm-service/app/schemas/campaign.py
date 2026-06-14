"""
schemas/campaign.py — Pydantic v2 schemas for Campaign endpoints.

CampaignStatsResponse computes rates as floats (0–100 scale).
Division-by-zero is guarded in the route handler by checking
denominators before dividing.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CampaignCreate(BaseModel):
    name: str
    segment_id: Optional[UUID] = None
    channel: str
    message_template: str
    ai_generated_message: bool = False


class CampaignResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    segment_id: Optional[UUID]
    channel: str
    message_template: str
    ai_generated_message: bool
    status: str
    scheduled_at: Optional[datetime]
    created_at: datetime


class CampaignStatsResponse(BaseModel):
    campaign_id: UUID
    name: str
    channel: str
    status: str

    # Raw counts
    sent: int
    delivered: int
    failed: int
    opened: int
    clicked: int
    converted: int

    # Computed rates (percentage, 0–100)
    delivery_rate: float
    open_rate: float
    click_rate: float
    conversion_rate: float
