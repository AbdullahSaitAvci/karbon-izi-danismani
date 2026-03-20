# ============================================================
# hesaplama.py — Karbon izi hesaplama fonksiyonları
# Elektrik ve ısınma kaynaklı CO₂ emisyonlarını hesaplar.
# Sonuçlar hem Claude'a gönderilecek prompt'a hem de UI'a aktarılır.
# ============================================================

from dataclasses import dataclass

from constants import (
    ELEKTRIK_EMISYON_FAKTORU,
    ISINMA_EMISYON_HARITASI,
    ISINMA_ENERJI_ORANI,
    KG_TO_TON,
)


@dataclass
class KarbonSonucu:
    """
    Karbon izi hesaplama sonuçlarını taşır.

    Attributes:
        elektrik_emisyon_kg: Elektrik kaynaklı aylık CO₂ emisyonu (kg).
        isinma_emisyon_kg: Isınma kaynaklı aylık CO₂ emisyonu (kg).
        toplam_emisyon_kg: Toplam aylık CO₂ emisyonu (kg).
        toplam_emisyon_ton: Toplam aylık CO₂ emisyonu (ton).
        yillik_emisyon_ton: Yıllık tahmini CO₂ emisyonu (ton).
    """
    elektrik_emisyon_kg: float
    isinma_emisyon_kg: float
    toplam_emisyon_kg: float
    toplam_emisyon_ton: float
    yillik_emisyon_ton: float


def elektrik_emisyonu_hesapla(aylik_tuketim_kwh: float) -> float:
    """
    Aylık elektrik tüketiminden CO₂ emisyonunu hesaplar.

    Args:
        aylik_tuketim_kwh: Aylık elektrik tüketimi (kWh).

    Returns:
        float: Aylık CO₂ emisyonu (kg).
    """
    return aylik_tuketim_kwh * ELEKTRIK_EMISYON_FAKTORU


def isinma_emisyonu_hesapla(
    aylik_tuketim_kwh: float,
    isinma_tipi: str,
) -> float:
    """
    Isınma kaynaklı CO₂ emisyonunu hesaplar.

    Isınma enerjisi ihtiyacı, toplam elektrik tüketiminin belirli bir
    oranı olarak tahmin edilir (ISINMA_ENERJI_ORANI sabiti).

    Args:
        aylik_tuketim_kwh: Aylık elektrik tüketimi (kWh) — referans değer.
        isinma_tipi: Isınma tipi (constants.ISINMA_TIPLERI'nden biri).

    Returns:
        float: Aylık ısınma kaynaklı CO₂ emisyonu (kg).

    Raises:
        ValueError: Geçersiz ısınma tipi verilirse.
    """
    if isinma_tipi not in ISINMA_EMISYON_HARITASI:
        raise ValueError(
            f"Geçersiz ısınma tipi: '{isinma_tipi}'. "
            f"Geçerli tipler: {list(ISINMA_EMISYON_HARITASI.keys())}"
        )

    # Isınma için harcanan tahmini enerji (kWh cinsinden)
    isinma_enerjisi_kwh = aylik_tuketim_kwh * ISINMA_ENERJI_ORANI

    emisyon_faktoru, _ = ISINMA_EMISYON_HARITASI[isinma_tipi]
    return isinma_enerjisi_kwh * emisyon_faktoru


def karbon_izi_hesapla(
    aylik_tuketim_kwh: float,
    isinma_tipi: str,
) -> KarbonSonucu:
    """
    Toplam karbon izi hesaplamasını yapar.

    Elektrik ve ısınma emisyonlarını ayrı ayrı hesaplayıp
    aylık ve yıllık toplamları döner.

    Args:
        aylik_tuketim_kwh: Aylık elektrik tüketimi (kWh).
        isinma_tipi: Isınma tipi adı.

    Returns:
        KarbonSonucu: Hesaplama sonuçlarını içeren veri sınıfı.
    """
    elektrik_kg = elektrik_emisyonu_hesapla(aylik_tuketim_kwh)
    isinma_kg = isinma_emisyonu_hesapla(aylik_tuketim_kwh, isinma_tipi)

    toplam_kg = elektrik_kg + isinma_kg
    toplam_ton = toplam_kg / KG_TO_TON
    # 12 ay üzerinden yıllık tahmin
    yillik_ton = toplam_ton * 12

    return KarbonSonucu(
        elektrik_emisyon_kg=round(elektrik_kg, 2),
        isinma_emisyon_kg=round(isinma_kg, 2),
        toplam_emisyon_kg=round(toplam_kg, 2),
        toplam_emisyon_ton=round(toplam_ton, 2),
        yillik_emisyon_ton=round(yillik_ton, 2),
    )
