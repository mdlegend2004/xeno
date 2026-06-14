"""
crm-service/app/main.py — FastAPI application entry point.

Design:
  - CORS is wide-open ("*") for local dev. In production, restrict
    allow_origins to your actual frontend domain.
  - StaticFiles mount is commented out — uncomment after running
    `npm run build` inside crm-service/frontend/.
  - All routers share a consistent /api/* prefix for easy nginx proxying.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles  # Uncomment after frontend build

from app.api.routes import customers, campaigns, segments, receipts, analytics, ai

app = FastAPI(
    title="BrewCo CRM API",
    version="1.0.0",
    description="AI-native Mini CRM for BrewCo coffee chain",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(segments.router,  prefix="/api/segments",  tags=["segments"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(receipts.router,  prefix="/api/receipts",  tags=["receipts"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(ai.router,        prefix="/api/ai",         tags=["ai"])


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok", "service": "crm"}


# ── Frontend (uncomment after: cd frontend && npm run build) ──────────────────
# app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
