# Resmi selenium/python imajını temel al
# Bu imaj, içinde Python, Selenium ve Chrome/ChromeDriver ile birlikte gelir.
FROM selenium/standalone-chrome:latest

# Çalışma dizinini ayarla
WORKDIR /app

# Projenizin dosyalarını konteynere kopyala
COPY . .

# Python bağımlılıklarını yükle
# --no-cache-dir, imaj boyutunu küçültmeye yardımcı olur.
RUN pip install --no-cache-dir -r requirements.txt

# Konteyner çalıştırıldığında otomatik olarak bu dosya çalışsın
CMD ["python", "scheduler_app.py"]



# # Temel Python imajı
# FROM python:3.11-slim

# # Çalışma dizinini ayarla
# WORKDIR /app

# # Gerekli sistem paketleri ve Google Chrome için bağımlılıkları kur
# RUN apt-get update && apt-get install -y \
#     wget \
#     gnupg \
#     unzip \
#     ca-certificates \
#     fonts-liberation \
#     libasound2 \
#     libatk-bridge2.0-0 \
#     libcups2 \
#     libdbus-1-3 \
#     libexpat1 \
#     libgbm1 \
#     libglib2.0-0 \
#     libnspr4 \
#     libnss3 \
#     libxcomposite1 \
#     libxdamage1 \
#     libxext6 \
#     libxfixes3 \
#     libxrandr2 \
#     libxrender1 \
#     libxss1 \
#     libxtst6 \
#     xdg-utils \
#     --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# # Chrome tarayıcısını kur (en güvenilir yöntemlerden biri)
# RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
#     && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get update && apt-get install -y google-chrome-stable

# # ChromeDriver'ı indir ve PATH'e ekle
# # NOT: ChromeDriver versiyonunu, kurulu Chrome versiyonuyla uyumlu olarak ayarlayın.
# # Örnek olarak 127.0.6533.102 versiyonunu kullanacağız, kontrol ediniz.
# ENV CHROME_DRIVER_VERSION="127.0.6533.102"
# RUN wget -q --no-verbose -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_DRIVER_VERSION}/linux64/chromedriver-linux64.zip" \
#     && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
#     && rm /tmp/chromedriver.zip \
#     && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
#     && rm -rf /usr/local/bin/chromedriver-linux64 \
#     && chmod +x /usr/local/bin/chromedriver

# # Proje dosyalarını kopyala
# COPY . .

# # Python bağımlılıklarını yükle
# RUN pip install --no-cache-dir -r requirements.txt

# # Konteyner çalıştırıldığında otomatik olarak bu dosya çalışsın
# CMD ["python", "scheduler_app.py"]
