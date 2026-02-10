from fastapi import APIRouter

from app.config import get_config
from app.schemas import TickersResponse, TickerInfo

router = APIRouter()


@router.get("/tickers", response_model=TickersResponse)
def get_tickers():
    cfg = get_config()
    etfs = cfg.get("etfs", [])
    default = etfs[0]["symbol"] if etfs else cfg["tickers"]["fallback"]
    return TickersResponse(
        tickers=[TickerInfo(symbol=e["symbol"], name=e["name"]) for e in etfs],
        default=default,
    )
