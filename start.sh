#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn photography_config.wsgi:application --bind 0.0.0.0:$PORT