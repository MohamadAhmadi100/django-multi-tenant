#!/bin/sh

python manage.py collectstatic --noinput
#ask what to do
#python manage.py migrate

gunicorn main.wsgi:application --bind 0.0.0.0:8001 --workers 3 --timeout 300 --log-level debug
nginx -g "daemon off;"