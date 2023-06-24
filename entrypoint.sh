#!/bin/sh

#if [ "$DATABASE" = "postgres" ]
#then
#    echo "Waiting for postgres..."
#
#    while ! nc -z $SQL_HOST $SQL_PORT; do
#      sleep 0.1
#    done
#
#    echo "PostgreSQL started"
#fi

python manage.py collectstatic --noinput
python manage.py migrate


#gunicorn main.wsgi:application --user www-data --bind 0.0.0.0:8010 --workers 3
#nginx -g "daemon off;"

# if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
#     (python manage.py createsuperuser --no-input)
# fi
(gunicorn main.wsgi:application --user www-data --bind 0.0.0.0:8000 --workers 3) &
nginx -g "daemon off;"