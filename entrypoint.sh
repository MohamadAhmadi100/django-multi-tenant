#!/bin/sh

python manage.py collectstatic --noinput
#ask what to do
#python manage.py migrate

#gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 300 --log-level debug
#python manage.py runserver 0.0.0.0:8000

nginx -g "daemon off;"