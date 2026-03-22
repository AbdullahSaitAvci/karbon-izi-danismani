# ============================================================
# sonuc.py — Analiz sonuçları ve sohbet geçmişi gösterim modülü
# Faz 2: chat_gecmisini_goster fonksiyonu eklendi.
# ============================================================

import streamlit as st

from constants import KG_TO_TON
from utils.hesaplama import KarbonSonucu


def karbon_metriklerini_goster(sonuc: KarbonSonucu) -> None:
    """
    Karbon izi hesaplama sonuçlarını metrik kutuları olarak gösterir.

    Args:
        sonuc: KarbonSonucu veri sınıfı.
    """
    st.markdown("#### 📊 Hesaplanan Karbon İzi")
    st.caption("IPCC 2006 emisyon faktörleri kullanılarak hesaplanmıştır.")

    sol, orta, sag = st.columns(3)

    elektrik_orani = (
        sonuc.elektrik_emisyon_kg / sonuc.toplam_emisyon_kg * 100
        if sonuc.toplam_emisyon_kg > 0
        else 0.0
    )
    isinma_ton = sonuc.isinma_emisyon_kg / KG_TO_TON
    diger_oran = 100.0 - elektrik_orani

    with sol:
        st.metric(
            label="Aylık CO₂ Emisyonu",
            value=f"{sonuc.toplam_emisyon_ton:.2f} ton",
            delta=round(isinma_ton, 2) if sonuc.toplam_emisyon_kg > 0 else None,
            delta_color="inverse",
            help="Alt gösterge: ısınma kaynaklı aylık CO₂ (ton).",
        )
    with orta:
        yillik_artis = sonuc.yillik_emisyon_ton - sonuc.toplam_emisyon_ton
        st.metric(
            label="Yıllık CO₂ Tahmini",
            value=f"{sonuc.yillik_emisyon_ton:.1f} ton",
            delta=round(yillik_artis, 2) if sonuc.toplam_emisyon_kg > 0 else None,
            delta_color="inverse",
            help="Alt gösterge: yıllık toplam ile tek ay arasındaki fark (ton, ×12 projeksiyonu).",
        )
    with sag:
        st.metric(
            label="Elektrik Payı",
            value=f"%{elektrik_orani:.0f}",
            delta=round(diger_oran, 1) if sonuc.toplam_emisyon_kg > 0 else None,
            delta_color="inverse",
            help="Alt gösterge: ısınmanın toplam emisyondaki payı (%).",
        )

    st.divider()


def ai_yanitini_goster(yanit: str) -> None:
    """
    İlk Claude analiz yanıtını gösterir.

    Args:
        yanit: Claude API'den dönen ilk analiz metni.
    """
    st.markdown("#### 🤖 AI Danışman Analizi")
    st.markdown(yanit)

    if st.session_state.get("_sonuc_last_ai_yanit") != yanit:
        st.session_state["ai_rapor_kopyala_acik"] = False
    st.session_state["_sonuc_last_ai_yanit"] = yanit

    if st.button("📋 Raporu Kopyala", key="ai_rapor_kopyala_btn"):
        st.session_state["ai_rapor_kopyala_acik"] = True
    if st.session_state.get("ai_rapor_kopyala_acik"):
        st.code(yanit, language=None)

    st.divider()


def chat_gecmisini_goster(mesajlar: list) -> None:
    """
    İlk analizden sonraki takip soru-cevaplarını chat baloncukları olarak gösterir.

    Args:
        mesajlar: İlk iki mesajdan sonraki sohbet geçmişi listesi.
                  Her eleman {"role": "user"|"assistant", "content": "..."} formatında.
    """
    st.markdown("#### 💬 Sohbet Geçmişi")

    for mesaj in mesajlar:
        if mesaj["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(mesaj["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(mesaj["content"])


def hosgeldin_mesaji_goster() -> None:
    """Henüz analiz yapılmamışken karşılama ekranını modern kartlarla gösterir."""
    st.markdown("### 👋 Hoş Geldiniz!")

    kolonlar = st.columns(3)
    kart_bilgileri = [
        {
            "emoji": "📊",
            "baslik": "Karbon İzi Hesaplama",
            "alt": "Tesisinizin aylık ve yıllık CO₂ emisyonunu hesaplayın"
        },
        {
            "emoji": "🤖",
            "baslik": "AI Danışman",
            "alt": "Yapay zeka destekli kişiselleştirilmiş otomasyon tavsiyeleri alın"
        },
        {
            "emoji": "💬",
            "baslik": "Soru-Cevap",
            "alt": "Analiz sonrası takip soruları sorun, detaylı bilgi alın"
        },
    ]

    for idx, kolon in enumerate(kolonlar):
        with kolon:
            with st.container(border=True):
                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<span style='font-size:2.1em;'>{kart_bilgileri[idx]['emoji']}</span><br>"
                    f"<span style='font-size:1.25em; font-weight:bold'>{kart_bilgileri[idx]['baslik']}</span><br>"
                    f"<span style='color:grey'>{kart_bilgileri[idx]['alt']}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    st.info("👈 Başlamak için sol panelden tesis bilgilerinizi girin ve 'Analiz Et' butonuna tıklayın.")