import pandas as pd
from app.services.indicator_engine import compute_indicators


def test_indicator_columns(sample_ohlcv):
    df = compute_indicators(sample_ohlcv)

    expected_cols = [
        "RSI_14", "SMA_20", "SMA_50", "SMA_200",
        "EMA_20", "EMA_50",
        "MACD_12_26_9", "MACDs_12_26_9", "MACDh_12_26_9",
        "BBU_20_2.0", "BBM_20_2.0", "BBL_20_2.0", "BBP_20_2.0",
        "ATRr_14",
        "log_return", "volatility", "drawdown",
        "dist_ma50", "dist_ma200", "momentum_5d",
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"


def test_rsi_bounded(sample_ohlcv):
    df = compute_indicators(sample_ohlcv)
    rsi = df["RSI_14"].dropna()
    assert (rsi >= 0).all(), "RSI should be >= 0"
    assert (rsi <= 100).all(), "RSI should be <= 100"


def test_drawdown_negative(sample_ohlcv):
    df = compute_indicators(sample_ohlcv)
    dd = df["drawdown"].dropna()
    assert (dd <= 0).all(), "Drawdown should always be <= 0"


def test_sma_computed(sample_ohlcv):
    df = compute_indicators(sample_ohlcv)
    # SMA_200 requires 200 periods, but SMA_20 should have values
    sma20 = df["SMA_20"].dropna()
    assert len(sma20) > 0, "SMA_20 should have values"


def test_empty_dataframe():
    df = compute_indicators(pd.DataFrame())
    assert df.empty
