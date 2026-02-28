import { useCallback } from 'react';
import { LineSeries, type IChartApi } from 'lightweight-charts';
import ChartContainer from './ChartContainer';
import { useTranslation } from '../../i18n';
import type { IndicatorPoint } from '../../api/types';

interface RSIChartProps {
  data: IndicatorPoint[];
}

function parseTime(iso: string): string {
  return iso.split('T')[0];
}

export default function RSIChart({ data }: RSIChartProps) {
  const { t } = useTranslation();

  const setupChart = useCallback((chart: IChartApi) => {
    const series = chart.addSeries(LineSeries, {
      color: '#f59e0b',
      lineWidth: 2,
      title: 'RSI(14)',
      priceLineVisible: false,
    });

    series.setData(
      data
        .filter((p) => p.value !== null)
        .map((p) => ({ time: parseTime(p.time), value: p.value! }))
    );

    // Overbought line
    const overbought = chart.addSeries(LineSeries, {
      color: '#ef444480',
      lineWidth: 1,
      lineStyle: 2,
      title: '70',
      priceLineVisible: false,
    });
    const oversold = chart.addSeries(LineSeries, {
      color: '#22c55e80',
      lineWidth: 1,
      lineStyle: 2,
      title: '30',
      priceLineVisible: false,
    });

    const timeRange = data
      .filter((p) => p.value !== null)
      .map((p) => parseTime(p.time));

    if (timeRange.length > 0) {
      overbought.setData(timeRange.map((t) => ({ time: t, value: 70 })));
      oversold.setData(timeRange.map((t) => ({ time: t, value: 30 })));
    }

    chart.timeScale().fitContent();
  }, [data]);

  return (
    <ChartContainer
      title={t('chart.rsi')}
      height={200}
      options={{ rightPriceScale: { scaleMargins: { top: 0.1, bottom: 0.1 } } }}
    >
      {setupChart}
    </ChartContainer>
  );
}
