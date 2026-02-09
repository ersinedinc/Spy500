from app.services.regime_detector import detect_regime
from app.models.enums import MarketRegime, RiskFlag


def test_bullish_regime():
    latest = {
        "Close": 550,
        "SMA_50": 530,
        "SMA_200": 500,
        "RSI_14": 55,
        "volatility": 0.15,
        "drawdown": -0.02,
    }
    result = detect_regime(latest)
    assert result.regime == MarketRegime.TREND_UP
    assert result.confidence >= 0.7


def test_bearish_regime():
    latest = {
        "Close": 400,
        "SMA_50": 430,
        "SMA_200": 460,
        "RSI_14": 35,
        "volatility": 0.20,
        "drawdown": -0.08,
    }
    result = detect_regime(latest)
    assert result.regime == MarketRegime.TREND_DOWN


def test_range_regime():
    latest = {
        "Close": 500,
        "SMA_50": 510,
        "SMA_200": 490,
        "RSI_14": 50,
        "volatility": 0.15,
        "drawdown": -0.03,
    }
    result = detect_regime(latest)
    assert result.regime == MarketRegime.RANGE


def test_overbought_flag():
    latest = {
        "Close": 550,
        "SMA_50": 530,
        "SMA_200": 500,
        "RSI_14": 75,
        "volatility": 0.15,
        "drawdown": -0.01,
    }
    result = detect_regime(latest)
    assert RiskFlag.OVERBOUGHT in result.risk_flags


def test_oversold_flag():
    latest = {
        "Close": 400,
        "SMA_50": 430,
        "SMA_200": 460,
        "RSI_14": 25,
        "volatility": 0.15,
        "drawdown": -0.05,
    }
    result = detect_regime(latest)
    assert RiskFlag.OVERSOLD in result.risk_flags


def test_high_volatility_flag():
    latest = {
        "Close": 500,
        "SMA_50": 500,
        "SMA_200": 500,
        "RSI_14": 50,
        "volatility": 0.35,
        "drawdown": -0.03,
    }
    result = detect_regime(latest)
    assert RiskFlag.HIGH_VOLATILITY in result.risk_flags


def test_extreme_drawdown_flag():
    latest = {
        "Close": 400,
        "SMA_50": 450,
        "SMA_200": 480,
        "RSI_14": 30,
        "volatility": 0.25,
        "drawdown": -0.15,
    }
    result = detect_regime(latest)
    assert RiskFlag.EXTREME_DRAWDOWN in result.risk_flags


def test_golden_cross():
    latest = {
        "Close": 500,
        "SMA_50": 501,
        "SMA_200": 500,
        "RSI_14": 55,
        "volatility": 0.15,
        "drawdown": -0.01,
    }
    prev = {
        "SMA_50": 499,
        "SMA_200": 500,
    }
    result = detect_regime(latest, prev)
    assert RiskFlag.GOLDEN_CROSS in result.risk_flags


def test_death_cross():
    latest = {
        "Close": 500,
        "SMA_50": 499,
        "SMA_200": 500,
        "RSI_14": 45,
        "volatility": 0.15,
        "drawdown": -0.03,
    }
    prev = {
        "SMA_50": 501,
        "SMA_200": 500,
    }
    result = detect_regime(latest, prev)
    assert RiskFlag.DEATH_CROSS in result.risk_flags
