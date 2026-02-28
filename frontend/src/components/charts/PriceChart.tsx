import { useCallback } from 'react';
import { CandlestickSeries, LineSeries, type IChartApi } from 'lightweight-charts';
import ChartContainer from './ChartContainer';
import { useTranslation } from '../../i18n';
import type { IndicatorsResponse } from '../../api/types';

interface PriceChartProps {
  data: IndicatorsResponse;
}

function parseTime(iso: string): string {
  return iso.split('T')[0];
}

export default function PriceChart({ data }: PriceChartProps) {
  const { t } = useTranslation();

  const setupChart = useCallback((chart: IChartApi) => {
    // Candlestick series
    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#22c55e',
      downColor: '#ef4444',
      borderDownColor: '#ef4444',
      borderUpColor: '#22c55e',
      wickDownColor: '#ef4444',
      wickUpColor: '#22c55e',
    });

    candleSeries.setData(
      data.ohlcv.map((p) => ({
        time: parseTime(p.time),
        open: p.open,
        high: p.high,
        low: p.low,
        close: p.close,
      }))
    );

    // SMA overlays
    const addLine = (points: { time: string; value: number | null }[], color: string, title: string) => {
      const series = chart.addSeries(LineSeries, {
        color,
        lineWidth: 1,
        title,
        priceLineVisible: false,
      });
      series.setData(
        points
          .filter((p) => p.value !== null)
          .map((p) => ({ time: parseTime(p.time), value: p.value! }))
      );
    };

    if (data.sma20.length) addLine(data.sma20, '#f59e0b', 'SMA 20');
    if (data.sma50.length) addLine(data.sma50, '#3b82f6', 'SMA 50');
    if (data.sma200.length) addLine(data.sma200, '#a855f7', 'SMA 200');

    // Bollinger Bands
    if (data.bb_upper.length) addLine(data.bb_upper, '#6b728033', 'BB Upper');
    if (data.bb_lower.length) addLine(data.bb_lower, '#6b728033', 'BB Lower');

    chart.timeScale().fitContent();
  }, [data]);

  const tf = data.timeframe === 'daily' ? t('chart.daily') : t('chart.hourly');
  return <ChartContainer title={`${data.ticker} ${t('chart.price')} (${tf})`} height={400}>{setupChart}</ChartContainer>;
}
