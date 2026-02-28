from fastapi import APIRouter, HTTPException, Query

from app.schemas import ReportResponse
from app.services.orchestrator import get_state, get_default_ticker
from app.i18n import translate_report

router = APIRouter()


@router.get("/report", response_model=ReportResponse)
def get_report(ticker: str = Query(None), lang: str = Query("en")):
    tk = ticker or get_default_ticker()
    s = get_state(tk)
    if not s.ready or not s.report:
        raise HTTPException(status_code=503, detail="Data not ready")

    return ReportResponse(markdown=translate_report(s.report, lang))
