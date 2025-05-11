# Usa una imagen oficial de Python
FROM python:3.11-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea el directorio de la app
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia TODO el proyecto (no solo core/)
COPY . /app

# Instala dependencias de Python
RUN pip install --upgrade pip && pip install -r /app/core/requirements.txt

# Expone el puerto
EXPOSE 8000

# Comando para iniciar
CMD python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT
