# ============================================================
# claude_service.py — Anthropic API ile iletişim modülü
# Tüm Claude API çağrıları bu dosyadan yapılır.
# app.py veya diğer modüller doğrudan API çağrısı YAPMAZ.
# ============================================================

import logging
from typing import Optional

import anthropic
import streamlit as st

from constants import (
    CLAUDE_MODEL,
    ANALIZ_MAX_TOKENS,
    TAKIP_MAX_TOKENS,
    MAX_GECMIS_MESAJ,
)

logger = logging.getLogger(__name__)

# -----------------------------------------------
# SİSTEM PROMPTU (v2 — optimize edilmiş)
#
# Önceki versiyon çok detaylı çıktı üretiyordu:
#   - İlk analiz 4096 token'a sığmıyordu
#   - Takip soruları 2048'i aşıyordu
#   - Her öneri için 3-4 paragraf yazıyordu
#
# Bu versiyonda:
#   - "KISA VE ÖZ" talimatı açıkça verildi
#   - Her bölüm için satır limiti konuldu
#   - Detay takip sorularına bırakıldı
# -----------------------------------------------
SISTEM_PROMPTU = """Sen bir endüstriyel otomasyon ve enerji verimliliği danışmanısın.
Görevin: Fabrika verilerini analiz edip karbon ayak izi değerlendirmesi ve otomasyon önerileri sunmak.

YANITIN YAPISI (HER BÖLÜM KISA VE ÖZ — toplam 600-800 kelime):

## 📊 Karbon İzi Değerlendirmesi
- <calculated_carbon_footprint> değerlerini AYNEN kullan, yeniden hesaplama YAPMA
- Sektör ortalamasıyla 1-2 cümle karşılaştırma
- Elektrik/ısınma dağılımını 1-2 cümle yorumla

## ⚡ Kısa Vadeli Öneriler (0-3 ay)
- 3-4 öneri yeterli, her biri 2-3 satır
- Spesifik donanım adı + tahmini tasarruf yüzdesi
- Toplam kısa vadeli tasarruf özeti (1 satır)

## 🏭 Uzun Vadeli Otomasyon Tavsiyeleri
- EN ÖNEMLİ 3 öneriyi seç (6 tane yazma!)
- Her biri: donanım adı + maliyet aralığı + tasarruf yüzdesi (3-4 satır)
- Protokol bilgisi (Modbus, OPC-UA vb.) kısa not olarak

## 📈 Verimlilik Özeti
- Toplam tasarruf yüzdesi (1 satır)
- Toplam CO₂ azaltma (1 satır)
- Tahmini geri dönüş süresi (1 satır)

KRİTİK KURALLAR:
- Türkçe yaz.
- KISA VE ÖZ ol. Detayları kullanıcı takip sorusuyla sorabilir.
- Her öneri için uzun paragraflar yazma, madde işareti kullan.
- Toplam yanıt 800 kelimeyi AŞMASIN.
- Spesifik ol: marka, model, protokol adı ver ama açıklamayı kısa tut.
- Varsayım yaparsan 1 cümleyle belirt.
- Maliyet tahminlerinde Türkiye piyasasını baz al.
"""


def _api_istemcisi_olustur() -> anthropic.Anthropic:
    """
    Anthropic API istemcisini oluşturur.

    Returns:
        anthropic.Anthropic: Yapılandırılmış API istemcisi.

    Raises:
        KeyError: API anahtarı secrets.toml'da bulunamazsa.
    """
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except KeyError as hata:
        logger.error("ANTHROPIC_API_KEY bulunamadı: %s", hata)
        raise KeyError(
            "API anahtarı bulunamadı. Lütfen .streamlit/secrets.toml dosyasını kontrol edin."
        ) from hata

    return anthropic.Anthropic(api_key=api_key)


