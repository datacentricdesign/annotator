#!/bin/sh

# python manage.py migrate --no-input
# python manage.py collectstatic --no-input

# gunicorn annotator.wsgi:application --bind 0.0.0.0:80

python manage.py runserver