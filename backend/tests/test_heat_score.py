from app.services.heat_score import compute_heat_score


def test_score_bounded():
    latest = {
        "RSI_14": 50,
        "MACDh_12_26_9": 0.0,
        "BBP_20_2.0": 0.5,
        "dist_ma50": 0.0,
        "drawdown": 0.0,
        "volatility": 0.20,
        "momentum_5d": 0.0,
        "dist_ma200": 0.0,
    }
    result = compute_heat_score(latest)
    assert 0 <= result.score <= 100


def test_eight_components():
    latest = {
        "RSI_14": 50,
        "MACDh_12_26_9": 0.0,
        "BBP_20_2.0": 0.5,
        "dist_ma50": 0.0,
        "drawdown": 0.0,
        "volatility": 0.20,
        "momentum_5d": 0.0,
        "dist_ma200": 0.0,
    }
    result = compute_heat_score(latest)
    assert len(result.components) == 8


def test_weights_sum_to_one():
    latest = {
        "RSI_14": 50,
        "MACDh_12_26_9": 0.0,
        "BBP_20_2.0": 0.5,
        "dist_ma50": 0.0,
        "drawdown": 0.0,
        "volatility": 0.20,
        "momentum_5d": 0.0,
        "dist_ma200": 0.0,
    }
    result = compute_heat_score(latest)
    total_weight = sum(c.weight for c in result.components)
    assert abs(total_weight - 1.0) < 0.01


def test_fear_label():
    """Extreme fear conditions should give a low score."""
    latest = {
        "RSI_14": 15,
        "MACDh_12_26_9": -3.0,
        "BBP_20_2.0": 0.0,
        "dist_ma50": -0.15,
        "drawdown": -0.25,
        "volatility": 0.50,
        "momentum_5d": -0.08,
        "dist_ma200": -0.20,
    }
    result = compute_heat_score(latest)
    assert result.score < 30
    assert result.label == "Fear"


def test_hot_label():
    """Extreme greed conditions should give a high score."""
    latest = {
        "RSI_14": 85,
        "MACDh_12_26_9": 3.0,
        "BBP_20_2.0": 1.0,
        "dist_ma50": 0.15,
        "drawdown": 0.0,
        "volatility": 0.08,
        "momentum_5d": 0.08,
        "dist_ma200": 0.20,
    }
    result = compute_heat_score(latest)
    assert result.score > 65
    assert result.label == "Hot"


def test_neutral_conditions():
    """Middle-of-the-road values should give a neutral score."""
    latest = {
        "RSI_14": 50,
        "MACDh_12_26_9": 0.0,
        "BBP_20_2.0": 0.5,
        "dist_ma50": 0.0,
        "drawdown": -0.05,
        "volatility": 0.20,
        "momentum_5d": 0.0,
        "dist_ma200": 0.0,
    }
    result = compute_heat_score(latest)
    assert 30 <= result.score <= 70
