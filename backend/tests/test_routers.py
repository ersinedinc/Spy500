import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.services.orchestrator import PipelineState
from app.services.regime_detector import RegimeResult
from app.services.heat_score import HeatScoreResult, ScoreComponent
from app.services.dca_engine import DCAResult
from app.models.enums import MarketRegime
import pandas as pd


def _mock_state():
    return PipelineState(
        active_ticker="SPY",
        used_fallback=True,
        fallback_reason="Test fallback",
        hourly_df=pd.DataFrame({"Close": [100.0]}),
        daily_df=pd.DataFrame({"Close": [100.0]}),
        regime=RegimeResult(
            regime=MarketRegime.RANGE,
            risk_flags=[],
            confidence=0.5,
            details={"trend": "test"},
        ),
        heat_score=HeatScoreResult(
            score=50.0,
            label="Neutral",
            components=[
                ScoreComponent(
                    name="RSI",
                    raw_value=50.0,
                    normalized=50.0,
                    weight=0.15,
                    contribution=7.5,
                    description="RSI(14) = 50.0",
                )
            ],
        ),
        dca=DCAResult(
            action="Normal DCA",
            base_amount=500,
            multiplier=1.0,
            suggested_amount=500,
            currency="EUR",
            reasoning=["Test reasoning"],
        ),
        report="# Test Report",
        last_refresh="2024-01-01T00:00:00+00:00",
        ready=True,
    )


@pytest.fixture
def client():
    with patch("app.services.orchestrator.initialize"):
        with TestClient(app) as c:
            yield c


@pytest.fixture(autouse=True)
def mock_orchestrator_state():
    with patch("app.routers.health.get_state", return_value=_mock_state()):
        with patch("app.routers.heat_score.get_state", return_value=_mock_state()):
            with patch("app.routers.regime.get_state", return_value=_mock_state()):
                with patch("app.routers.action_plan.get_state", return_value=_mock_state()):
                    with patch("app.routers.report.get_state", return_value=_mock_state()):
                        yield


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["active_ticker"] == "SPY"
    assert data["ready"] is True


def test_heat_score(client):
    resp = client.get("/api/heat-score")
    assert resp.status_code == 200
    data = resp.json()
    assert 0 <= data["score"] <= 100
    assert "label" in data
    assert len(data["components"]) > 0


def test_regime(client):
    resp = client.get("/api/regime")
    assert resp.status_code == 200
    data = resp.json()
    assert "regime" in data
    assert "confidence" in data


def test_action_plan(client):
    resp = client.get("/api/action-plan")
    assert resp.status_code == 200
    data = resp.json()
    assert "action" in data
    assert "multiplier" in data
    assert "suggested_amount" in data


def test_report(client):
    resp = client.get("/api/report")
    assert resp.status_code == 200
    data = resp.json()
    assert "markdown" in data
    assert len(data["markdown"]) > 0
