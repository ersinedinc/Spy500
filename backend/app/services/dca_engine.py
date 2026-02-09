import logging
from dataclasses import dataclass

from app.config import get_config

logger = logging.getLogger(__name__)


@dataclass
class DCAResult:
    action: str
    base_amount: float
    multiplier: float
    suggested_amount: float
    currency: str
    reasoning: list[str]


def compute_dca(score: float, score_label: str, regime_name: str) -> DCAResult:
    cfg = get_config()["dca"]
    base = cfg["base_amount"]
    currency = cfg["currency"]
    brackets = cfg["brackets"]

    action = "Normal DCA"
    multiplier = 1.0

    for bracket in brackets:
        lo, hi = bracket["range"]
        if lo <= score < hi or (hi == 100 and score <= hi):
            action = bracket["label"]
            multiplier = bracket["multiplier"]
            break

    suggested = round(base * multiplier, 2)

    reasoning = [
        f"Heat Score is {score:.1f} ({score_label})",
        f"Market regime: {regime_name}",
        f"Score falls in bracket [{lo}-{hi}] → {action} ({multiplier}x)",
        f"Base monthly contribution: {currency} {base:.2f}",
        f"Suggested contribution: {currency} {suggested:.2f}",
    ]

    if multiplier > 1.0:
        reasoning.append(
            "Market conditions suggest opportunity — consider increasing allocation"
        )
    elif multiplier < 1.0:
        reasoning.append(
            "Market conditions suggest caution — consider reducing allocation"
        )
    else:
        reasoning.append(
            "Market conditions are neutral — maintain regular DCA schedule"
        )

    logger.info(f"DCA: {action}, {multiplier}x, {currency} {suggested}")

    return DCAResult(
        action=action,
        base_amount=base,
        multiplier=multiplier,
        suggested_amount=suggested,
        currency=currency,
        reasoning=reasoning,
    )
