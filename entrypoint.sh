#!/bin/bash

# Recolecta archivos estáticos sin interacción
python manage.py collectstatic --noinput

# Aplica migraciones de la base de datos
python manage.py migrate

# Ejecuta el servidor escuchando en el puerto dinámico de Cloud Run
exec python manage.py runserver 0.0.0.0:$PORT
