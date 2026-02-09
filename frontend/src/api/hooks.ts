import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query';
import { apiFetch, apiPost } from './client';
import type {
  HealthResponse,
  HeatScoreResponse,
  IndicatorsResponse,
  RegimeResponse,
  ActionPlanResponse,
  ReportResponse,
} from './types';

export function useRefresh() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => apiPost<HealthResponse>('/refresh'),
    onSuccess: () => {
      queryClient.invalidateQueries();
    },
  });
}

export function useHealth() {
  return useQuery<HealthResponse>({
    queryKey: ['health'],
    queryFn: () => apiFetch<HealthResponse>('/health'),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useHeatScore() {
  return useQuery<HeatScoreResponse>({
    queryKey: ['heat-score'],
    queryFn: () => apiFetch<HeatScoreResponse>('/heat-score'),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useIndicators(timeframe: 'daily' | 'hourly' = 'daily') {
  return useQuery<IndicatorsResponse>({
    queryKey: ['indicators', timeframe],
    queryFn: () => apiFetch<IndicatorsResponse>(`/indicators?timeframe=${timeframe}`),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useRegime() {
  return useQuery<RegimeResponse>({
    queryKey: ['regime'],
    queryFn: () => apiFetch<RegimeResponse>('/regime'),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useActionPlan() {
  return useQuery<ActionPlanResponse>({
    queryKey: ['action-plan'],
    queryFn: () => apiFetch<ActionPlanResponse>('/action-plan'),
    refetchInterval: 5 * 60 * 1000,
  });
}

export function useReport() {
  return useQuery<ReportResponse>({
    queryKey: ['report'],
    queryFn: () => apiFetch<ReportResponse>('/report'),
    refetchInterval: 5 * 60 * 1000,
  });
}
