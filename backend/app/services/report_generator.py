import logging
from datetime import datetime, timezone

from app.services.heat_score import HeatScoreResult
from app.services.regime_detector import RegimeResult
from app.services.dca_engine import DCAResult

logger = logging.getLogger(__name__)


def generate_report(
    heat: HeatScoreResult,
    regime: RegimeResult,
    dca: DCAResult,
    active_ticker: str,
    used_fallback: bool,
    fallback_reason: str | None,
    latest: dict,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# S&P 500 Market Analysis Report",
        f"**Generated:** {now}",
        "",
        "---",
        "",
        "## Data Source",
        f"- **Active Ticker:** {active_ticker}",
    ]

    if used_fallback:
        lines.append(f"- **Fallback Used:** Yes")
        lines.append(f"- **Reason:** {fallback_reason}")
    else:
        lines.append(f"- **Fallback Used:** No (primary ticker active)")

    close = latest.get("Close", 0)
    lines.extend([
        f"- **Latest Close:** {close:.2f}",
        "",
        "---",
        "",
        "## Heat Score",
        f"**Score: {heat.score:.1f} / 100 ({heat.label})**",
        "",
        "| Component | Raw Value | Normalized | Weight | Contribution |",
        "|-----------|-----------|------------|--------|--------------|",
    ])

    for c in heat.components:
        if abs(c.raw_value) < 1:
            raw_fmt = f"{c.raw_value:.4f}"
        else:
            raw_fmt = f"{c.raw_value:.2f}"
        lines.append(
            f"| {c.name} | {raw_fmt} | {c.normalized:.1f} | "
            f"{c.weight:.0%} | {c.contribution:.1f} |"
        )

    total_weight = sum(c.weight for c in heat.components)
    lines.extend([
        f"| **Total** | | | **{total_weight:.0%}** | **{heat.score:.1f}** |",
        "",
        "---",
        "",
        "## Market Regime",
        f"- **Regime:** {regime.regime.value}",
        f"- **Confidence:** {regime.confidence:.0%}",
    ])

    if regime.risk_flags:
        flags_str = ", ".join(f.value for f in regime.risk_flags)
        lines.append(f"- **Risk Flags:** {flags_str}")
    else:
        lines.append("- **Risk Flags:** None")

    lines.append("")
    for key, detail in regime.details.items():
        lines.append(f"- *{key}:* {detail}")

    lines.extend([
        "",
        "---",
        "",
        "## DCA Recommendation",
        f"- **Action:** {dca.action}",
        f"- **Multiplier:** {dca.multiplier}x",
        f"- **Base Amount:** {dca.currency} {dca.base_amount:.2f}",
        f"- **Suggested Amount:** {dca.currency} {dca.suggested_amount:.2f}",
        "",
        "**Reasoning:**",
    ])
    for r in dca.reasoning:
        lines.append(f"- {r}")

    # Support / Resistance zones
    sma50 = latest.get("SMA_50")
    sma200 = latest.get("SMA_200")
    bbl = latest.get("BBL_20_2.0")
    bbu = latest.get("BBU_20_2.0")

    lines.extend([
        "",
        "---",
        "",
        "## Key Levels",
    ])
    if sma50 is not None:
        lines.append(f"- **SMA 50:** {sma50:.2f}")
    if sma200 is not None:
        lines.append(f"- **SMA 200:** {sma200:.2f}")
    if bbl is not None:
        lines.append(f"- **Bollinger Lower:** {bbl:.2f}")
    if bbu is not None:
        lines.append(f"- **Bollinger Upper:** {bbu:.2f}")

    lines.extend([
        "",
        "---",
        "",
        "## Disclaimer",
        "",
        "> This report is generated automatically for informational and educational "
        "purposes only. It is **not financial advice**. The Heat Score and DCA "
        "recommendations are based on technical indicators with hardcoded normalization "
        "ranges that may not be appropriate in all market conditions. Past performance "
        "does not guarantee future results. Always consult a qualified financial "
        "advisor before making investment decisions.",
    ])

    report = "\n".join(lines)
    logger.info(f"Report generated: {len(report)} chars")
    return report
