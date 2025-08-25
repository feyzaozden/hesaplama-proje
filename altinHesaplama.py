import json
from zoneinfo import ZoneInfo
from datetime import datetime
from pathlib import Path
import argparse

ts = datetime.now(ZoneInfo("Europe/Istanbul")).isoformat(timespec="seconds")

def parse_num(s):
    if s is None:
        return 0.0
    if isinstance(s, str):
        s = s.strip()
        if s == "-" or s == "":
            return 0.0
        return float(s.replace(".", "").replace(",", "."))
    return float(s)


# --- Girdi: CLI argümanı veya etkileşimli ---
parser = argparse.ArgumentParser(description="Altın hesaplama")
parser.add_argument("--gram", type=parse_num, help="Elinizdeki gram miktarı (virgül veya nokta)")
parser.add_argument("--alinan", type=parse_num, help="Altını aldığınız birim fiyat (TL)")
args = parser.parse_args()

if args.gram is not None:
    gram = float(args.gram)
else:
    gram = parse_num(input("Elinizde kaç gram altın var?  "))

if args.alinan is not None:
    alis_fiyati_musteri = float(args.alinan)
else:
    alis_fiyati_musteri = parse_num(input("Altını kaç TL'den aldınız?  "))

# --- JSON oku (scraper çıktısı) ---
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
json_yol = OUTPUT_DIR / "altin_fiyatlari.json"

if not json_yol.exists():
    raise FileNotFoundError(
        f"{json_yol} bulunamadı. Önce `python harem.py` çalıştırıp fiyatları kaydedin."
    )

with open(json_yol, "r", encoding="utf-8") as f:
    fiyatlar = json.load(f)


def format_tl(value) -> str:
    """Float değeri Türk Lirası formatına çevirir (binlik ayraç . ve ondalık ,)."""
    if isinstance(value, str):
        # Eğer string gelirse önce temizleyip float'a çevir
        value = value.replace(".", "").replace(",", ".")
        value = float(value)
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# JSON'dan gelen 1 gram has altın fiyatları
alis_fiyati_gram = parse_num(fiyatlar["hasAltin"]["alis"])
satis_fiyati_gram = parse_num(fiyatlar["hasAltin"]["satis"])

# Hesaplamalar :
# Güncel satış değeri (sen kuyumcuya satıyorsun, kuyumcu alis fiyatından alır)
toplam_satis_fiyati = float((gram) * alis_fiyati_gram)

# Senin ödediğin toplam maliyet (müşteri girişi)
toplam_alis_fiyati = float(gram * satis_fiyati_gram)

# Kar / zarar
iscilik =  float(alis_fiyati_musteri - (toplam_satis_fiyati))


sonuc = {
    "kaynak": "haremaltin.com",
    "kayitzamani": ts,
    "gram": float(gram),
    "alis_fiyati_gram": float(alis_fiyati_gram),
    "satis_fiyati_gram": float(satis_fiyati_gram),
    "toplam_satis_fiyati": float(toplam_satis_fiyati),
    "toplam_alis_fiyati": float(toplam_alis_fiyati),
    "iscilik": float(iscilik),
    "musteri_aldigi_fiyat": float(alis_fiyati_musteri),
}


OUTPUT_DIR.mkdir(exist_ok=True)
sonuc_dosya = OUTPUT_DIR / "altinHesapSonucu.json"
with open(sonuc_dosya, "w", encoding="utf-8") as f:
    json.dump(sonuc, f, ensure_ascii=False, indent=4)

print(f"\nSonuçlar '{sonuc_dosya}' dosyasına kaydedildi.")
