import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query';
import { apiFetch, apiPost } from './client';
import { useTranslation } from '../i18n';
import type {
  HealthResponse,
  HeatScoreResponse,
  IndicatorsResponse,
  RegimeResponse,
  ActionPlanResponse,
  ReportResponse,
  TickersResponse,
} from './types';

function buildParams(params: Record<string, string | undefined>): string {
  const entries = Object.entries(params).filter(
    (e): e is [string, string] => e[1] !== undefined && e[1] !== '',
  );
  if (entries.length === 0) return '';
  return '?' + entries.map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&');
}

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
  const { lang } = useTranslation();
  const params = buildParams({ ticker, lang });
  return useQuery<HeatScoreResponse>({
    queryKey: ['heat-score', ticker, lang],
    queryFn: () => apiFetch<HeatScoreResponse>(`/heat-score${params}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useIndicators(timeframe: 'daily' | 'hourly' = 'daily', ticker?: string) {
  const params = buildParams({ timeframe, ticker });
  return useQuery<IndicatorsResponse>({
    queryKey: ['indicators', timeframe, ticker],
    queryFn: () => apiFetch<IndicatorsResponse>(`/indicators${params}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useRegime(ticker?: string) {
  const { lang } = useTranslation();
  const params = buildParams({ ticker, lang });
  return useQuery<RegimeResponse>({
    queryKey: ['regime', ticker, lang],
    queryFn: () => apiFetch<RegimeResponse>(`/regime${params}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useActionPlan(ticker?: string) {
  const { lang } = useTranslation();
  const params = buildParams({ ticker, lang });
  return useQuery<ActionPlanResponse>({
    queryKey: ['action-plan', ticker, lang],
    queryFn: () => apiFetch<ActionPlanResponse>(`/action-plan${params}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useReport(ticker?: string) {
  const { lang } = useTranslation();
  const params = buildParams({ ticker, lang });
  return useQuery<ReportResponse>({
    queryKey: ['report', ticker, lang],
    queryFn: () => apiFetch<ReportResponse>(`/report${params}`),
    refetchInterval: 5 * 60 * 1000,
  });
}
