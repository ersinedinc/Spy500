import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_config
from app.services.orchestrator import initialize
from app.routers import health, heat_score, indicators, regime, action_plan, report, tickers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting S&P 500 Analysis Dashboard...")
    initialize()
    logger.info("Initialization complete, API ready")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="S&P 500 Analysis Dashboard",
    version="1.0.0",
    lifespan=lifespan,
)

cfg = get_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg["api"]["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(heat_score.router, prefix="/api")
app.include_router(indicators.router, prefix="/api")
app.include_router(regime.router, prefix="/api")
app.include_router(action_plan.router, prefix="/api")
app.include_router(report.router, prefix="/api")
app.include_router(tickers.router, prefix="/api")
