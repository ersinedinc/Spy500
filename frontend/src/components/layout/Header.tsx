import StatusIndicator from '../widgets/StatusIndicator';
import { useRefresh } from '../../api/hooks';
import type { HealthResponse } from '../../api/types';

interface HeaderProps {
  health: HealthResponse | undefined;
  isLoading: boolean;
}

export default function Header({ health, isLoading }: HeaderProps) {
  const refresh = useRefresh();

  return (
    <header className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-10">
      <div className="max-w-screen-2xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-bold text-gray-100">S&P 500 Dashboard</h1>
          <span className="text-xs text-gray-600 hidden sm:inline">Decision Support for Long-Term DCA</span>
        </div>
        <div className="flex items-center gap-3">
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
