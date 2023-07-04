#!/bin/sh

python manage.py collectstatic --noinput

# gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 300 --log-level debug

# need get config command before migrate
# python manage.py makemigrations 
# python manage.py migrate


gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 3
nginx -g "daemon off;"