def _mesajlari_kirp(mesajlar: list[dict]) -> list[dict]:
    """
    Sohbet geçmişini API'ye göndermeden önce kırpar.

    Strateji:
    ─────────
    İlk 2 mesaj (analiz talebi + ilk AI yanıtı) HER ZAMAN korunur.
    Geri kalan mesajlardan son MAX_GECMIS_MESAJ tanesi tutulur.

    Args:
        mesajlar: Tüm sohbet geçmişi listesi.

    Returns:
        list[dict]: API'ye gönderilecek kırpılmış mesaj listesi.
    """
    toplam = len(mesajlar)

    if toplam <= 2 + MAX_GECMIS_MESAJ:
        return mesajlar

    cekirdek = mesajlar[:2]
    son_kisim = mesajlar[-MAX_GECMIS_MESAJ:]
    atlanan = toplam - 2 - MAX_GECMIS_MESAJ

    logger.info(
        "Sohbet geçmişi kırpıldı: %d mesajdan %d'i atlandı, %d mesaj gönderiliyor",
        toplam,
        atlanan,
        2 + 1 + MAX_GECMIS_MESAJ,
    )

    kopru = {
        "role": "user",
        "content": (
            f"[Sistem notu: Aradaki {atlanan} mesaj bağlam penceresi "
            f"nedeniyle kısaltıldı. Yukarıdaki ilk analizi referans alarak "
            f"aşağıdaki son mesajlarla devam et.]"
        ),
    }

    if son_kisim[0]["role"] == "user":
        return cekirdek + son_kisim
    else:
        return cekirdek + [kopru] + son_kisim


def kullanim_sayacini_guncelle() -> int:
    """
    Oturumdaki API çağrı sayısını takip eder.

    Returns:
        int: Güncel toplam API çağrı sayısı.
    """
    if "api_cagri_sayisi" not in st.session_state:
        st.session_state["api_cagri_sayisi"] = 0

    st.session_state["api_cagri_sayisi"] += 1
    return st.session_state["api_cagri_sayisi"]


def analiz_istegi_gonder(
    mesajlar: list[dict],
    ilk_analiz: bool = True,
) -> Optional[str]:
    """
    Claude API'ye mesaj geçmişiyle birlikte istek gönderir.

    Args:
        mesajlar: Kullanıcı ve asistan mesajlarını içeren liste.
        ilk_analiz: True ise ANALIZ_MAX_TOKENS, False ise TAKIP_MAX_TOKENS kullanılır.

    Returns:
        str veya None: Claude'un yanıt metni. Hata durumunda None döner.
    """
    max_tokens = ANALIZ_MAX_TOKENS if ilk_analiz else TAKIP_MAX_TOKENS

    try:
        istemci = _api_istemcisi_olustur()
    except KeyError:
        return None

    gonderilecek_mesajlar = mesajlar if ilk_analiz else _mesajlari_kirp(mesajlar)

    try:
        yanit = istemci.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=max_tokens,
            system=SISTEM_PROMPTU,
            messages=gonderilecek_mesajlar,
        )

        yanit_metni = yanit.content[0].text

        # Kesilme kontrolü
        if yanit.stop_reason == "max_tokens":
            logger.warning(
                "⚠️ Yanıt token limitine ulaştığı için kesildi! "
                "max_tokens=%d, ilk_analiz=%s",
                max_tokens,
                ilk_analiz,
            )
            yanit_metni += "\n\n---\n*💡 Daha detaylı bilgi için takip sorusu sorabilirsiniz.*"

        cagri_no = kullanim_sayacini_guncelle()

        logger.info(
            "API yanıtı #%d | Gönderilen: %d mesaj | "
            "Girdi token: %d | Çıktı token: %d | Kesildi: %s",
            cagri_no,
            len(gonderilecek_mesajlar),
            yanit.usage.input_tokens,
            yanit.usage.output_tokens,
            yanit.stop_reason == "max_tokens",
        )

        return yanit_metni

    except anthropic.APIConnectionError as hata:
        logger.error("API bağlantı hatası: %s", hata)
        st.error(
            "⚠️ Claude API'ye bağlanılamadı. "
            "İnternet bağlantınızı kontrol edip tekrar deneyin."
        )
        return None

    except anthropic.RateLimitError as hata:
        logger.error("API istek limiti aşıldı: %s", hata)
        st.error(
            "⚠️ API istek limiti aşıldı. "
            "Lütfen birkaç dakika bekleyip tekrar deneyin."
        )
        return None

    except anthropic.APIStatusError as hata:
        logger.error(
            "API durum hatası (kod: %d): %s", hata.status_code, hata.message
        )
        st.error(
            f"⚠️ API hatası (kod: {hata.status_code}). "
            "Lütfen daha sonra tekrar deneyin."
        )
        return None