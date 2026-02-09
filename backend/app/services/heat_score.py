import logging
from dataclasses import dataclass

from app.config import get_config

logger = logging.getLogger(__name__)


@dataclass
class ScoreComponent:
    name: str
    raw_value: float
    normalized: float
    weight: float
    contribution: float
    description: str


@dataclass
class HeatScoreResult:
    score: float
    label: str
    components: list[ScoreComponent]


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _linear_map(value: float, in_lo: float, in_hi: float) -> float:
    """Map value from [in_lo, in_hi] to [0, 100]."""
    if in_hi == in_lo:
        return 50.0
    normalized = (value - in_lo) / (in_hi - in_lo) * 100.0
    return _clamp(normalized, 0.0, 100.0)


def compute_heat_score(latest: dict) -> HeatScoreResult:
    cfg = get_config()["heat_score"]
    weights = cfg["weights"]
    norm = cfg["normalization"]
    labels_cfg = cfg["labels"]

    components: list[ScoreComponent] = []

    # 1. RSI — direct 0-100 mapping
    rsi = latest.get("RSI_14", 50.0) or 50.0
    rsi_norm = _clamp(rsi, 0.0, 100.0)
    components.append(ScoreComponent(
        name="RSI",
        raw_value=rsi,
        normalized=rsi_norm,
        weight=weights["rsi"],
        contribution=rsi_norm * weights["rsi"],
        description=f"RSI(14) = {rsi:.1f}",
    ))

    # 2. MACD Histogram — clamped, linear to 0-100
    macd_h = latest.get("MACDh_12_26_9", 0.0) or 0.0
    macd_lo, macd_hi = norm["macd_clamp"]
    macd_clamped = _clamp(macd_h, macd_lo, macd_hi)
    macd_norm = _linear_map(macd_clamped, macd_lo, macd_hi)
    components.append(ScoreComponent(
        name="MACD Histogram",
        raw_value=macd_h,
        normalized=macd_norm,
        weight=weights["macd_histogram"],
        contribution=macd_norm * weights["macd_histogram"],
        description=f"MACD histogram = {macd_h:.4f} (clamped to [{macd_lo}, {macd_hi}])",
    ))

    # 3. Bollinger Band Position — BBP 0-1 scaled to 0-100
    bbp = latest.get("BBP_20_2.0", 0.5) or 0.5
    bbp_norm = _clamp(bbp * 100.0, 0.0, 100.0)
    components.append(ScoreComponent(
        name="BB Position",
        raw_value=bbp,
        normalized=bbp_norm,
        weight=weights["bb_position"],
        contribution=bbp_norm * weights["bb_position"],
        description=f"BB %B = {bbp:.3f} (0=lower band, 1=upper band)",
    ))

    # 4. MA Trend / SMA50 distance — [-10%, +10%] → [0, 100]
    dist_ma50 = latest.get("dist_ma50", 0.0) or 0.0
    ma_lo, ma_hi = norm["ma_trend_range"]
    ma_norm = _linear_map(dist_ma50, ma_lo, ma_hi)
    components.append(ScoreComponent(
        name="MA Trend",
        raw_value=dist_ma50,
        normalized=ma_norm,
        weight=weights["ma_trend"],
        contribution=ma_norm * weights["ma_trend"],
        description=f"Distance to SMA50 = {dist_ma50:.2%}",
    ))

    # 5. Drawdown — [-20%, 0%] → [0, 100]
    dd = latest.get("drawdown", 0.0) or 0.0
    dd_lo, dd_hi = norm["drawdown_range"]
    dd_norm = _linear_map(dd, dd_lo, dd_hi)
    components.append(ScoreComponent(
        name="Drawdown",
        raw_value=dd,
        normalized=dd_norm,
        weight=weights["drawdown"],
        contribution=dd_norm * weights["drawdown"],
        description=f"Drawdown = {dd:.2%} (0% = at high)",
    ))

    # 6. Volatility — [40%, 10%] → [0, 100] (inverted: high vol = low score)
    vol = latest.get("volatility", 0.2) or 0.2
    vol_lo, vol_hi = norm["volatility_range"]  # [0.40, 0.10]
    vol_norm = _linear_map(vol, vol_lo, vol_hi)
    components.append(ScoreComponent(
        name="Volatility",
        raw_value=vol,
        normalized=vol_norm,
        weight=weights["volatility"],
        contribution=vol_norm * weights["volatility"],
        description=f"Annualized volatility = {vol:.1%} (inverted: high vol → low score)",
    ))

    # 7. 5-day Momentum — [-5%, +5%] → [0, 100]
    mom = latest.get("momentum_5d", 0.0) or 0.0
    mom_lo, mom_hi = norm["momentum_range"]
    mom_norm = _linear_map(mom, mom_lo, mom_hi)
    components.append(ScoreComponent(
        name="5-Day Momentum",
        raw_value=mom,
        normalized=mom_norm,
        weight=weights["momentum_5d"],
        contribution=mom_norm * weights["momentum_5d"],
        description=f"5-day price change = {mom:.2%}",
    ))

    # 8. Distance to MA200 — [-15%, +15%] → [0, 100]
    dist_ma200 = latest.get("dist_ma200", 0.0) or 0.0
    d200_lo, d200_hi = norm["distance_ma200_range"]
    d200_norm = _linear_map(dist_ma200, d200_lo, d200_hi)
    components.append(ScoreComponent(
        name="Distance to MA200",
        raw_value=dist_ma200,
        normalized=d200_norm,
        weight=weights["distance_ma200"],
        contribution=d200_norm * weights["distance_ma200"],
        description=f"Distance to SMA200 = {dist_ma200:.2%}",
    ))

    # Final score
    score = _clamp(sum(c.contribution for c in components), 0.0, 100.0)

    # Determine label
    label = "Neutral"
    for lbl, (lo, hi) in labels_cfg.items():
        if lo <= score < hi or (hi == 100 and score == 100):
            label = lbl.replace("_", " ").title()
            break

    logger.info(f"Heat Score = {score:.1f} ({label})")

    return HeatScoreResult(score=score, label=label, components=components)
