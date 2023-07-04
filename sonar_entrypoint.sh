#!/bin/sh

python manage.py collectstatic --noinput

# gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 300 --log-level debug

gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon

python manage.py makemigrations 
python manage.py migrate