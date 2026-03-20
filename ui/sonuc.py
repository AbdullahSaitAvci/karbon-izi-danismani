# ============================================================
# sonuc.py — Analiz sonuçları ve sohbet geçmişi gösterim modülü
# Faz 2: chat_gecmisini_goster fonksiyonu eklendi.
# ============================================================

import streamlit as st
from utils.hesaplama import KarbonSonucu


def karbon_metriklerini_goster(sonuc: KarbonSonucu) -> None:
    """
    Karbon izi hesaplama sonuçlarını metrik kutuları olarak gösterir.

    Args:
        sonuc: KarbonSonucu veri sınıfı.
    """
    st.markdown("#### 📊 Hesaplanan Karbon İzi")

    sol, orta, sag = st.columns(3)

    with sol:
        st.metric(
            label="Aylık CO₂ Emisyonu",
            value=f"{sonuc.toplam_emisyon_ton:.2f} ton",
        )
    with orta:
        st.metric(
            label="Yıllık CO₂ Tahmini",
            value=f"{sonuc.yillik_emisyon_ton:.1f} ton",
        )
    with sag:
        elektrik_orani = (
            sonuc.elektrik_emisyon_kg / sonuc.toplam_emisyon_kg * 100
            if sonuc.toplam_emisyon_kg > 0
            else 0.0
        )
        st.metric(
            label="Elektrik Payı",
            value=f"%{elektrik_orani:.0f}",
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
    """Henüz analiz yapılmamışken karşılama ekranını gösterir."""
    st.markdown(
        """
        ### 👋 Hoş Geldiniz!

        Bu uygulama tesisinizin operasyonel verilerini analiz ederek
        **karbon ayak izinizi** hesaplar ve **otomasyon tabanlı iyileştirme
        önerileri** sunar.

        **Nasıl kullanılır:**
        1. Sol paneldeki formu tesis bilgilerinizle doldurun
        2. **"Analiz Et"** butonuna tıklayın
        3. AI danışmanınız size özel teknik tavsiyeler üretecek
        4. Analiz bittikten sonra **takip soruları** sorabilirsiniz

        **Analiz içeriği:**
        - Aylık ve yıllık CO₂ emisyon tahmini
        - Kısa vadeli (0-3 ay) düşük maliyetli öneriler
        - Uzun vadeli otomasyon, IoT sensör ve PLC tavsiyeleri
        - Tahmini verimlilik kazanımı ve yatırım geri dönüşü
        """
    )