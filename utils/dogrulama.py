# ============================================================
# dogrulama.py — Kullanıcı girdilerini doğrulama ve temizleme
# Form'dan gelen veriler API'ye gönderilmeden önce burada kontrol edilir.
# ============================================================

from dataclasses import dataclass

from constants import (
    ELEKTRIK_MIN,
    ELEKTRIK_MAX,
    URETIM_HATTI_MIN,
    URETIM_HATTI_MAX,
    OTOMASYON_MIN,
    OTOMASYON_MAX,
    TESIS_ADI_MAX_UZUNLUK,
)


@dataclass
class DogrulamaHatasi:
    """
    Doğrulama sonucunda oluşan hata bilgisini taşır.

    Attributes:
        alan: Hatanın oluştuğu form alanının adı.
        mesaj: Kullanıcıya gösterilecek Türkçe hata mesajı.
    """
    alan: str
    mesaj: str


def tesis_adi_dogrula(tesis_adi: str) -> list[DogrulamaHatasi]:
    """
    Tesis adı alanını doğrular.

    Args:
        tesis_adi: Kullanıcının girdiği tesis adı.

    Returns:
        list[DogrulamaHatasi]: Hata listesi. Boşsa geçerli demektir.
    """
    hatalar = []

    temiz_ad = tesis_adi.strip()
    if not temiz_ad:
        hatalar.append(DogrulamaHatasi(
            alan="tesis_adi",
            mesaj="Tesis adı boş bırakılamaz."
        ))
    elif len(temiz_ad) > TESIS_ADI_MAX_UZUNLUK:
        hatalar.append(DogrulamaHatasi(
            alan="tesis_adi",
            mesaj=f"Tesis adı en fazla {TESIS_ADI_MAX_UZUNLUK} karakter olabilir."
        ))

    return hatalar


def elektrik_tuketimi_dogrula(tuketim: float) -> list[DogrulamaHatasi]:
    """
    Aylık elektrik tüketimi değerini doğrular.

    Args:
        tuketim: Kullanıcının girdiği kWh değeri.

    Returns:
        list[DogrulamaHatasi]: Hata listesi. Boşsa geçerli demektir.
    """
    hatalar = []

    if tuketim < ELEKTRIK_MIN:
        hatalar.append(DogrulamaHatasi(
            alan="elektrik_tuketimi",
            mesaj=f"Elektrik tüketimi en az {ELEKTRIK_MIN:,} kWh olmalıdır."
        ))
    elif tuketim > ELEKTRIK_MAX:
        hatalar.append(DogrulamaHatasi(
            alan="elektrik_tuketimi",
            mesaj=f"Elektrik tüketimi en fazla {ELEKTRIK_MAX:,} kWh olabilir."
        ))

    return hatalar


def uretim_hatti_dogrula(hat_sayisi: int) -> list[DogrulamaHatasi]:
    """
    Üretim hattı sayısını doğrular.

    Args:
        hat_sayisi: Kullanıcının girdiği hat sayısı.

    Returns:
        list[DogrulamaHatasi]: Hata listesi. Boşsa geçerli demektir.
    """
    hatalar = []

    if hat_sayisi < URETIM_HATTI_MIN:
        hatalar.append(DogrulamaHatasi(
            alan="uretim_hatti",
            mesaj=f"Üretim hattı sayısı en az {URETIM_HATTI_MIN} olmalıdır."
        ))
    elif hat_sayisi > URETIM_HATTI_MAX:
        hatalar.append(DogrulamaHatasi(
            alan="uretim_hatti",
            mesaj=f"Üretim hattı sayısı en fazla {URETIM_HATTI_MAX} olabilir."
        ))

    return hatalar


def tum_alanlari_dogrula(
    tesis_adi: str,
    elektrik_tuketimi: float,
    uretim_hatti: int,
    otomasyon_seviyesi: int,
) -> list[DogrulamaHatasi]:
    """
    Formdaki tüm alanları tek seferde doğrular.

    Args:
        tesis_adi: Tesis adı metni.
        elektrik_tuketimi: Aylık elektrik tüketimi (kWh).
        uretim_hatti: Üretim hattı sayısı.
        otomasyon_seviyesi: 0-10 arası otomasyon seviyesi.

    Returns:
        list[DogrulamaHatasi]: Tüm hataların birleşik listesi.
    """
    hatalar = []

    hatalar.extend(tesis_adi_dogrula(tesis_adi))
    hatalar.extend(elektrik_tuketimi_dogrula(elektrik_tuketimi))
    hatalar.extend(uretim_hatti_dogrula(uretim_hatti))

    # Otomasyon seviyesi slider ile kontrol edildiği için
    # normalde aralık dışına çıkmaması gerekir, ama yine de kontrol edelim
    if not (OTOMASYON_MIN <= otomasyon_seviyesi <= OTOMASYON_MAX):
        hatalar.append(DogrulamaHatasi(
            alan="otomasyon_seviyesi",
            mesaj=f"Otomasyon seviyesi {OTOMASYON_MIN}-{OTOMASYON_MAX} arasında olmalıdır."
        ))

    return hatalar
