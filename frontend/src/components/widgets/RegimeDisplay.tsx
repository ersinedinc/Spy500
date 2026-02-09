import type { RegimeResponse } from '../../api/types';

interface RegimeDisplayProps {
  data: RegimeResponse;
}

function regimeColor(regime: string): string {
  switch (regime) {
    case 'Trend Up': return 'bg-green-900/50 text-green-400 border-green-700';
    case 'Trend Down': return 'bg-red-900/50 text-red-400 border-red-700';
    default: return 'bg-yellow-900/50 text-yellow-400 border-yellow-700';
  }
}

function flagColor(flag: string): string {
  if (flag.includes('Overbought') || flag.includes('Death')) return 'bg-red-900/50 text-red-300';
  if (flag.includes('Oversold') || flag.includes('Golden')) return 'bg-green-900/50 text-green-300';
  return 'bg-orange-900/50 text-orange-300';
}

export default function RegimeDisplay({ data }: RegimeDisplayProps) {
  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-4">
      <div className="text-sm font-medium text-gray-300 mb-3">Market Regime</div>

      <div className={`inline-block px-3 py-1.5 rounded-md border text-sm font-semibold ${regimeColor(data.regime)}`}>
        {data.regime}
      </div>

      <div className="mt-2 text-xs text-gray-400">
        Confidence: {Math.round(data.confidence * 100)}%
      </div>

      {data.risk_flags.length > 0 && (
        <div className="mt-3">
          <div className="text-xs text-gray-500 mb-1">Risk Flags</div>
          <div className="flex flex-wrap gap-1.5">
            {data.risk_flags.map((flag) => (
              <span key={flag} className={`px-2 py-0.5 rounded text-xs ${flagColor(flag)}`}>
                {flag}
              </span>
            ))}
          </div>
        </div>
      )}

      {Object.entries(data.details).length > 0 && (
        <div className="mt-3 space-y-1">
          {Object.entries(data.details).map(([key, val]) => (
            <div key={key} className="text-xs text-gray-400">
              <span className="text-gray-500">{key}:</span> {val}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
