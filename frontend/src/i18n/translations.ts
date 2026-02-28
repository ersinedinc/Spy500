export type Lang = 'en' | 'tr';

export interface TranslationDict {
  [key: string]: string;
}

const en: TranslationDict = {
  // Header
  'header.dashboard': 'Dashboard',
  'header.subtitle': 'Decision Support for Long-Term DCA',
  'header.refresh': 'Refresh',
  'header.refreshing': 'Refreshing...',

  // Status
  'status.loading': 'Loading...',
  'status.disconnected': 'Disconnected',
  'status.live': 'Live',
  'status.loadingData': 'Loading',
  'status.fallback': '(fallback)',
  'status.rows': 'rows',
  'status.updated': 'Updated:',
  'status.never': 'never',

  // Dashboard
  'dashboard.loading': 'Loading dashboard data...',
  'dashboard.error': 'Failed to load data. Is the backend running on port 8000?',

  // Heat Score
  'heat.title': 'Market Heat Score',
  'heat.fear': 'Fear',
  'heat.hot': 'Hot',
  'heat.scale': '0 = Opportunity / 100 = Risk',

  // Score Breakdown
  'breakdown.title': 'Score Breakdown',
  'breakdown.total': 'Total Score',

  // Regime
  'regime.title': 'Market Regime',
  'regime.confidence': 'Confidence',
  'regime.riskFlags': 'Risk Flags',

  // Action Plan
  'action.title': 'DCA Action Plan',
  'action.base': 'base',

  // Report
  'report.title': 'Full Report',
  'report.copy': 'Copy',
  'report.copied': 'Copied!',

  // History Table
  'history.title': 'Recent Data',
  'history.date': 'Date',
  'history.close': 'Close',

  // Charts
  'chart.price': 'Price',
  'chart.rsi': 'RSI (14)',
  'chart.drawdown': 'Drawdown (%)',
  'chart.volatility': 'Annualized Volatility (%)',
  'chart.daily': 'daily',
  'chart.hourly': 'hourly',
};

const tr: TranslationDict = {
  // Header
  'header.dashboard': 'Kontrol Paneli',
  'header.subtitle': 'Uzun Vadeli DCA icin Karar Destegi',
  'header.refresh': 'Yenile',
  'header.refreshing': 'Yenileniyor...',

  // Status
  'status.loading': 'Yukleniyor...',
  'status.disconnected': 'Baglanti Kesildi',
  'status.live': 'Canli',
  'status.loadingData': 'Yukleniyor',
  'status.fallback': '(yedek)',
  'status.rows': 'satir',
  'status.updated': 'Guncelleme:',
  'status.never': 'hic',

  // Dashboard
  'dashboard.loading': 'Panel verileri yukleniyor...',
  'dashboard.error': 'Veri yuklenemedi. Backend 8000 portunda calisiyor mu?',

  // Heat Score
  'heat.title': 'Piyasa Isi Skoru',
  'heat.fear': 'Korku',
  'heat.hot': 'Sicak',
  'heat.scale': '0 = Firsat / 100 = Risk',

  // Score Breakdown
  'breakdown.title': 'Skor Dagilimi',
  'breakdown.total': 'Toplam Skor',

  // Regime
  'regime.title': 'Piyasa Rejimi',
  'regime.confidence': 'Guven',
  'regime.riskFlags': 'Risk Bayraklari',

  // Action Plan
  'action.title': 'DCA Eylem Plani',
  'action.base': 'taban',

  // Report
  'report.title': 'Tam Rapor',
  'report.copy': 'Kopyala',
  'report.copied': 'Kopyalandi!',

  // History Table
  'history.title': 'Son Veriler',
  'history.date': 'Tarih',
  'history.close': 'Kapanis',

  // Charts
  'chart.price': 'Fiyat',
  'chart.rsi': 'RSI (14)',
  'chart.drawdown': 'Dusus (%)',
  'chart.volatility': 'Yillik Volatilite (%)',
  'chart.daily': 'gunluk',
  'chart.hourly': 'saatlik',
};

export const translations: Record<Lang, TranslationDict> = { en, tr };
