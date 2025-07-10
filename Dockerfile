# 1. Python image asosida
FROM python:3.10

# 2. Ishchi katalog
WORKDIR /django_channels

# 3. Tizim uchun kerakli paketlar
RUN apt-get update && apt-get install -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Talablar faylini ko‘chirish va o‘rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Loyihani ichiga ko‘chirish
COPY . .

# 6. Django uchun `collectstatic`, `migrate`, va WebSocket serverni ishga tushirish
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
