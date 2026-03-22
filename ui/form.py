# ============================================================
# form.py — Sidebar'daki kullanıcı veri giriş formu
# Tesis bilgileri bu form üzerinden toplanır.
# ============================================================

from dataclasses import dataclass
from typing import Optional

import streamlit as st

from constants import (
    SEKTOR_LISTESI,
    ISINMA_TIPLERI,
    VARDIYA_DUZENLERI,
    ELEKTRIK_MIN,
    ELEKTRIK_MAX,
    ELEKTRIK_VARSAYILAN,
    URETIM_HATTI_MIN,
    URETIM_HATTI_MAX,
    URETIM_HATTI_VARSAYILAN,
    OTOMASYON_MIN,
    OTOMASYON_MAX,
    OTOMASYON_VARSAYILAN,
    TESIS_ADI_MAX_UZUNLUK,
)


@dataclass
class FormVerisi:
    """
    Kullanıcının formdan girdiği tüm verileri taşır.

    Attributes:
        tesis_adi: Tesis veya fabrikanın adı.
        sektor: Faaliyet gösterilen sektör.
        elektrik_tuketimi: Aylık elektrik tüketimi (kWh).
        isinma_tipi: Kullanılan ısınma yöntemi.
        uretim_hatti: Aktif üretim hattı sayısı.
        vardiya: Vardiya düzeni açıklaması.
        vardiya_saat: Vardiya süresi (saat).
        otomasyon_seviyesi: 0-10 arası mevcut otomasyon seviyesi.
    """
    tesis_adi: str
    sektor: str
    elektrik_tuketimi: float
    isinma_tipi: str
    uretim_hatti: int
    vardiya: str
    vardiya_saat: int
    otomasyon_seviyesi: int


def sidebar_formu_goster() -> Optional[FormVerisi]:
    """
    Sidebar'da tesis bilgi formunu gösterir.

    Kullanıcı formu doldurup "Analiz Et" butonuna bastığında
    FormVerisi döner. Butona basılmadıysa None döner.

    Returns:
        FormVerisi veya None: Form gönderildiyse veri, gönderilmediyse None.
    """
    st.sidebar.title("🏭 Karbon İzi Danışmanı")
    st.sidebar.caption("v1.0 | YGA Future Talent Program")
    st.sidebar.divider()

    st.sidebar.header("🏭 Tesis Bilgileri")
    st.sidebar.caption("Analiz için tesis verilerinizi girin.")

    # --- Form alanları ---
    tesis_adi = st.sidebar.text_input(
        "Tesis Adı",
        max_chars=TESIS_ADI_MAX_UZUNLUK,
        placeholder="Örn: ABC Otomotiv Fabrikası",
    )

    sektor = st.sidebar.selectbox(
        "Sektör",
        options=SEKTOR_LISTESI,
    )

    elektrik_tuketimi = st.sidebar.number_input(
        "Aylık Elektrik Tüketimi (kWh)",
        min_value=ELEKTRIK_MIN,
        max_value=ELEKTRIK_MAX,
        value=ELEKTRIK_VARSAYILAN,
        step=1000,
        help="Tesisinizin aylık ortalama elektrik tüketimini kWh olarak girin.",
    )

    isinma_tipi = st.sidebar.selectbox(
        "Isınma Tipi",
        options=ISINMA_TIPLERI,
    )

    uretim_hatti = st.sidebar.number_input(
        "Üretim Hattı Sayısı",
        min_value=URETIM_HATTI_MIN,
        max_value=URETIM_HATTI_MAX,
        value=URETIM_HATTI_VARSAYILAN,
        step=1,
    )

    vardiya = st.sidebar.selectbox(
        "Vardiya Düzeni",
        options=list(VARDIYA_DUZENLERI.keys()),
    )

    otomasyon_seviyesi = st.sidebar.slider(
        "Mevcut Otomasyon Seviyesi",
        min_value=OTOMASYON_MIN,
        max_value=OTOMASYON_MAX,
        value=OTOMASYON_VARSAYILAN,
        help="0 = Tamamen manuel, 10 = Tam otomasyon",
    )

    # --- Analiz butonu ---
    analiz_basildi = st.sidebar.button(
        "🔍 Analiz Et",
        use_container_width=True,
        type="primary",
    )

    st.sidebar.divider()
    st.sidebar.caption(
        "🔒 Verileriniz yalnızca analiz süresince işlenir, kalıcı olarak saklanmaz.\n"
        "Sayfa yenilendiğinde tüm veriler silinir.\n"
        "Analiz için Anthropic Claude API kullanılmaktadır."
    )

    if analiz_basildi:
        return FormVerisi(
            tesis_adi=tesis_adi,
            sektor=sektor,
            elektrik_tuketimi=float(elektrik_tuketimi),
            isinma_tipi=isinma_tipi,
            uretim_hatti=int(uretim_hatti),
            vardiya=vardiya,
            vardiya_saat=VARDIYA_DUZENLERI[vardiya],
            otomasyon_seviyesi=otomasyon_seviyesi,
        )

    return None
