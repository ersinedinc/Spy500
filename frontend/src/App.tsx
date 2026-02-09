import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Header from './components/layout/Header';
import Dashboard from './pages/Dashboard';
import { useHealth } from './api/hooks';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
      retry: 2,
    },
  },
});

function AppContent() {
  const health = useHealth();

  return (
    <div className="min-h-screen bg-gray-950">
      <Header health={health.data} isLoading={health.isLoading} />
      <Dashboard />
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}
