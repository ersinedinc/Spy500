import type { HeatScoreResponse } from '../../api/types';

interface HeatScoreGaugeProps {
  data: HeatScoreResponse;
}

function scoreToColor(score: number): string {
  if (score < 30) return '#22c55e';
  if (score < 45) return '#84cc16';
  if (score < 65) return '#f59e0b';
  if (score < 80) return '#f97316';
  return '#ef4444';
}

export default function HeatScoreGauge({ data }: HeatScoreGaugeProps) {
  const score = data.score;
  const color = scoreToColor(score);
  const angle = (score / 100) * 180;

  // SVG semicircular gauge
  const cx = 120;
  const cy = 110;
  const r = 90;
  const startAngle = Math.PI;
  const endAngle = Math.PI + (angle / 180) * Math.PI;

  const x1 = cx + r * Math.cos(startAngle);
  const y1 = cy + r * Math.sin(startAngle);
  const x2 = cx + r * Math.cos(endAngle);
  const y2 = cy + r * Math.sin(endAngle);

  const largeArc = angle > 180 ? 1 : 0;

  // Background arc
  const bgX2 = cx + r * Math.cos(0);
  const bgY2 = cy + r * Math.sin(0);

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-4">
      <div className="text-sm font-medium text-gray-300 mb-2">Market Heat Score</div>
      <div className="flex flex-col items-center">
        <svg width="240" height="140" viewBox="0 0 240 140">
          {/* Background arc */}
          <path
            d={`M ${x1} ${y1} A ${r} ${r} 0 1 1 ${bgX2} ${bgY2}`}
            fill="none"
            stroke="#1f2937"
            strokeWidth="16"
            strokeLinecap="round"
          />
          {/* Score arc */}
          {score > 0 && (
            <path
              d={`M ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2}`}
              fill="none"
              stroke={color}
              strokeWidth="16"
              strokeLinecap="round"
            />
          )}
          {/* Score text */}
          <text x={cx} y={cy - 10} textAnchor="middle" fill={color} fontSize="36" fontWeight="bold">
            {Math.round(score)}
          </text>
          <text x={cx} y={cy + 15} textAnchor="middle" fill="#9ca3af" fontSize="14">
            {data.label}
          </text>
          {/* Labels */}
          <text x="20" y="130" fill="#22c55e" fontSize="11">Fear</text>
          <text x="200" y="130" fill="#ef4444" fontSize="11">Hot</text>
        </svg>
      </div>
      <div className="text-center text-xs text-gray-500 mt-1">
        0 = Opportunity / 100 = Risk
      </div>
    </div>
  );
}
