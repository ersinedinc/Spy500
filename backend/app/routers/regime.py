from fastapi import APIRouter, HTTPException, Query

from app.schemas import RegimeResponse
from app.services.orchestrator import get_state, get_default_ticker

router = APIRouter()


@router.get("/regime", response_model=RegimeResponse)
def get_regime(ticker: str = Query(None)):
    t = ticker or get_default_ticker()
    s = get_state(t)
    if not s.ready or s.regime is None:
        raise HTTPException(status_code=503, detail="Data not ready")

    return RegimeResponse(
        regime=s.regime.regime.value,
        risk_flags=[f.value for f in s.regime.risk_flags],
        confidence=s.regime.confidence,
        details=s.regime.details,
    )
