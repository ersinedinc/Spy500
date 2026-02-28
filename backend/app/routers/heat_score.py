from fastapi import APIRouter, HTTPException, Query

from app.schemas import HeatScoreResponse, ScoreComponentSchema
from app.services.orchestrator import get_state, get_default_ticker
from app.i18n import t as tr, translate_description

router = APIRouter()


@router.get("/heat-score", response_model=HeatScoreResponse)
def get_heat_score(ticker: str = Query(None), lang: str = Query("en")):
    tk = ticker or get_default_ticker()
    s = get_state(tk)
    if not s.ready or s.heat_score is None:
        raise HTTPException(status_code=503, detail="Data not ready")

    return HeatScoreResponse(
        score=s.heat_score.score,
        label=tr(s.heat_score.label, lang),
        components=[
            ScoreComponentSchema(
                name=tr(c.name, lang),
                raw_value=c.raw_value,
                normalized=c.normalized,
                weight=c.weight,
                contribution=c.contribution,
                description=translate_description(c.description, lang),
            )
            for c in s.heat_score.components
        ],
    )
