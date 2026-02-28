"""Internationalisation helpers — English / Turkish translations.

Translations happen at the router/response layer so the core pipeline
stays English internally.
"""

from __future__ import annotations

from typing import Any

_TRANSLATIONS: dict[str, dict[str, str]] = {
    # ── Heat-score labels ──────────────────────────────────────
    "Fear":     {"tr": "Korku"},
    "Cooling":  {"tr": "Soguyor"},
    "Neutral":  {"tr": "Notr"},
    "Hot":      {"tr": "Sicak"},

    # ── Heat-score component names ─────────────────────────────
    "RSI":              {"tr": "RSI - Goreceli Guc Endeksi"},
    "MACD Histogram":   {"tr": "MACD Histogrami"},
    "BB Position":      {"tr": "Bollinger Bandi Pozisyonu"},
    "MA Trend":         {"tr": "HO Trendi (Hareketli Ortalama)"},
    "Drawdown":         {"tr": "Dusus (Zirveden Geri Cekilme)"},
    "Volatility":       {"tr": "Volatilite (Dalgalanma)"},
    "5-Day Momentum":   {"tr": "5 Gunluk Momentum"},
    "Distance to MA200": {"tr": "MA200'e Uzaklik"},

    # ── Market regime ──────────────────────────────────────────
    "Trend Up":   {"tr": "Yukselis Trendi"},
    "Trend Down": {"tr": "Dusus Trendi"},
    "Range":      {"tr": "Yatay Seyir"},

    # ── Risk flags ─────────────────────────────────────────────
    "Overbought":       {"tr": "Asiri Alim"},
    "Oversold":         {"tr": "Asiri Satim"},
    "High Volatility":  {"tr": "Yuksek Volatilite"},
    "Extreme Drawdown": {"tr": "Asiri Dusus"},
    "Death Cross":      {"tr": "Olum Caprazlamasi"},
    "Golden Cross":     {"tr": "Altin Caprazlama"},

    # ── DCA action labels ─────────────────────────────────────
    "Aggressive Buy": {"tr": "Agresif Alis"},
    "Moderate Buy":   {"tr": "Ilimli Alis"},
    "Normal DCA":     {"tr": "Normal DCA"},
    "Reduce":         {"tr": "Azalt"},
    "Minimal":        {"tr": "Minimum"},

    # ── Regime detail keys ─────────────────────────────────────
    "SMA50 vs SMA200":  {"tr": "HO50 - HO200 Karsilastirmasi"},
    "Price vs SMA50":   {"tr": "Fiyat - HO50 Karsilastirmasi"},
    "RSI zone":         {"tr": "RSI Bolgesi"},
    "Volatility level": {"tr": "Volatilite Seviyesi"},
    "Drawdown level":   {"tr": "Dusus Seviyesi"},

    # ── Regime detail values ───────────────────────────────────
    "bullish (SMA50 > SMA200)":    {"tr": "yukselis (HO50 > HO200)"},
    "bearish (SMA50 < SMA200)":    {"tr": "dusus (HO50 < HO200)"},
    "above SMA50":                 {"tr": "HO50 ustunde"},
    "below SMA50":                 {"tr": "HO50 altinda"},
    "overbought":                  {"tr": "asiri alim"},
    "oversold":                    {"tr": "asiri satim"},
    "normal":                      {"tr": "normal"},
    "high":                        {"tr": "yuksek"},
    "moderate":                    {"tr": "orta"},
    "low":                         {"tr": "dusuk"},
    "extreme":                     {"tr": "asiri"},
    "minimal":                     {"tr": "minimum"},
    "none":                        {"tr": "yok"},
}


def t(key: str, lang: str = "en") -> str:
    """Translate *key* into *lang*. Falls back to the key itself."""
    if lang == "en":
        return key
    entry = _TRANSLATIONS.get(key)
    if entry and lang in entry:
        return entry[lang]
    return key


def translate_items(items: list[str], lang: str) -> list[str]:
    """Translate a list of strings."""
    return [t(item, lang) for item in items]


def translate_dict(d: dict[str, Any], lang: str) -> dict[str, Any]:
    """Translate both keys and string values of a dict."""
    return {t(k, lang): t(v, lang) if isinstance(v, str) else v for k, v in d.items()}


# ── DCA reasoning templates (Turkish) ─────────────────────────

_REASONING_PATTERNS_TR: list[tuple[str, str]] = [
    ("Heat Score is",          "Isi Skoru"),
    ("Market regime:",         "Piyasa rejimi:"),
    ("Score falls in bracket", "Skor araliği"),
    ("Base monthly contribution:", "Aylik temel katki:"),
    ("Suggested contribution:", "Onerilen katki:"),
    ("Market conditions suggest opportunity — consider increasing allocation",
     "Piyasa kosullari firsat isaret ediyor — tahsisati artirmayi dusunun"),
    ("Market conditions suggest caution — consider reducing allocation",
     "Piyasa kosullari temkinli olmayi isaret ediyor — tahsisati azaltmayi dusunun"),
    ("Market conditions are neutral — maintain regular DCA schedule",
     "Piyasa kosullari notr — duzenli DCA takvimini surdurun"),
]


