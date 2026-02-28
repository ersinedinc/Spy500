import { useTranslation } from '../../i18n';
import type { ActionPlanResponse } from '../../api/types';

interface ActionPanelProps {
  data: ActionPlanResponse;
}

function actionColor(action: string): string {
  if (action.includes('Aggressive') || action.includes('Agresif'))
    return 'text-green-400 border-green-700 bg-green-900/30';
  if (action.includes('Moderate') || action.includes('Ilimli'))
    return 'text-emerald-400 border-emerald-700 bg-emerald-900/30';
  if (action.includes('Normal'))
    return 'text-blue-400 border-blue-700 bg-blue-900/30';
  if (action.includes('Reduce') || action.includes('Azalt'))
    return 'text-orange-400 border-orange-700 bg-orange-900/30';
  return 'text-red-400 border-red-700 bg-red-900/30';
}

export default function ActionPanel({ data }: ActionPanelProps) {
  const { t } = useTranslation();

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-4">
      <div className="text-sm font-medium text-gray-300 mb-3">{t('action.title')}</div>

      <div className={`rounded-md border p-3 mb-3 ${actionColor(data.action)}`}>
        <div className="text-lg font-bold">{data.action}</div>
        <div className="text-2xl font-bold mt-1">
          {data.currency} {data.suggested_amount.toFixed(2)}
        </div>
        <div className="text-xs mt-1 opacity-75">
          {data.multiplier}x of {data.currency} {data.base_amount.toFixed(2)} {t('action.base')}
        </div>
      </div>

      <div className="space-y-1">
        {data.reasoning.map((r, i) => (
          <div key={i} className="text-xs text-gray-400 flex items-start gap-1.5">
            <span className="text-gray-600 mt-0.5">•</span>
            <span>{r}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
