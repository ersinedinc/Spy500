import { useTranslation } from '../../i18n';
import type { IndicatorsResponse } from '../../api/types';

interface HistoryTableProps {
  data: IndicatorsResponse;
  rows?: number;
}

export default function HistoryTable({ data, rows = 10 }: HistoryTableProps) {
  const { t } = useTranslation();
  const ohlcv = data.ohlcv.slice(-rows).reverse();

  // Build lookup maps for indicators
  const getLatest = (points: { time: string; value: number | null }[]) => {
    const map = new Map<string, number | null>();
    for (const p of points) {
      const day = p.time.split('T')[0];
      map.set(day, p.value);
    }
    return map;
  };

  const rsiMap = getLatest(data.rsi);
  const sma50Map = getLatest(data.sma50);
  const volMap = getLatest(data.volatility);
  const ddMap = getLatest(data.drawdown);

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-4 overflow-x-auto">
      <div className="text-sm font-medium text-gray-300 mb-3">{t('history.title')}</div>
      <table className="w-full text-xs">
        <thead>
          <tr className="text-gray-500 border-b border-gray-800">
            <th className="text-left py-1.5 pr-3">{t('history.date')}</th>
            <th className="text-right py-1.5 px-2">{t('history.close')}</th>
            <th className="text-right py-1.5 px-2">RSI</th>
            <th className="text-right py-1.5 px-2">SMA50</th>
            <th className="text-right py-1.5 px-2">Vol%</th>
            <th className="text-right py-1.5 pl-2">DD%</th>
          </tr>
        </thead>
        <tbody>
          {ohlcv.map((row) => {
            const day = row.time.split('T')[0];
            const rsi = rsiMap.get(day);
            const sma50 = sma50Map.get(day);
            const vol = volMap.get(day);
            const dd = ddMap.get(day);

            return (
              <tr key={day} className="border-b border-gray-800/50 text-gray-400">
                <td className="py-1.5 pr-3">{day}</td>
                <td className="text-right py-1.5 px-2 text-gray-200">{row.close.toFixed(2)}</td>
                <td className="text-right py-1.5 px-2">{rsi != null ? rsi.toFixed(1) : '—'}</td>
                <td className="text-right py-1.5 px-2">{sma50 != null ? sma50.toFixed(2) : '—'}</td>
                <td className="text-right py-1.5 px-2">{vol != null ? (vol * 100).toFixed(1) : '—'}</td>
                <td className="text-right py-1.5 pl-2">{dd != null ? (dd * 100).toFixed(1) : '—'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
