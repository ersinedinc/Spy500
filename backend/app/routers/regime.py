from fastapi import APIRouter, HTTPException, Query

from app.schemas import RegimeResponse
from app.services.orchestrator import get_state, get_default_ticker
from app.i18n import t as tr, translate_items, translate_dict

router = APIRouter()


@router.get("/regime", response_model=RegimeResponse)
def get_regime(ticker: str = Query(None), lang: str = Query("en")):
    tk = ticker or get_default_ticker()
    s = get_state(tk)
    if not s.ready or s.regime is None:
        raise HTTPException(status_code=503, detail="Data not ready")

    return RegimeResponse(
        regime=tr(s.regime.regime.value, lang),
        risk_flags=translate_items([f.value for f in s.regime.risk_flags], lang),
        confidence=s.regime.confidence,
        details=translate_dict(s.regime.details, lang),
    )
