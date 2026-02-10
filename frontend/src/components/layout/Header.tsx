import StatusIndicator from '../widgets/StatusIndicator';
import { useRefresh } from '../../api/hooks';
import type { HealthResponse, TickerInfo } from '../../api/types';

interface HeaderProps {
  health: HealthResponse | undefined;
  isLoading: boolean;
  tickers: TickerInfo[];
  selectedTicker: string;
  selectedName: string;
  onTickerChange: (ticker: string) => void;
}

export default function Header({ health, isLoading, tickers, selectedTicker, selectedName, onTickerChange }: HeaderProps) {
  const refresh = useRefresh(selectedTicker);

  return (
    <header className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-10">
      <div className="max-w-screen-2xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-bold text-gray-100">{selectedName} Dashboard</h1>
          <span className="text-xs text-gray-600 hidden sm:inline">Decision Support for Long-Term DCA</span>
        </div>
        <div className="flex items-center gap-3">
          {tickers.length > 0 && (
            <select
              value={selectedTicker}
              onChange={(e) => onTickerChange(e.target.value)}
              className="px-2 py-1.5 text-xs font-medium rounded border border-gray-700 bg-gray-800 text-gray-300 hover:bg-gray-700 transition-colors cursor-pointer focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              {tickers.map((t) => (
                <option key={t.symbol} value={t.symbol}>
                  {t.name}
                </option>
              ))}
            </select>
          )}
          <StatusIndicator data={health} isLoading={isLoading} />
          <button
            onClick={() => refresh.mutate()}
            disabled={refresh.isPending}
            className="px-3 py-1.5 text-xs font-medium rounded border border-gray-700 bg-gray-800 hover:bg-gray-700 text-gray-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {refresh.isPending ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
      </div>
    </header>
  );
}
