# S&P 500 Analysis Dashboard

A full-stack decision-support tool for long-term Dollar-Cost Averaging (DCA) investing. Fetches S&P 500 data, computes technical indicators, produces an explainable Market Heat Score (0-100), and generates score-based DCA recommendations.

**This is NOT a trading bot.** It is an informational dashboard for long-term investors.

![Dashboard Screenshot](https://raw.githubusercontent.com/ersinedinc/Spy500/main/screenshot.png)

## Features

- **Market Heat Score (0-100)** — Weighted composite of 8 technical indicators with full breakdown
- **Market Regime Detection** — Trend Up / Trend Down / Range classification with risk flags
- **DCA Action Plan** — Dynamic contribution multiplier based on market conditions
- **Interactive Charts** — Candlestick price chart with MA/BB overlays, RSI, Drawdown, Volatility
- **Full Report** — Markdown report with analysis, key levels, and disclaimer
- **Auto Refresh** — Polls every 5 minutes, with manual refresh button

## Architecture

```
React Frontend (Vite + TypeScript + Tailwind + TradingView Lightweight Charts v5)
        | REST API (JSON)
FastAPI Backend (Python)
        |
Data Pipeline + Indicators + Score Engine
        |
Local Storage (parquet files)
        |
yfinance (VUAA.AS / SPY)
```

## Heat Score Components

| Component | Weight | Description |
|-----------|--------|-------------|
| RSI(14) | 15% | Relative Strength Index |
| MACD Histogram | 10% | Momentum direction |
| Bollinger Band Position | 10% | Price position within bands |
| MA Trend (SMA50 distance) | 15% | Short-term trend strength |
| Drawdown | 15% | Distance from all-time high |
| Volatility | 10% | Annualized rolling volatility (inverted) |
| 5-Day Momentum | 10% | Short-term price change |
| Distance to MA200 | 15% | Long-term trend position |

**Score interpretation:** 0-30 = Fear/Opportunity, 30-45 = Cooling, 45-65 = Neutral, 65-100 = Hot/Risky

## DCA Brackets

| Score Range | Multiplier | Action |
|-------------|-----------|--------|
| 0-30 | 2.0x | Aggressive Buy |
| 30-45 | 1.25x | Moderate Buy |
| 45-65 | 1.0x | Normal DCA |
| 65-80 | 0.75x | Reduce |
| 80-100 | 0.5x | Minimal |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend starts on **http://localhost:8000** and fetches market data on first launch (~5 seconds).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend starts on **http://localhost:5173** and proxies API requests to the backend.

### Run Tests

```bash
cd backend
pytest -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Status, ticker, data info |
| GET | `/api/heat-score` | Score + component breakdown |
| GET | `/api/indicators?timeframe=daily\|hourly` | OHLCV + all indicator time series |
| GET | `/api/regime` | Market regime + risk flags |
| GET | `/api/action-plan` | DCA recommendation |
| GET | `/api/report` | Full markdown report |
| POST | `/api/refresh` | Force data refresh |

## Configuration

All parameters are tunable in `backend/config.yaml`:
- Ticker symbols and fallback logic
- Indicator periods (RSI, SMA, MACD, etc.)
- Heat score weights and normalization ranges
- DCA base amount, currency, and bracket thresholds
- CORS origins and API settings

## Tech Stack

**Backend:** Python, FastAPI, pandas, NumPy, ta (technical analysis), yfinance, PyArrow

**Frontend:** React, TypeScript, Vite, Tailwind CSS, TradingView Lightweight Charts v5, TanStack React Query

## Known Limitations

- yfinance provides delayed data (15-20 min for non-US exchanges)
- VUAA.AS hourly data unavailable on Yahoo Finance — falls back to SPY
- No historical score database (scores computed on the fly)
- No authentication (designed for local use)
- Heat Score normalization ranges may need recalibration in extreme markets

## Disclaimer

This tool is for **informational and educational purposes only**. It is not financial advice. Always consult a qualified financial advisor before making investment decisions.
