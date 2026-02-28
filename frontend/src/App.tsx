import { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { LanguageProvider } from './i18n';
import Header from './components/layout/Header';
import Dashboard from './pages/Dashboard';
import { useHealth, useTickers } from './api/hooks';
import type { TickerInfo } from './api/types';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
      retry: 2,
    },
  },
});

function AppContent() {
  const { data: tickersData } = useTickers();
  const [selectedTicker, setSelectedTicker] = useState<string>('');

  useEffect(() => {
    if (tickersData && !selectedTicker) {
      setSelectedTicker(tickersData.default);
    }
  }, [tickersData, selectedTicker]);

  const ticker = selectedTicker || tickersData?.default || 'SPY';
  const tickers: TickerInfo[] = tickersData?.tickers ?? [];
  const selectedName = tickers.find(t => t.symbol === ticker)?.name ?? ticker;

  const health = useHealth(ticker);

  return (
    <div className="min-h-screen bg-gray-950">
      <Header
        health={health.data}
        isLoading={health.isLoading}
        tickers={tickers}
        selectedTicker={ticker}
        selectedName={selectedName}
        onTickerChange={setSelectedTicker}
      />
      <Dashboard ticker={ticker} />
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <LanguageProvider>
        <AppContent />
      </LanguageProvider>
    </QueryClientProvider>
  );
}
