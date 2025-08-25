from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json, os, shutil

# --- Chrome Options ---
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def get_altin_fiyatlari():
    """Harem Altın web sitesinden fiyatları çeker ve JSON olarak kaydeder."""

    driver = webdriver.Chrome(options=options)

    try:
        ts = datetime.now(ZoneInfo("Europe/Istanbul")).isoformat(timespec="seconds")
        driver.get("https://www.haremaltin.com/")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "tr__ALTIN"))
        )

        def satir_verisi_al(drv, satir_id):
            satir = drv.find_element(By.ID, satir_id)
            hucreler = satir.find_elements(By.TAG_NAME, "td")
            return {
                "isim": hucreler[0].text.split("\n")[0],
                "alis": hucreler[1].text,
                "satis": hucreler[2].text,
                "fark": hucreler[3].text,
            }

        hasAltin = satir_verisi_al(driver, "tr__ALTIN")
        ons = satir_verisi_al(driver, "tr__ONS")
        usdKg = satir_verisi_al(driver, "tr__USDKG")
        eurKg = satir_verisi_al(driver, "tr__EURKG")
        yirmiIkiAyar = satir_verisi_al(driver, "tr__AYAR22")
        gramAltin = satir_verisi_al(driver, "tr__KULCEALTIN")
        onDortAyar = satir_verisi_al(driver, "tr__AYAR14")

        data = {
            "kaynak": "haremaltin.com",
            "kayitZamani": ts,
            "hasAltin": hasAltin,
            "ons": ons,
            "usdKg": usdKg,
            "eurKg": eurKg,
            "yirmiIkiAyar": yirmiIkiAyar,
            "gramAltin": gramAltin,
            "onDortAyar": onDortAyar,
        }

        BASE_DIR = Path(__file__).resolve().parent
        OUTPUT_DIR = BASE_DIR / "output"
        OUTPUT_DIR.mkdir(exist_ok=True)
        json_dosya = OUTPUT_DIR / "altin_fiyatlari.json"

        with open(json_dosya, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"[{ts}] Altın fiyatları başarıyla kaydedildi: {json_dosya}")
    finally:
        driver.quit()

if __name__ == '__main__':
    # Bu bölüm, dosya doğrudan çalıştırıldığında fiyatları çeker
    get_altin_fiyatlari()