from fastapi import APIRouter, HTTPException

from app.schemas import ActionPlanResponse
from app.services.orchestrator import get_state

router = APIRouter()


@router.get("/action-plan", response_model=ActionPlanResponse)
def get_action_plan():
    s = get_state()
    if not s.ready or s.dca is None:
        raise HTTPException(status_code=503, detail="Data not ready")

    return ActionPlanResponse(
        action=s.dca.action,
        base_amount=s.dca.base_amount,
        multiplier=s.dca.multiplier,
        suggested_amount=s.dca.suggested_amount,
        currency=s.dca.currency,
        reasoning=s.dca.reasoning,
    )
