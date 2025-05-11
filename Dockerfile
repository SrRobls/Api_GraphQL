# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Variables de entorno para evitar archivos .pyc y mejorar logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia todo el proyecto a /app
COPY . /app

# Instala dependencias de Python
RUN pip install --upgrade pip && pip install -r core/requirements.txt

# Da permisos de ejecución al script de entrada
RUN chmod +x /app/entrypoint.sh

# Expone el puerto (opcional)
EXPOSE 8000

# Comando para arrancar el servidor
CMD ["/app/entrypoint.sh"]
