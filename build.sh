#!/usr/bin/env bash
set -o errexit
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
celery -A prostocks worker --loglevel=info &
celery -A prostocks beat --loglevel=info &
