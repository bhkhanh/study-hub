#!/bin/bash

set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting web server with Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
