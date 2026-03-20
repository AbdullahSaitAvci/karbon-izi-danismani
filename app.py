# ============================================================
# app.py — AI Destekli Karbon İzi ve Otomasyon Danışmanı
# Ana uygulama dosyası. Faz 2: conversation history eklendi.
# ============================================================

import logging
import streamlit as st

from ui.form import sidebar_formu_goster
from ui.sonuc import (
    karbon_metriklerini_goster,
    ai_yanitini_goster,
    chat_gecmisini_goster,
    hosgeldin_mesaji_goster,
)
from utils.dogrulama import tum_alanlari_dogrula
from utils.hesaplama import karbon_izi_hesapla
from services.claude_service import analiz_istegi_gonder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Karbon İzi Danışmanı",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _session_state_baslat() -> None:
    """Oturum değişkenlerini başlatır, zaten varsa dokunmaz."""
    varsayilanlar = {
        "mesajlar": [],
        "analiz_yapildi": False,
        "karbon_sonucu": None,
        "son_yanit": None,
    }
    for anahtar, deger in varsayilanlar.items():
        if anahtar not in st.session_state:
            st.session_state[anahtar] = deger


def _kullanici_mesaji_olustur(form_verisi) -> str:
    """
    Form verisinden Claude'a gönderilecek ilk analiz mesajını oluşturur.

    Args:
        form_verisi: FormVerisi dataclass'ı.

    Returns:
        str: Formatlı analiz talebi metni.
    """
    return (
        f"Aşağıdaki tesis verilerini analiz et:\n\n"
        f"- **Tesis Adı:** {form_verisi.tesis_adi}\n"
        f"- **Sektör:** {form_verisi.sektor}\n"
        f"- **Aylık Elektrik Tüketimi:** {form_verisi.elektrik_tuketimi:,.0f} kWh\n"
        f"- **Isınma Tipi:** {form_verisi.isinma_tipi}\n"
        f"- **Üretim Hattı Sayısı:** {form_verisi.uretim_hatti}\n"
        f"- **Vardiya Düzeni:** {form_verisi.vardiya} ({form_verisi.vardiya_saat} saat)\n"
        f"- **Mevcut Otomasyon Seviyesi:** {form_verisi.otomasyon_seviyesi}/10\n\n"
        f"Lütfen karbon izi hesabı, kısa vadeli öneriler, uzun vadeli "
        f"otomasyon/IoT/PLC tavsiyeleri ve verimlilik kazanımı tahminini sun."
    )


def _analiz_yap(form_verisi) -> None:
    """
    Formu doğrular, karbon izini hesaplar ve ilk Claude analizini başlatır.

    Args:
        form_verisi: Kullanıcının doldurduğu form verileri.
    """
    hatalar = tum_alanlari_dogrula(
        tesis_adi=form_verisi.tesis_adi,
        elektrik_tuketimi=form_verisi.elektrik_tuketimi,
        uretim_hatti=form_verisi.uretim_hatti,
        otomasyon_seviyesi=form_verisi.otomasyon_seviyesi,
    )

    if hatalar:
        for hata in hatalar:
            st.error(f"❌ {hata.mesaj}")
        return

    # Karbon izi hesapla ve kaydet
    karbon_sonucu = karbon_izi_hesapla(
        aylik_tuketim_kwh=form_verisi.elektrik_tuketimi,
        isinma_tipi=form_verisi.isinma_tipi,
    )
    st.session_state["karbon_sonucu"] = karbon_sonucu

    # Yeni analiz — sohbet geçmişini sıfırla
    kullanici_mesaji = _kullanici_mesaji_olustur(form_verisi)
    st.session_state["mesajlar"] = [
        {"role": "user", "content": kullanici_mesaji}
    ]

    with st.spinner("🔄 AI danışmanınız analiz hazırlıyor..."):
        yanit = analiz_istegi_gonder(
            mesajlar=st.session_state["mesajlar"],
            ilk_analiz=True,
        )

    if yanit:
        st.session_state["mesajlar"].append(
            {"role": "assistant", "content": yanit}
        )
        st.session_state["son_yanit"] = yanit
        st.session_state["analiz_yapildi"] = True
        logger.info("Analiz tamamlandı: %s", form_verisi.tesis_adi)
    else:
        st.error("❌ Analiz oluşturulamadı. API anahtarınızı kontrol edin.")


def _takip_sorusu_isle(soru: str) -> None:
    """
    Kullanıcının takip sorusunu mevcut sohbet geçmişine ekler ve yanıt alır.

    Args:
        soru: Kullanıcının yazdığı takip sorusu metni.
    """
    if not soru.strip():
        return

    # Kullanıcı mesajını geçmişe ekle
    st.session_state["mesajlar"].append(
        {"role": "user", "content": soru}
    )

    with st.spinner("🔄 Yanıt hazırlanıyor..."):
        yanit = analiz_istegi_gonder(
            mesajlar=st.session_state["mesajlar"],
            ilk_analiz=False,
        )

    if yanit:
        st.session_state["mesajlar"].append(
            {"role": "assistant", "content": yanit}
        )
        logger.info("Takip sorusu yanıtlandı (%d karakter)", len(yanit))
    else:
        st.error("❌ Yanıt alınamadı. Lütfen tekrar deneyin.")


def _sonuclari_ve_chati_goster() -> None:
    """
    Karbon metriklerini, ilk analizi, sohbet geçmişini ve chat kutusunu gösterir.
    """
    karbon_sonucu = st.session_state.get("karbon_sonucu")
    mesajlar = st.session_state.get("mesajlar", [])

    if karbon_sonucu:
        karbon_metriklerini_goster(karbon_sonucu)

    # İlk analiz yanıtını göster (mesajlar[1] = ilk asistan yanıtı)
    if len(mesajlar) >= 2:
        ai_yanitini_goster(mesajlar[1]["content"])

    # Faz 2: 2'den fazla mesaj varsa takip sohbetini göster
    if len(mesajlar) > 2:
        chat_gecmisini_goster(mesajlar[2:])

    # Chat giriş kutusu
    st.markdown("---")
    st.markdown("##### 💬 Danışmanınıza Soru Sorun")
    st.caption("Analiz sonuçları hakkında takip soruları sorabilirsiniz.")

    # Chat input — her rerun'da temizlenir, key ile kontrol edilir
    takip_sorusu = st.chat_input(
        "Örn: Bu PLC'nin daha ucuz alternatifi var mı?",
    )

    if takip_sorusu:
        _takip_sorusu_isle(takip_sorusu)
        st.rerun()  # noqa: rerun burada zorunlu


def main() -> None:
    """Ana uygulama akışı: başlık, form, analiz ve sohbet."""
    _session_state_baslat()

    # Başlık — daha sade
    st.markdown("## 🏭 Karbon İzi ve Otomasyon Danışmanı")
    st.caption(
        "Tesis verilerinizi girin, yapay zeka destekli kişiselleştirilmiş "
        "otomasyon ve enerji verimliliği tavsiyeleri alın."
    )

    form_verisi = sidebar_formu_goster()

    if form_verisi:
        _analiz_yap(form_verisi)

    if st.session_state.get("analiz_yapildi"):
        _sonuclari_ve_chati_goster()
    else:
        hosgeldin_mesaji_goster()


if __name__ == "__main__":
    main()