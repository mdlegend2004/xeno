"""
services/campaign_service.py — Campaign launch orchestrator.

Design:
  - Called from POST /api/campaigns/{id}/launch via FastAPI BackgroundTasks.
    The endpoint returns immediately; this function runs in the background.
  - Messages are personalised per-customer before creating Communication rows.
  - Communications are batched in groups of 50 before calling the channel
    service, avoiding an overwhelming flood of individual HTTP calls.
  - Status updates happen per-batch so partial progress is persisted even
    if the service crashes mid-way through a large campaign.
"""

from __future__ import annotations
import logging
from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign
from app.models.communication import Communication
from app.models.customer import Customer
from app.models.segment import Segment
from app.services.segmentation import RulesEngine
from app.services import channel_client

logger = logging.getLogger(__name__)

BATCH_SIZE = 50  # messages per channel service call


async def launch_campaign(campaign_id: UUID, db: AsyncSession) -> None:
    """
    Full campaign launch:
      1. Resolve segment → customer IDs
      2. Create Communication rows (status=queued)
      3. Send in batches of BATCH_SIZE via channel_client
      4. Update Communication statuses from channel response
      5. Mark campaign as completed (or failed if no customers)
    """
    # ── 1. Fetch campaign ────────────────────────────────────────────────────
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()
    if not campaign:
        logger.error(f"[LAUNCH] Campaign {campaign_id} not found")
        return

    # ── 2. Fetch segment rules ───────────────────────────────────────────────
    if not campaign.segment_id:
        logger.error(f"[LAUNCH] Campaign {campaign_id} has no segment_id — cannot launch")
        campaign.status = "failed"
        await db.commit()
        return

    result = await db.execute(select(Segment).where(Segment.id == campaign.segment_id))
    segment = result.scalar_one_or_none()
    if not segment:
        logger.error(f"[LAUNCH] Segment {campaign.segment_id} not found for campaign {campaign_id}")
        campaign.status = "failed"
        await db.commit()
        return

    # ── 3. Resolve customer IDs from rules ───────────────────────────────────
    rules_engine = RulesEngine()
    customer_ids = await rules_engine.get_ids(db, segment.rules)

    if not customer_ids:
        logger.warning(f"[LAUNCH] No customers matched for campaign {campaign_id}")
        campaign.status = "failed"
        await db.commit()
        return

    logger.info(f"[LAUNCH] Targeting {len(customer_ids)} customers for campaign {campaign_id}")

    # ── 4. Create Communication rows ─────────────────────────────────────────
    communications: list[Communication] = []

    for cid in customer_ids:
        result = await db.execute(select(Customer).where(Customer.id == cid))
        customer = result.scalar_one_or_none()
        if not customer:
            continue

        # Simple personalisation: replace {name} placeholder
        personalised = campaign.message_template.replace("{name}", customer.name)

        comm = Communication(
            campaign_id=campaign_id,
            customer_id=cid,
            channel=campaign.channel,
            message=personalised,
            status="queued",
            external_id=str(uuid4()),  # unique ID shared with channel service
        )
        db.add(comm)
        communications.append(comm)

    await db.commit()

    # Mark campaign as running after all rows are committed
    campaign.status = "running"
    await db.commit()

    # ── 5. Send in batches ───────────────────────────────────────────────────
    for i in range(0, len(communications), BATCH_SIZE):
        batch = communications[i : i + BATCH_SIZE]

        # Build payload for channel service
        payload = []
        # We need customer records for recipient resolution — load them
        cust_map: dict[UUID, Customer] = {}
        for comm in batch:
            res = await db.execute(select(Customer).where(Customer.id == comm.customer_id))
            c = res.scalar_one_or_none()
            if c:
                cust_map[comm.customer_id] = c

        for comm in batch:
            c = cust_map.get(comm.customer_id)
            if not c:
                continue
            recipient = c.email if campaign.channel == "email" else (c.phone or c.email)
            payload.append({
                "external_id": comm.external_id,
                "recipient": recipient,
                "channel": comm.channel,
                "message": comm.message,
            })

        # Call channel service
        batch_result = await channel_client.send_batch(payload)

        # Update Communication statuses from response
        now = datetime.utcnow()
        for comm in batch:
            outcome = batch_result.get(comm.external_id, "failed")
            if outcome == "accepted":
                comm.status = "sent"
                comm.sent_at = now
            else:
                comm.status = "failed"

        await db.commit()
        logger.info(
            f"[LAUNCH] Batch {i // BATCH_SIZE + 1}: "
            f"{sum(1 for v in batch_result.values() if v == 'accepted')} sent, "
            f"{sum(1 for v in batch_result.values() if v == 'failed')} failed"
        )

    # ── 6. Finalise campaign ─────────────────────────────────────────────────
    campaign.status = "completed"
    await db.commit()
    logger.info(f"[LAUNCH] Campaign {campaign_id} completed")
