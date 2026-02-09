import logging

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def validate(df: pd.DataFrame, label: str = "data") -> pd.DataFrame:
    if df.empty:
        logger.warning(f"[{label}] Empty dataframe, nothing to validate")
        return df

    original_len = len(df)

    # Sort by datetime index
    df = df.sort_index()

    # Remove duplicate timestamps (keep last)
    dup_count = df.index.duplicated(keep="last").sum()
    if dup_count > 0:
        logger.info(f"[{label}] Removing {dup_count} duplicate timestamps")
        df = df[~df.index.duplicated(keep="last")]

    # Remove rows with NaN in Close
    nan_close = df["Close"].isna().sum()
    if nan_close > 0:
        logger.info(f"[{label}] Removing {nan_close} rows with NaN Close")
        df = df.dropna(subset=["Close"])

    # Detect and remove price spikes (>10 std devs from rolling mean)
    if len(df) > 20:
        returns = df["Close"].pct_change()
        rolling_std = returns.rolling(20, min_periods=5).std()
        rolling_mean = returns.rolling(20, min_periods=5).mean()
        z_scores = (returns - rolling_mean) / rolling_std
        spikes = z_scores.abs() > 10
        spike_count = spikes.sum()
        if spike_count > 0:
            logger.warning(
                f"[{label}] Removing {spike_count} price spikes (>10 std devs)"
            )
            df = df[~spikes]

    # Log gaps in timestamps
    if len(df) > 1:
        time_diffs = df.index.to_series().diff()
        median_diff = time_diffs.median()
        large_gaps = time_diffs[time_diffs > median_diff * 5].dropna()
        if len(large_gaps) > 0:
            logger.info(
                f"[{label}] Found {len(large_gaps)} timestamp gaps "
                f"(>{median_diff * 5})"
            )

    removed = original_len - len(df)
    if removed > 0:
        logger.info(f"[{label}] Validation removed {removed} rows total")

    return df
