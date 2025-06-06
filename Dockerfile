# ┌───────────────────────────────────────────────────────────────────────┐
# │ Dockerfile para Django + OpenCV + Tesseract (OCR)                    │
# └───────────────────────────────────────────────────────────────────────┘

# 1) Partimos de Python 3.11-slim
FROM python:3.11-slim

# 2) Establecemos el directorio de trabajo
WORKDIR /app

# 3) Copiamos únicamente requirements.txt al contenedor (capa de caché)
COPY requirements.txt /app/requirements.txt

# 4) Instalamos dependencias de sistema:
#    - build-essential, libpq-dev, gcc: para psycopg2 y compilación de paquetes.
#    - libgl1, libglib2.0-0: para que OpenCV cargue libGL.so.1.
#    - tesseract-ocr: el motor nativo de OCR que pytesseract usará.
RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        gcc \
        libgl1 \
        libglib2.0-0 \
        tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# 5) Instalamos las dependencias de Python (incluye pytesseract, cv2, pandas, etc.)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# 6) Copiamos TODO el código de la carpeta actual en /app
COPY . /app/

# 7) Variables de entorno para Python:
#    - Impide crear archivos .pyc
#    - Evita buffering de salida para ver los logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 8) Creamos carpetas para media y static
RUN mkdir -p /app/media /app/static

# 9) Exponemos el puerto 8000
EXPOSE 8000

# 10) Comando por defecto: llaves, migraciones y runserver
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
