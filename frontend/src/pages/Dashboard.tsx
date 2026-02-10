import { useHeatScore, useIndicators, useRegime, useActionPlan, useReport } from '../api/hooks';
import DashboardGrid from '../components/layout/DashboardGrid';
import PriceChart from '../components/charts/PriceChart';
import RSIChart from '../components/charts/RSIChart';
import DrawdownChart from '../components/charts/DrawdownChart';
import VolatilityChart from '../components/charts/VolatilityChart';
import HeatScoreGauge from '../components/widgets/HeatScoreGauge';
import RegimeDisplay from '../components/widgets/RegimeDisplay';
import ActionPanel from '../components/widgets/ActionPanel';
import ScoreBreakdown from '../components/widgets/ScoreBreakdown';
import HistoryTable from '../components/widgets/HistoryTable';
import ReportViewer from '../components/widgets/ReportViewer';

interface DashboardProps {
  ticker: string;
}

export default function Dashboard({ ticker }: DashboardProps) {
  const heatScore = useHeatScore(ticker);
  const indicators = useIndicators('daily', ticker);
  const regime = useRegime(ticker);
  const actionPlan = useActionPlan(ticker);
  const report = useReport(ticker);

  const isLoading = heatScore.isLoading || indicators.isLoading;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500 text-sm">Loading dashboard data...</div>
      </div>
    );
  }

  const hasError = heatScore.isError || indicators.isError;
  if (hasError) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-400 text-sm">
          Failed to load data. Is the backend running on port 8000?
        </div>
      </div>
    );
  }

  return (
    <DashboardGrid>
      {/* Row 1: Score Gauge + Regime + Action Plan */}
      {heatScore.data && (
        <HeatScoreGauge data={heatScore.data} />
      )}
      {regime.data && (
        <RegimeDisplay data={regime.data} />
      )}
      {actionPlan.data && (
        <ActionPanel data={actionPlan.data} />
      )}

      {/* Row 2: Price Chart (spans 2 cols on md+) */}
      {indicators.data && (
        <div className="md:col-span-2 xl:col-span-2">
          <PriceChart data={indicators.data} />
        </div>
      )}

      {/* Score Breakdown */}
      {heatScore.data && (
        <ScoreBreakdown
          components={heatScore.data.components}
          totalScore={heatScore.data.score}
        />
      )}

      {/* Row 3: RSI + Drawdown + Volatility */}
      {indicators.data && (
        <>
          <RSIChart data={indicators.data.rsi} />
          <DrawdownChart data={indicators.data.drawdown} />
          <VolatilityChart data={indicators.data.volatility} />
        </>
      )}

      {/* Row 4: History Table (spans 2 cols) */}
      {indicators.data && (
        <div className="md:col-span-2">
          <HistoryTable data={indicators.data} />
        </div>
      )}

      {/* Report (spans full width) */}
      {report.data && (
        <div className="md:col-span-2 xl:col-span-3">
          <ReportViewer markdown={report.data.markdown} />
        </div>
      )}
    </DashboardGrid>
  );
}
