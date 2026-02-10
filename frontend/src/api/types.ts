export interface TickerInfo {
  symbol: string;
  name: string;
}

export interface TickersResponse {
  tickers: TickerInfo[];
  default: string;
}

export interface HealthResponse {
  status: string;
  active_ticker: string;
  used_fallback: boolean;
  fallback_reason: string | null;
  last_refresh: string | null;
  hourly_rows: number;
  daily_rows: number;
  ready: boolean;
}

export interface ScoreComponent {
  name: string;
  raw_value: number;
  normalized: number;
  weight: number;
  contribution: number;
  description: string;
}

export interface HeatScoreResponse {
  score: number;
  label: string;
  components: ScoreComponent[];
}

export interface RegimeResponse {
  regime: string;
  risk_flags: string[];
  confidence: number;
  details: Record<string, string>;
}

export interface ActionPlanResponse {
  action: string;
  base_amount: number;
  multiplier: number;
  suggested_amount: number;
  currency: string;
  reasoning: string[];
}

export interface ReportResponse {
  markdown: string;
}

export interface OHLCVPoint {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface IndicatorPoint {
  time: string;
  value: number | null;
}

export interface IndicatorsResponse {
  ticker: string;
  timeframe: string;
  ohlcv: OHLCVPoint[];
  sma20: IndicatorPoint[];
  sma50: IndicatorPoint[];
  sma200: IndicatorPoint[];
  ema20: IndicatorPoint[];
  ema50: IndicatorPoint[];
  rsi: IndicatorPoint[];
  macd: IndicatorPoint[];
  macd_signal: IndicatorPoint[];
  macd_histogram: IndicatorPoint[];
  bb_upper: IndicatorPoint[];
  bb_middle: IndicatorPoint[];
  bb_lower: IndicatorPoint[];
  volatility: IndicatorPoint[];
  drawdown: IndicatorPoint[];
}
