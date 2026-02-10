import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query';
import { apiFetch, apiPost } from './client';
import type {
  HealthResponse,
  HeatScoreResponse,
  IndicatorsResponse,
  RegimeResponse,
  ActionPlanResponse,
  ReportResponse,
  TickersResponse,
} from './types';

export function useTickers() {
  return useQuery<TickersResponse>({
    queryKey: ['tickers'],
    queryFn: () => apiFetch<TickersResponse>('/tickers'),
    staleTime: Infinity,
  });
}

export function useRefresh(ticker?: string) {
  const queryClient = useQueryClient();
  const param = ticker ? `?ticker=${encodeURIComponent(ticker)}` : '';
  return useMutation({
    mutationFn: () => apiPost<HealthResponse>(`/refresh${param}`),
    onSuccess: () => {
      queryClient.invalidateQueries();
    },
  });
}

export function useHealth(ticker?: string) {
  const param = ticker ? `?ticker=${encodeURIComponent(ticker)}` : '';
  return useQuery<HealthResponse>({
    queryKey: ['health', ticker],
    queryFn: () => apiFetch<HealthResponse>(`/health${param}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useHeatScore(ticker?: string) {
  const param = ticker ? `?ticker=${encodeURIComponent(ticker)}` : '';
  return useQuery<HeatScoreResponse>({
    queryKey: ['heat-score', ticker],
    queryFn: () => apiFetch<HeatScoreResponse>(`/heat-score${param}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useIndicators(timeframe: 'daily' | 'hourly' = 'daily', ticker?: string) {
  const tickerParam = ticker ? `&ticker=${encodeURIComponent(ticker)}` : '';
  return useQuery<IndicatorsResponse>({
    queryKey: ['indicators', timeframe, ticker],
    queryFn: () => apiFetch<IndicatorsResponse>(`/indicators?timeframe=${timeframe}${tickerParam}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useRegime(ticker?: string) {
  const param = ticker ? `?ticker=${encodeURIComponent(ticker)}` : '';
  return useQuery<RegimeResponse>({
    queryKey: ['regime', ticker],
    queryFn: () => apiFetch<RegimeResponse>(`/regime${param}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useActionPlan(ticker?: string) {
  const param = ticker ? `?ticker=${encodeURIComponent(ticker)}` : '';
  return useQuery<ActionPlanResponse>({
    queryKey: ['action-plan', ticker],
    queryFn: () => apiFetch<ActionPlanResponse>(`/action-plan${param}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useReport(ticker?: string) {
  const param = ticker ? `?ticker=${encodeURIComponent(ticker)}` : '';
  return useQuery<ReportResponse>({
    queryKey: ['report', ticker],
    queryFn: () => apiFetch<ReportResponse>(`/report${param}`),
    refetchInterval: 5 * 60 * 1000,
  });
}
