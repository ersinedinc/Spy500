import logging

import numpy as np
import pandas as pd
import ta as ta_lib

from app.config import get_config

logger = logging.getLogger(__name__)


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or len(df) < 2:
        logger.warning("Not enough data to compute indicators")
        return df

    cfg = get_config()["indicators"]
    df = df.copy()

    close = df["Close"]
    high = df["High"]
    low = df["Low"]

    # RSI
    df["RSI_14"] = ta_lib.momentum.RSIIndicator(close, window=cfg["rsi_period"]).rsi()

    # SMAs
    for period in cfg["sma_periods"]:
        df[f"SMA_{period}"] = ta_lib.trend.SMAIndicator(close, window=period).sma_indicator()

    # EMAs
    for period in cfg["ema_periods"]:
        df[f"EMA_{period}"] = ta_lib.trend.EMAIndicator(close, window=period).ema_indicator()

    # MACD
    macd = ta_lib.trend.MACD(
        close,
        window_slow=cfg["macd_slow"],
        window_fast=cfg["macd_fast"],
        window_sign=cfg["macd_signal"],
    )
    df["MACD_12_26_9"] = macd.macd()
    df["MACDs_12_26_9"] = macd.macd_signal()
    df["MACDh_12_26_9"] = macd.macd_diff()

    # Bollinger Bands
    bb = ta_lib.volatility.BollingerBands(
        close, window=cfg["bb_period"], window_dev=cfg["bb_std"]
    )
    df["BBU_20_2.0"] = bb.bollinger_hband()
    df["BBM_20_2.0"] = bb.bollinger_mavg()
    df["BBL_20_2.0"] = bb.bollinger_lband()
    df["BBP_20_2.0"] = bb.bollinger_pband()

    # ATR
    df["ATRr_14"] = ta_lib.volatility.AverageTrueRange(
        high, low, close, window=cfg["atr_period"]
    ).average_true_range()

    # Log returns
    df["log_return"] = np.log(close / close.shift(1))

    # Rolling volatility (annualized)
    window = cfg["volatility_window"]
    trading_days = cfg["trading_days_per_year"]
    df["volatility"] = df["log_return"].rolling(window).std() * np.sqrt(trading_days)

    # Drawdown
    cummax = close.cummax()
    df["drawdown"] = (close - cummax) / cummax

    # Distance to MA50 and MA200
    if "SMA_50" in df.columns:
        df["dist_ma50"] = (close - df["SMA_50"]) / df["SMA_50"]
    if "SMA_200" in df.columns:
        df["dist_ma200"] = (close - df["SMA_200"]) / df["SMA_200"]

    # 5-day momentum (percent change)
    df["momentum_5d"] = close.pct_change(5)

    logger.info(f"Indicators computed: {len(df)} rows, {len(df.columns)} columns")
    return df
