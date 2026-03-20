# 🏭 AI Destekli Karbon İzi ve Otomasyon Danışmanı

Fabrika ve tesisler için yapay zeka destekli karbon ayak izi hesaplama ve otomasyon danışmanlığı uygulaması.

## 🎯 Ne Yapıyor?

Tesis operasyonel verilerini (elektrik tüketimi, ısınma tipi, üretim hattı sayısı vb.) analiz ederek:

- Aylık ve yıllık CO₂ emisyonu hesaplar
- Kısa vadeli (0-3 ay) düşük maliyetli öneriler sunar
- Spesifik donanım önerileriyle uzun vadeli otomasyon/IoT/PLC tavsiyeleri verir
- Tahmini verimlilik kazanımı ve yatırım geri dönüş süresi hesaplar
- Takip soruları sormanıza olanak tanır

## 🛠️ Teknolojiler

- **Python 3.11+**
- **Streamlit** — web arayüzü
- **Anthropic Claude API** — AI analiz motoru

## 🚀 Kurulum

1. Repoyu klonla:
```bash
git clone https://github.com/AbdullahSaitAvci/AI-Destekli-Karbon-zi-ve-Otomasyon-Dan-man-.git
cd AI-Destekli-Karbon-zi-ve-Otomasyon-Dan-man-
```

2. Bağımlılıkları yükle:
```bash
pip install -r requirements.txt
```

3. API anahtarını ekle:
```bash
# .streamlit/secrets.toml dosyası oluştur
ANTHROPIC_API_KEY = "sk-ant-..."
```

4. Uygulamayı başlat:
```bash
streamlit run app.py
```

## 📁 Proje Yapısı
```
karbon-danismani/
├── app.py                  # Ana uygulama akışı
├── constants.py            # Sabitler ve emisyon faktörleri
├── services/
│   └── claude_service.py   # Claude API entegrasyonu
├── ui/
│   ├── form.py             # Sidebar form bileşeni
│   └── sonuc.py            # Sonuç gösterim bileşeni
└── utils/
    ├── dogrulama.py        # Girdi doğrulama
    └── hesaplama.py        # Karbon izi hesaplama
```

## 🌱 YGA Future Talent Program

Bu proje YGA & UP School Future Talent Programı (AI, Big Data, Automation) 201 modülü bitirme projesi olarak geliştirilmiştir.
