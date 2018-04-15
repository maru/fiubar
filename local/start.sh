#!/bin/bash

python manage.py makemigrations && \
python manage.py migrate && \
python manage.py loaddata fiubar.json || exit 1

echo
echo "Crear un usuario administrador"
python manage.py createsuperuser

python manage.py runserver 0.0.0.0:8000 --settings fiubar.config.settings.local
