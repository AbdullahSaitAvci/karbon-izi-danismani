# ============================================================
# constants.py — Proje genelinde kullanılan sabit değerler
# Tüm emisyon faktörleri, form seçenekleri ve limitler burada tanımlanır.
# Magic number kullanımını önlemek için her sabit buradan import edilir.
# ============================================================

# -----------------------------------------------
# EMİSYON FAKTÖRLERİ
# Kaynak: IPCC 2006 Kılavuzu, TEİAŞ yıllık raporları
# -----------------------------------------------

# Türkiye şebeke ortalaması (kg CO₂ / kWh)
ELEKTRIK_EMISYON_FAKTORU = 0.47

# Doğalgaz emisyon faktörü (kg CO₂ / m³)
DOGALGAZ_EMISYON_FAKTORU = 2.0

# Kömür emisyon faktörü (kg CO₂ / kg)
KOMUR_EMISYON_FAKTORU = 2.86

# Fuel-oil emisyon faktörü (kg CO₂ / litre)
FUELOIL_EMISYON_FAKTORU = 3.15

# Isı pompası — şebeke elektriğiyle çalıştığı için
# COP (performans katsayısı) ile düzeltilmiş faktör
ISI_POMPASI_COP = 3.5

# Isınma tipine göre aylık yakıt tüketimi tahmini (birim / kWh ısı)
# Bu çarpanlar, aylık elektrik tüketiminin %30'u kadar ısı ihtiyacı varsayar
ISINMA_ENERJI_ORANI = 0.30

# Isınma tipi -> (emisyon_faktoru, birim_adi) eşleştirmesi
ISINMA_EMISYON_HARITASI = {
    "Doğalgaz": (DOGALGAZ_EMISYON_FAKTORU, "m³"),
    "Kömür": (KOMUR_EMISYON_FAKTORU, "kg"),
    "Elektrikli": (ELEKTRIK_EMISYON_FAKTORU, "kWh"),
    "Fuel-oil": (FUELOIL_EMISYON_FAKTORU, "litre"),
    "Isı pompası": (ELEKTRIK_EMISYON_FAKTORU / ISI_POMPASI_COP, "kWh"),
}

# -----------------------------------------------
# FORM SEÇENEKLERİ
# -----------------------------------------------

SEKTOR_LISTESI = [
    "Otomotiv",
    "Gıda",
    "Tekstil",
    "Kimya",
    "Metal",
    "Plastik",
    "Elektronik",
    "Diğer",
]

ISINMA_TIPLERI = [
    "Doğalgaz",
    "Kömür",
    "Elektrikli",
    "Fuel-oil",
    "Isı pompası",
]

VARDIYA_DUZENLERI = {
    "Tek vardiya (8 saat)": 8,
    "Çift vardiya (16 saat)": 16,
    "Üç vardiya (24 saat)": 24,
}

# -----------------------------------------------
# GİRDİ LİMİTLERİ
# -----------------------------------------------

# Aylık elektrik tüketimi (kWh)
ELEKTRIK_MIN = 100
ELEKTRIK_MAX = 10_000_000
ELEKTRIK_VARSAYILAN = 50_000

# Üretim hattı sayısı
URETIM_HATTI_MIN = 1
URETIM_HATTI_MAX = 100
URETIM_HATTI_VARSAYILAN = 3

# Otomasyon seviyesi (0-10 arası slider)
OTOMASYON_MIN = 0
OTOMASYON_MAX = 10
OTOMASYON_VARSAYILAN = 3

# Tesis adı maksimum karakter sayısı
TESIS_ADI_MAX_UZUNLUK = 100

# -----------------------------------------------
# API AYARLARI
# -----------------------------------------------

# Anthropic model adı
CLAUDE_MODEL = "claude-sonnet-4-5"

# İlk analiz için maksimum token sayısı
ANALIZ_MAX_TOKENS = 2048

# Takip soruları için maksimum token sayısı
TAKIP_MAX_TOKENS = 1024

# -----------------------------------------------
# KG'DAN TON'A ÇEVİRME
# -----------------------------------------------
KG_TO_TON = 1000
