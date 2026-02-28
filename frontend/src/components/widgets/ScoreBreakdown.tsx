import { useTranslation } from '../../i18n';
import type { ScoreComponent } from '../../api/types';

interface ScoreBreakdownProps {
  components: ScoreComponent[];
  totalScore: number;
}

function barColor(normalized: number): string {
  if (normalized < 30) return 'bg-green-500';
  if (normalized < 45) return 'bg-lime-500';
  if (normalized < 65) return 'bg-yellow-500';
  if (normalized < 80) return 'bg-orange-500';
  return 'bg-red-500';
}

export default function ScoreBreakdown({ components, totalScore }: ScoreBreakdownProps) {
  const { t } = useTranslation();

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-4">
      <div className="text-sm font-medium text-gray-300 mb-3">{t('breakdown.title')}</div>

      <div className="space-y-2">
        {components.map((c) => (
          <div key={c.name}>
            <div className="flex justify-between text-xs mb-0.5">
              <span className="text-gray-400">{c.name}</span>
              <span className="text-gray-500">
                {c.normalized.toFixed(0)} x {(c.weight * 100).toFixed(0)}% = {c.contribution.toFixed(1)}
              </span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${barColor(c.normalized)}`}
                style={{ width: `${Math.min(c.normalized, 100)}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-3 pt-2 border-t border-gray-800 flex justify-between text-sm font-semibold">
        <span className="text-gray-300">{t('breakdown.total')}</span>
        <span className="text-gray-200">{totalScore.toFixed(1)}</span>
      </div>
    </div>
  );
}
