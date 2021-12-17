#!/bin/sh

echo "Migrating..."
python manage.py migrate --no-input
echo "Making static files..."
python manage.py collectstatic --no-input

echo "Starting Gunicorn..."
gunicorn annotator.wsgi:application --bind 0.0.0.0:8000