# ============================================================
# constants.py — Proje genelinde kullanılan sabit değerler
# Tüm emisyon faktörleri, form seçenekleri ve limitler burada tanımlanır.
# Magic number kullanımını önlemek için her sabit buradan import edilir.
# ============================================================

# -----------------------------------------------
# EMİSYON FAKTÖRLERİ
# Kaynak: IPCC 2006 Kılavuzu, TEİAŞ yıllık raporları
# -----------------------------------------------

ELEKTRIK_EMISYON_FAKTORU = 0.47
DOGALGAZ_EMISYON_FAKTORU = 2.0
KOMUR_EMISYON_FAKTORU = 2.86
FUELOIL_EMISYON_FAKTORU = 3.15
ISI_POMPASI_COP = 3.5
ISINMA_ENERJI_ORANI = 0.30

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

ELEKTRIK_MIN = 100
ELEKTRIK_MAX = 10_000_000
ELEKTRIK_VARSAYILAN = 50_000

URETIM_HATTI_MIN = 1
URETIM_HATTI_MAX = 100
URETIM_HATTI_VARSAYILAN = 3

OTOMASYON_MIN = 0
OTOMASYON_MAX = 10
OTOMASYON_VARSAYILAN = 3

TESIS_ADI_MAX_UZUNLUK = 100

# -----------------------------------------------
# API AYARLARI
# -----------------------------------------------

CLAUDE_MODEL = "claude-sonnet-4-5"

# Token limitleri (v2 — optimize edilmiş)
#
# Önceki değerler: ANALIZ=2048, TAKIP=1024 → her ikisinde de kesilme oluyordu
# 4096 bile yetmedi çünkü Claude çok detaylı yazıyordu.
#
# Yeni strateji: Sistem promptunu kısalttık ("800 kelime aşma" dedik)
# + limitleri makul seviyede tuttuk. Claude artık 2048 içinde bitirecek
# çünkü prompt ona kısa yazmasını söylüyor.
#
# Eğer yine kesilirse 3072'ye çıkar, ama prompt optimize olduğu için
# 2048 yetmeli.
ANALIZ_MAX_TOKENS = 2048
TAKIP_MAX_TOKENS = 1536

# -----------------------------------------------
# KG'DAN TON'A ÇEVİRME
# -----------------------------------------------
KG_TO_TON = 1000

# -----------------------------------------------
# SOHBET GEÇMİŞİ ve TOKEN YÖNETİMİ
# -----------------------------------------------

MAX_GECMIS_MESAJ = 14
MAX_TAKIP_SORUSU = 15
# Son güncelleme: 2026-03-22
