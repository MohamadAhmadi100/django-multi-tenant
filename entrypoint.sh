#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

#gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 3
#nginx -g "daemon off;"

#MJ for test
exec "$@"