from apscheduler.schedulers.background import BackgroundScheduler
from harem2 import get_altin_fiyatlari
import time
import sys
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)


# Projenizin temel dizinini ayarlayın
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Altın fiyatlarını çeken fonksiyonu ve hesaplama fonksiyonunu çağır
def run_all_tasks():
    print("-" * 30)
    print("Zamanlanmış görev başlatılıyor...")
    get_altin_fiyatlari()
    # Altın hesaplama dosyasını da burada çağırabiliriz.
    # Ancak altinHesaplama.py'nin kullanıcı girişi istediğini unutmayın.
    # Bu yüzden, bu dosyayı sadece CLI argümanları ile çalıştırabilirsiniz.
    # Örneğin: subprocess.run(["python", "altinHesaplama.py", "--gram", "10", "--alinan", "1200"])
    print("Zamanlanmış görev tamamlandı.")
    print("-" * 30)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # Her 1 dakikada bir 'run_all_tasks' fonksiyonunu çalıştır
    scheduler.add_job(run_all_tasks, 'interval', minutes=1)
    
    # Uygulama başlatıldığında hemen ilk görevi çalıştır
    scheduler.add_job(run_all_tasks, 'date', run_date=datetime.now())
    
    scheduler.start()
    
    print("Altın fiyatı güncelleme servisi başlatıldı.")
    
    try:
        # Bu döngü, uygulamanın arka planda çalışmasını sağlar
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Servis durduruldu.")
    