def translate_reasoning(reasoning: list[str], lang: str) -> list[str]:
    """Translate DCA reasoning strings."""
    if lang == "en":
        return reasoning
    result = []
    for line in reasoning:
        translated = line
        for en_pat, tr_pat in _REASONING_PATTERNS_TR:
            if en_pat in translated:
                translated = translated.replace(en_pat, tr_pat)
        # Translate known inline terms
        for en_term in ("Trend Up", "Trend Down", "Range",
                        "Aggressive Buy", "Moderate Buy", "Normal DCA",
                        "Reduce", "Minimal",
                        "Fear", "Cooling", "Neutral", "Hot"):
            if en_term in translated:
                translated = translated.replace(en_term, t(en_term, lang))
        result.append(translated)
    return result


def translate_description(desc: str, lang: str) -> str:
    """Translate a heat-score component description."""
    if lang == "en":
        return desc
    return (
        desc
        .replace("5-day price change", "5 gunluk fiyat degisimi")
        .replace("Distance to SMA200", "SMA200'e uzaklik")
    )


# ── Report translation ────────────────────────────────────────

def translate_report(
    report_md: str,
    lang: str,
) -> str:
    """Translate the full markdown report.  For 'en' returns as-is."""
    if lang == "en":
        return report_md

    replacements = [
        ("# S&P 500 Market Analysis Report", "# S&P 500 Piyasa Analiz Raporu"),
        ("**Generated:**", "**Olusturulma:**"),
        ("## Data Source", "## Veri Kaynagi"),
        ("**Active Ticker:**", "**Aktif Hisse:**"),
        ("**Fallback Used:** Yes", "**Yedek Kullanildi:** Evet"),
        ("**Fallback Used:** No (primary ticker active)",
         "**Yedek Kullanildi:** Hayir (birincil hisse aktif)"),
        ("**Reason:**", "**Sebep:**"),
        ("**Latest Close:**", "**Son Kapanis:**"),
        ("## Heat Score", "## Isi Skoru"),
        ("| Component | Raw Value | Normalized | Weight | Contribution |",
         "| Bilesen | Ham Deger | Normalize | Agirlik | Katki |"),
        ("|-----------|-----------|------------|--------|--------------|",
         "|---------|-----------|-----------|--------|------|"),
        ("| **Total**", "| **Toplam**"),
        ("## Market Regime", "## Piyasa Rejimi"),
        ("**Regime:**", "**Rejim:**"),
        ("**Confidence:**", "**Guven:**"),
        ("**Risk Flags:**", "**Risk Bayraklari:**"),
        ("None", "Yok"),
        ("## DCA Recommendation", "## DCA Onerisi"),
        ("**Action:**", "**Eylem:**"),
        ("**Multiplier:**", "**Carpan:**"),
        ("**Base Amount:**", "**Temel Tutar:**"),
        ("**Suggested Amount:**", "**Onerilen Tutar:**"),
        ("**Reasoning:**", "**Gerekce:**"),
        ("## Key Levels", "## Onemli Seviyeler"),
        ("**SMA 50:**", "**HO 50:**"),
        ("**SMA 200:**", "**HO 200:**"),
        ("**Bollinger Lower:**", "**Bollinger Alt:**"),
        ("**Bollinger Upper:**", "**Bollinger Ust:**"),
        ("## Disclaimer", "## Yasal Uyari"),
        ("> This report is generated automatically for informational and educational "
         "purposes only. It is **not financial advice**. The Heat Score and DCA "
         "recommendations are based on technical indicators with hardcoded normalization "
         "ranges that may not be appropriate in all market conditions. Past performance "
         "does not guarantee future results. Always consult a qualified financial "
         "advisor before making investment decisions.",
         "> Bu rapor yalnizca bilgilendirme ve egitim amaciyla otomatik olarak "
         "olusturulmustur. **Yatirim tavsiyesi degildir**. Isi Skoru ve DCA onerileri, "
         "tum piyasa kosullarinda uygun olmayabilecek sabit normalizasyon araliklarina "
         "sahip teknik gostergelere dayanmaktadir. Gecmis performans gelecekteki "
         "sonuclari garanti etmez. Yatirim kararlari vermeden once her zaman yetkili "
         "bir mali danismana danisin."),
    ]

    translated = report_md
    for en, tr in replacements:
        translated = translated.replace(en, tr)

    # Translate regime/flag/action terms that appear inline
    for en_term in ("Trend Up", "Trend Down", "Range",
                    "Overbought", "Oversold", "High Volatility",
                    "Extreme Drawdown", "Death Cross", "Golden Cross",
                    "Aggressive Buy", "Moderate Buy", "Normal DCA",
                    "Reduce", "Minimal", "Fear", "Cooling", "Hot"):
        tr_term = t(en_term, "tr")
        if en_term != tr_term:
            translated = translated.replace(en_term, tr_term)

    # Translate component names in the table rows
    for en_name in ("RSI", "MACD Histogram", "BB Position", "MA Trend",
                    "Drawdown", "Volatility", "5-Day Momentum", "Distance to MA200"):
        tr_name = t(en_name, "tr")
        if en_name != tr_name:
            translated = translated.replace(f"| {en_name} |", f"| {tr_name} |")

    # Translate detail keys
    for en_key in ("SMA50 vs SMA200", "Price vs SMA50", "RSI zone",
                   "Volatility level", "Drawdown level"):
        tr_key = t(en_key, "tr")
        translated = translated.replace(f"*{en_key}:*", f"*{tr_key}:*")

    return translated
