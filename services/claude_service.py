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
)

# Loglama yapılandırması
logger = logging.getLogger(__name__)

# -----------------------------------------------
# SİSTEM PROMPTU
# Claude'a endüstriyel otomasyon danışmanı rolü veriyoruz.
# Her yanıtta belirli bir yapıyı takip etmesini istiyoruz.
# -----------------------------------------------
SISTEM_PROMPTU = """Sen bir endüstriyel otomasyon ve enerji verimliliği danışmanısın.
Görevin: Fabrika ve tesis operasyonel verilerini analiz ederek karbon ayak izini
değerlendirmek ve otomasyon tabanlı somut iyileştirme önerileri sunmak.

YANITLARIN HER ZAMAN ŞU YAPIYI TAKİP ETMELİDİR:

## 📊 Karbon İzi Değerlendirmesi
- Verilen bilgiler ışığında aylık tahmini CO₂ emisyonu (ton cinsinden)
- Türkiye sektör ortalamasıyla kısa bir karşılaştırma
- Hangi kaynağın (elektrik, ısınma) ne kadar emisyona sebep olduğunun dökümü

## ⚡ Kısa Vadeli Öneriler (0-3 ay)
- Düşük maliyetli, hemen uygulanabilir adımlar
- PLC parametre optimizasyonu (spesifik parametre adlarıyla)
- Sensör kalibrasyonu, enerji izleme yazılımı gibi pratik öneriler
- Her önerinin tahmini tasarruf etkisini yüzde olarak belirt

## 🏭 Uzun Vadeli Otomasyon / IoT / PLC Tavsiyeleri
- Spesifik donanım önerileri (marka ve model adıyla, örn: Siemens S7-1500, Schneider Modicon M340)
- IoT sensör tipleri ve yerleşim önerileri (örn: sıcaklık, nem, enerji analizörü)
- PLC program optimizasyonu detayları
- SCADA entegrasyon önerileri
- Her öneri için tahmini maliyet aralığı (TL cinsinden)
- Uygulama öncelik sırası

## 📈 Tahmini Verimlilik Kazanımı
- Toplam enerji tasarrufu yüzdesi
- Toplam CO₂ azaltma yüzdesi
- Tahmini yatırım geri dönüş süresi (ay)

ÖNEMLİ KURALLAR:
- Tüm yanıtlarını Türkçe ver.
- Yüzeysel "enerji tasarruflu cihaz kullanın" gibi öneriler verme.
  Spesifik donanım modeli, protokol adı (Modbus, OPC-UA, MQTT), PLC programı önerisi sun.
- Eğer bir varsayım yapıyorsan, bunu açıkça belirt.
- Kullanıcı takip sorusu sorduğunda önceki bağlamı koru ve tutarlı ol.
- Maliyet tahminlerinde Türkiye piyasa koşullarını göz önünde bulundur.
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


def analiz_istegi_gonder(
    mesajlar: list[dict],
    ilk_analiz: bool = True,
) -> Optional[str]:
    """
    Claude API'ye mesaj geçmişiyle birlikte istek gönderir.

    Args:
        mesajlar: Kullanıcı ve asistan mesajlarını içeren liste.
                  Her eleman {"role": "user"|"assistant", "content": "..."} formatında.
        ilk_analiz: True ise ANALIZ_MAX_TOKENS, False ise TAKIP_MAX_TOKENS kullanılır.

    Returns:
        str veya None: Claude'un yanıt metni. Hata durumunda None döner.

    Raises:
        anthropic.APIConnectionError: API'ye bağlanılamazsa.
        anthropic.RateLimitError: İstek limiti aşılırsa.
        anthropic.APIStatusError: API durum hatası oluşursa.
    """
    max_tokens = ANALIZ_MAX_TOKENS if ilk_analiz else TAKIP_MAX_TOKENS

    try:
        istemci = _api_istemcisi_olustur()
    except KeyError:
        # Hata mesajı _api_istemcisi_olustur içinde loglandı
        return None

    try:
        yanit = istemci.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=max_tokens,
            system=SISTEM_PROMPTU,
            messages=mesajlar,
        )
        # Yanıttan metin içeriğini çıkar
        yanit_metni = yanit.content[0].text
        logger.info("API yanıtı başarıyla alındı (%d karakter)", len(yanit_metni))
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
        logger.error("API durum hatası (kod: %d): %s", hata.status_code, hata.message)
        st.error(
            f"⚠️ API hatası (kod: {hata.status_code}). "
            "Lütfen daha sonra tekrar deneyin."
        )
        return None
