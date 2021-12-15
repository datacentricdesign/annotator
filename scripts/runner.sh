#!/usr/bin/env sh

# Getting static files for Admin panel hosting!
./manage.py collectstatic --noinput
uwsgi --http "0.0.0.0:${PORT}" --module app.wsgi --master --processes 4 --threads 2