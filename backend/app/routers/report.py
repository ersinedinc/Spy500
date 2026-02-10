from fastapi import APIRouter, HTTPException, Query

from app.schemas import ReportResponse
from app.services.orchestrator import get_state, get_default_ticker

router = APIRouter()


@router.get("/report", response_model=ReportResponse)
def get_report(ticker: str = Query(None)):
    t = ticker or get_default_ticker()
    s = get_state(t)
    if not s.ready or not s.report:
        raise HTTPException(status_code=503, detail="Data not ready")

    return ReportResponse(markdown=s.report)
