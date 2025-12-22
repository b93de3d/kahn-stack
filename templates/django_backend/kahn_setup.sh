#!/bin/bash
set -e

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

sudo cp example_config.json /etc/_KAHN_PROJECT_SLUG_.json

python manage.py makemigrations
python manage.py migrate

MIGRATE_PROD=true python manage.py makemigrations
MIGRATE_PROD=true python manage.py migrate
