from fastapi import APIRouter, HTTPException

from app.schemas import ReportResponse
from app.services.orchestrator import get_state

router = APIRouter()


@router.get("/report", response_model=ReportResponse)
def get_report():
    s = get_state()
    if not s.ready or not s.report:
        raise HTTPException(status_code=503, detail="Data not ready")

    return ReportResponse(markdown=s.report)
