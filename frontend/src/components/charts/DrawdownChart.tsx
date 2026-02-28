import { useCallback } from 'react';
import { AreaSeries, type IChartApi } from 'lightweight-charts';
import ChartContainer from './ChartContainer';
import { useTranslation } from '../../i18n';
import type { IndicatorPoint } from '../../api/types';

interface DrawdownChartProps {
  data: IndicatorPoint[];
}

function parseTime(iso: string): string {
  return iso.split('T')[0];
}

export default function DrawdownChart({ data }: DrawdownChartProps) {
  const { t } = useTranslation();

  const setupChart = useCallback((chart: IChartApi) => {
    const series = chart.addSeries(AreaSeries, {
      lineColor: '#ef4444',
      topColor: '#ef444440',
      bottomColor: '#ef444408',
      lineWidth: 2,
      title: 'Drawdown',
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

    chart.timeScale().fitContent();
  }, [data]);

  return (
    <ChartContainer
      title={t('chart.drawdown')}
      height={200}
    >
      {setupChart}
    </ChartContainer>
  );
}
