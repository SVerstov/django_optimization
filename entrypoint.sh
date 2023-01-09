#!/bin/sh


python manage.py migrate --no-input
#python manage.py collectstatic --no-input

#python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --noinput

#python manage.py runserver 0.0.0.0:8000

