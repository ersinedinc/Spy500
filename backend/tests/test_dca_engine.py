from app.services.dca_engine import compute_dca


def test_aggressive_buy():
    result = compute_dca(15.0, "Fear", "Trend Down")
    assert result.multiplier == 2.0
    assert result.action == "Aggressive Buy"
    assert result.suggested_amount == 1000.0


def test_moderate_buy():
    result = compute_dca(37.0, "Cooling", "Range")
    assert result.multiplier == 1.25
    assert result.action == "Moderate Buy"


def test_normal_dca():
    result = compute_dca(55.0, "Neutral", "Range")
    assert result.multiplier == 1.0
    assert result.action == "Normal DCA"
    assert result.suggested_amount == 500.0


def test_reduce():
    result = compute_dca(72.0, "Hot", "Trend Up")
    assert result.multiplier == 0.75
    assert result.action == "Reduce"


def test_minimal():
    result = compute_dca(90.0, "Hot", "Trend Up")
    assert result.multiplier == 0.5
    assert result.action == "Minimal"
    assert result.suggested_amount == 250.0


def test_boundary_30():
    result = compute_dca(30.0, "Cooling", "Range")
    assert result.multiplier == 1.25


def test_boundary_0():
    result = compute_dca(0.0, "Fear", "Trend Down")
    assert result.multiplier == 2.0


def test_boundary_100():
    result = compute_dca(100.0, "Hot", "Trend Up")
    assert result.multiplier == 0.5


def test_reasoning_populated():
    result = compute_dca(50.0, "Neutral", "Range")
    assert len(result.reasoning) > 0
    assert result.currency == "EUR"
