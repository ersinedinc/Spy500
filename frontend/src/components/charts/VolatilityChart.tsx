import { useCallback } from 'react';
import { LineSeries, type IChartApi } from 'lightweight-charts';
import ChartContainer from './ChartContainer';
import { useTranslation } from '../../i18n';
import type { IndicatorPoint } from '../../api/types';

interface VolatilityChartProps {
  data: IndicatorPoint[];
}

function parseTime(iso: string): string {
  return iso.split('T')[0];
}

export default function VolatilityChart({ data }: VolatilityChartProps) {
  const { t } = useTranslation();

  const setupChart = useCallback((chart: IChartApi) => {
    const series = chart.addSeries(LineSeries, {
      color: '#8b5cf6',
      lineWidth: 2,
      title: 'Volatility',
      priceLineVisible: false,
    });

    series.setData(
      data
        .filter((p) => p.value !== null)
        .map((p) => ({
          time: parseTime(p.time),
          value: Math.round(p.value! * 10000) / 100,
        }))
    );

    // Threshold at 30%
    const timeRange = data
      .filter((p) => p.value !== null)
      .map((p) => parseTime(p.time));

    if (timeRange.length > 0) {
      const threshold = chart.addSeries(LineSeries, {
        color: '#ef444480',
        lineWidth: 1,
        lineStyle: 2,
        title: '30%',
        priceLineVisible: false,
      });
      threshold.setData(timeRange.map((t) => ({ time: t, value: 30 })));
    }

    chart.timeScale().fitContent();
  }, [data]);

  return (
    <ChartContainer
      title={t('chart.volatility')}
      height={200}
    >
      {setupChart}
    </ChartContainer>
  );
}
