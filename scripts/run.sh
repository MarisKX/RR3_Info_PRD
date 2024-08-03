#!/bin/sh
set -e

# Use the PORT environment variable provided by Heroku
PORT=${PORT:-8000}

# Start Gunicorn with the appropriate settings
exec gunicorn -b 0.0.0.0:$PORT --chdir /django_backend/django_backend django_backend.wsgi:application \
    --workers 3 \
    --timeout 450