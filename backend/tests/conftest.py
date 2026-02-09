import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_ohlcv() -> pd.DataFrame:
    """Generate synthetic OHLCV data (250 trading days)."""
    np.random.seed(42)
    n = 250
    dates = pd.bdate_range("2024-01-02", periods=n, tz="UTC")

    # Random walk for close prices starting at 500
    returns = np.random.normal(0.0004, 0.012, n)
    close = 500.0 * np.exp(np.cumsum(returns))

    # Build OHLCV
    high = close * (1 + np.abs(np.random.normal(0, 0.005, n)))
    low = close * (1 - np.abs(np.random.normal(0, 0.005, n)))
    open_ = close * (1 + np.random.normal(0, 0.003, n))
    volume = np.random.randint(1_000_000, 10_000_000, n).astype(float)

    df = pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume},
        index=dates,
    )
    df.index.name = "Datetime"
    return df


@pytest.fixture
def bullish_ohlcv() -> pd.DataFrame:
    """Generate strongly uptrending data."""
    np.random.seed(10)
    n = 250
    dates = pd.bdate_range("2024-01-02", periods=n, tz="UTC")

    # Consistent uptrend
    returns = np.random.normal(0.003, 0.008, n)
    close = 400.0 * np.exp(np.cumsum(returns))

    high = close * 1.005
    low = close * 0.995
    open_ = close * 0.999
    volume = np.random.randint(1_000_000, 10_000_000, n).astype(float)

    df = pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume},
        index=dates,
    )
    df.index.name = "Datetime"
    return df


@pytest.fixture
def bearish_ohlcv() -> pd.DataFrame:
    """Generate strongly downtrending data."""
    np.random.seed(20)
    n = 250
    dates = pd.bdate_range("2024-01-02", periods=n, tz="UTC")

    # Consistent downtrend
    returns = np.random.normal(-0.003, 0.008, n)
    close = 600.0 * np.exp(np.cumsum(returns))

    high = close * 1.005
    low = close * 0.995
    open_ = close * 1.001
    volume = np.random.randint(1_000_000, 10_000_000, n).astype(float)

    df = pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume},
        index=dates,
    )
    df.index.name = "Datetime"
    return df
