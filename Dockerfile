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

# Copia los archivos de requerimientos
COPY core/requirements.txt /app/requirements.txt

# Instala dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código
COPY core /app

# Expone el puerto
EXPOSE 8000

# Comando para recolectar estáticos y correr el servidor
CMD python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8000