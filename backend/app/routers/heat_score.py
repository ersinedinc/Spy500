from fastapi import APIRouter, HTTPException

from app.schemas import HeatScoreResponse, ScoreComponentSchema
from app.services.orchestrator import get_state

router = APIRouter()


@router.get("/heat-score", response_model=HeatScoreResponse)
def get_heat_score():
    s = get_state()
    if not s.ready or s.heat_score is None:
        raise HTTPException(status_code=503, detail="Data not ready")

    return HeatScoreResponse(
        score=s.heat_score.score,
        label=s.heat_score.label,
        components=[
            ScoreComponentSchema(
                name=c.name,
                raw_value=c.raw_value,
                normalized=c.normalized,
                weight=c.weight,
                contribution=c.contribution,
                description=c.description,
            )
            for c in s.heat_score.components
        ],
    )
