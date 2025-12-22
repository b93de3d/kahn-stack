#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate
python manage.py init_models

echo "Booting Django..."
gunicorn _KAHN_PROJECT_SLUG_.wsgi:application \
            --bind 0.0.0.0:8000 \
            --workers 4 \
            --timeout 180 \
            --access-logfile - \
            --error-logfile - \
            --log-level info
