import type { HealthResponse } from '../../api/types';

interface StatusIndicatorProps {
  data: HealthResponse | undefined;
  isLoading: boolean;
}

export default function StatusIndicator({ data, isLoading }: StatusIndicatorProps) {
  if (isLoading) {
    return (
      <div className="flex items-center gap-2 text-xs text-gray-500">
        <span className="w-2 h-2 rounded-full bg-yellow-500 animate-pulse" />
        Loading...
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center gap-2 text-xs text-gray-500">
        <span className="w-2 h-2 rounded-full bg-red-500" />
        Disconnected
      </div>
    );
  }

  const dotColor = data.ready ? 'bg-green-500' : 'bg-yellow-500';
  const refreshTime = data.last_refresh
    ? new Date(data.last_refresh).toLocaleTimeString()
    : 'never';

  return (
    <div className="flex items-center gap-3 text-xs text-gray-400">
      <div className="flex items-center gap-1.5">
        <span className={`w-2 h-2 rounded-full ${dotColor}`} />
        {data.ready ? 'Live' : 'Loading'}
      </div>
      <span>{data.active_ticker}</span>
      {data.used_fallback && (
        <span className="text-yellow-500">(fallback)</span>
      )}
      <span className="text-gray-600">|</span>
      <span>{data.daily_rows}d / {data.hourly_rows}h rows</span>
      <span className="text-gray-600">|</span>
      <span>Updated: {refreshTime}</span>
    </div>
  );
}
