FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system and browser dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget gnupg unzip ca-certificates \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 \
    libcairo2 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libxss1 libxtst6 libu2f-udev libvulkan1 \
    chromium firefox-esr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Install Playwright browsers
RUN python -m playwright install chromium firefox

WORKDIR /app
CMD ["bash"]