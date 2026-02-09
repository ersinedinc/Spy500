import { useRef, useEffect, type ReactNode } from 'react';
import { createChart, type IChartApi, type DeepPartial, type ChartOptions } from 'lightweight-charts';

interface ChartContainerProps {
  children: (chart: IChartApi) => void;
  height?: number;
  options?: DeepPartial<ChartOptions>;
  title?: string;
}

export default function ChartContainer({ children, height = 300, options, title }: ChartContainerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      width: containerRef.current.clientWidth,
      height,
      layout: {
        background: { color: '#0a0a1a' },
        textColor: '#9ca3af',
      },
      grid: {
        vertLines: { color: '#1f2937' },
        horzLines: { color: '#1f2937' },
      },
      crosshair: {
        mode: 0,
      },
      timeScale: {
        borderColor: '#374151',
        timeVisible: true,
      },
      rightPriceScale: {
        borderColor: '#374151',
      },
      ...options,
    });

    chartRef.current = chart;
    children(chart);

    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        chart.applyOptions({ width: entry.contentRect.width });
      }
    });
    observer.observe(containerRef.current);

    return () => {
      observer.disconnect();
      chart.remove();
      chartRef.current = null;
    };
  }, [children, height, options]);

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
      {title && (
        <div className="px-4 py-2 border-b border-gray-800 text-sm font-medium text-gray-300">
          {title}
        </div>
      )}
      <div ref={containerRef} />
    </div>
  );
}
