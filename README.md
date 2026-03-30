# 🏭 AI-Powered Carbon Footprint & Automation Advisor

An AI-powered web application that analyzes factory operational data to calculate carbon footprint and provide specific industrial automation recommendations (PLC, IoT, SCADA) for energy efficiency.

**Built with:** Python · Streamlit · Claude API (Anthropic)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-karbon-izi-danismani.streamlit.app)

> 🔗 **Live Demo:** [ai-karbon-izi-danismani.streamlit.app](https://ai-karbon-izi-danismani.streamlit.app)

---

## ✨ Key Features

- **Carbon Footprint Calculation** — Deterministic Python-based CO₂ emission calculations using IPCC 2006 emission factors
- **AI-Powered Analysis** — Claude Sonnet 4.5 generates specific hardware recommendations (Siemens, Schneider, ABB) with cost estimates in Turkish Lira
- **Interactive Follow-up Chat** — Ask follow-up questions about the analysis; conversation context is preserved
- **Token Cost Management** — Smart message trimming keeps API costs under $0.05/session
- **Security** — Prompt injection protection with dual-layer filtering (pattern matching + XML wrapping)
- **Turkish Interface** — Fully localized for Turkish factory/facility engineers

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend & Backend | Streamlit 1.55 |
| LLM | Claude Sonnet 4.5 (Anthropic API) |
| Language | Python 3.12 |
| Deployment | Streamlit Community Cloud |
| Version Control | Git & GitHub |

## 📁 Project Structure

```
karbon-izi-danismani/
├── app.py                  # Main application entry point
├── constants.py            # All constants, emission factors, limits
├── requirements.txt        # Python dependencies
├── .gitignore
├── .streamlit/
│   └── secrets.toml        # API key (not in repo)
├── services/
│   └── claude_service.py   # Claude API integration & system prompt
├── ui/
│   ├── form.py             # Sidebar input form
│   └── sonuc.py            # Results display & chat history
└── utils/
    ├── dogrulama.py         # Input validation & security
    └── hesaplama.py         # Carbon footprint calculations
```

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/AbdullahSaitAvci/karbon-izi-danismani.git
cd karbon-izi-danismani

# Install dependencies
pip install -r requirements.txt

# Add your Anthropic API key
mkdir -p .streamlit
echo 'ANTHROPIC_API_KEY = "your-key-here"' > .streamlit/secrets.toml

# Run the application
streamlit run app.py
```

## 🔒 Security Features

- **Prompt Injection Protection:** User inputs are filtered against known injection patterns (Turkish & English) and wrapped in `<user_data>` XML tags
- **Input Validation:** All form fields validated with min/max limits before processing
- **API Key Protection:** Stored in `.streamlit/secrets.toml`, excluded from version control via `.gitignore`
- **Session Isolation:** Each user session is independent; data is not persisted

---

# 🇹🇷 Türkçe

## 🏭 AI Destekli Karbon İzi ve Otomasyon Danışmanı

Fabrika ve tesis operasyonel verilerini analiz ederek karbon ayak izini hesaplayan ve endüstriyel otomasyon (PLC, IoT, SCADA) tabanlı enerji verimliliği tavsiyeleri sunan yapay zeka destekli web uygulaması.

> 🔗 **Canlı Demo:** [ai-karbon-izi-danismani.streamlit.app](https://ai-karbon-izi-danismani.streamlit.app)

## 🎯 Ne Yapıyor?

1. **Veri Girişi:** Kullanıcı sol panelden tesis bilgilerini girer (elektrik tüketimi, ısınma tipi, üretim hattı sayısı, vardiya düzeni, otomasyon seviyesi)
2. **Karbon İzi Hesaplama:** Python tarafında IPCC 2006 emisyon faktörleri kullanılarak deterministik hesaplama yapılır
3. **AI Analiz:** Claude Sonnet 4.5, hesaplanan verileri temel alarak sektöre özel otomasyon tavsiyeleri üretir
4. **Takip Soruları:** Kullanıcı analiz hakkında sorular sorabilir, sistem sohbet geçmişini korur

## 📊 Örnek Analiz Çıktısı

Uygulama şu bilgileri sunar:
- Aylık ve yıllık CO₂ emisyon tahmini (ton cinsinden)
- Sektör ortalamasıyla karşılaştırma
- Kısa vadeli öneriler (0-3 ay): LED aydınlatma, kompresör bakımı, PLC parametre optimizasyonu
- Uzun vadeli öneriler: Spesifik PLC modelleri (Siemens S7-1200, Schneider Modicon M241), IoT sensör tipleri, SCADA yazılımları
- Tahmini maliyet aralıkları (₺ cinsinden) ve yatırım geri dönüş süresi

## ⚙️ Teknik Detaylar

### Emisyon Faktörleri
| Kaynak | Faktör | Birim |
|--------|--------|-------|
| Elektrik (Türkiye şebeke ortalaması) | 0.47 | kg CO₂/kWh |
| Doğalgaz | 2.0 | kg CO₂/m³ |
| Kömür | 2.86 | kg CO₂/kg |
| Fuel-oil | 3.15 | kg CO₂/litre |

*Kaynak: IPCC 2006 Kılavuzu, TEİAŞ yıllık raporları*

### Token Yönetimi
- İlk analiz: ~1500 token (~3 cent/analiz)
- Takip sorusu: ~1000 token (~2 cent/soru)
- Sohbet geçmişi kırpma: İlk 2 mesaj (analiz çekirdeği) korunur, son 14 mesaj tutulur
- Oturum başına maksimum 15 takip sorusu

### Güvenlik
- İki katmanlı prompt injection koruması (kalıp filtreleme + XML sarmalama)
- Tüm kullanıcı girdileri `<user_data>` tag'leri içinde Claude'a gönderilir
- Hesaplamalar Python'da yapılır, Claude'a sadece yorum ve öneri üretmesi için gönderilir (LLM halüsinasyonu önlenir)

## 🏗️ Proje Bağlamı

Bu proje, [YGA](https://yga.org.tr/) ve [UP School](https://upschool.com/) tarafından Citi Foundation desteğiyle yürütülen **Future Talent Program** (201 modülü) kapsamında geliştirilmiştir. Program; AI, Büyük Veri, Otomasyon ve GreenTech alanlarında uzmanlaşmayı hedeflemektedir.

**Eğitmenler ve katkıda bulunanlar:**
- Yağmur Yıldız Parıltı — Yapay Zeka ile Uygulama Geliştirme
- Hakan Şençiçek & Mehmet Özalp (Schneider Electric) — Otomasyon, Robotik ve PLC
- Cihan Özel & Şahin Çağlayan (Faradai) — GreenTech

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👤 Geliştirici

**Abdullah Sait Avcı**
- 🎓 Sakarya Üniversitesi — Bilgisayar Mühendisliği (3. Sınıf)
- 🔗 [GitHub](https://github.com/AbdullahSaitAvci)
- 🔗 [LinkedIn](https://www.linkedin.com/in/abdullah-sait-avci)
