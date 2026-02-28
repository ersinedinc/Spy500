from fastapi import APIRouter, HTTPException, Query

from app.schemas import ActionPlanResponse
from app.services.orchestrator import get_state, get_default_ticker
from app.i18n import t as tr, translate_reasoning

router = APIRouter()


@router.get("/action-plan", response_model=ActionPlanResponse)
def get_action_plan(ticker: str = Query(None), lang: str = Query("en")):
    tk = ticker or get_default_ticker()
    s = get_state(tk)
    if not s.ready or s.dca is None:
        raise HTTPException(status_code=503, detail="Data not ready")

    return ActionPlanResponse(
        action=tr(s.dca.action, lang),
        base_amount=s.dca.base_amount,
        multiplier=s.dca.multiplier,
        suggested_amount=s.dca.suggested_amount,
        currency=s.dca.currency,
        reasoning=translate_reasoning(s.dca.reasoning, lang),
    )
