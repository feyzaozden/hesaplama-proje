# Temel Python imajı
FROM python:3.11-slim AS base

# Ortak bağımlılıklar
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libexpat1-7 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-6 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxrender1 \
    libxkbcommon0 \
    libxshmfence1 \
    libpango-1.0-0 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Chrome yükleme (platforma göre)
ARG TARGETARCH
RUN if [ "$TARGETARCH" = "amd64" ]; then \
        wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
        apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb && \
        rm google-chrome-stable_current_amd64.deb; \
    elif [ "$TARGETARCH" = "arm64" ]; then \
        wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_arm64.deb && \
        apt-get update && apt-get install -y ./google-chrome-stable_current_arm64.deb && \
        rm google-chrome-stable_current_arm64.deb; \
    fi


# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg ca-certificates fonts-liberation \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libexpat1 \
    libgbm1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libx11-6 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libxrender1 \
    libxkbcommon0 libxshmfence1 libpango-1.0-0 libxss1 libxtst6 xdg-utils \
    fonts-liberation libappindicator3-1 \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome kurulumu
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# ChromeDriver kurulumu
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f1) && \
    wget -q https://chromedriver.storage.googleapis.com/$CHROME_VERSION.0/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && mv chromedriver /usr/local/bin/ && rm chromedriver_linux64.zip && chmod +x /usr/local/bin/chromedriver

# Çalışma dizini
WORKDIR /app

# Proje dosyalarını kopyala
COPY . /app

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Konteyner çalıştırıldığında otomatik olarak bu dosya çalışsın
CMD ["python", "scheduler_app.py"]
