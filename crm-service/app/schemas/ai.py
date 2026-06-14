"""
schemas/ai.py — Pydantic v2 schemas for AI endpoints.

These schemas validate the structured JSON returned by gpt-4o-mini
before it's used to create DB records or returned to the client.
"""

from __future__ import annotations
from typing import List, Literal
from pydantic import BaseModel

from app.schemas.segment import SegmentRules
from app.schemas.customer import CustomerResponse
from app.schemas.campaign import CampaignResponse
from app.schemas.segment import SegmentResponse


# ── /api/ai/build-segment ────────────────────────────────────────────────────

class BuildSegmentRequest(BaseModel):
    prompt: str


class BuildSegmentResponse(BaseModel):
    rules: SegmentRules
    preview_count: int
    sample_customers: List[CustomerResponse]


# ── /api/ai/write-message ────────────────────────────────────────────────────

class WriteMessageRequest(BaseModel):
    brand_name: str
    segment_description: str
    channel: str
    goal: str


class MessageVariant(BaseModel):
    tone: str
    message: str


class WriteMessageResponse(BaseModel):
    variants: List[MessageVariant]


# ── /api/ai/insights/{campaign_id} ──────────────────────────────────────────

class InsightItem(BaseModel):
    type: Literal["insight", "recommendation"]
    text: str


class CampaignInsightsResponse(BaseModel):
    insights: List[InsightItem]


# ── /api/ai/create-campaign ──────────────────────────────────────────────────

class CreateCampaignRequest(BaseModel):
    intent: str


class CreateCampaignResponse(BaseModel):
    campaign: CampaignResponse
    segment: SegmentResponse
    message_variants: List[MessageVariant]
    ready_to_launch: bool
