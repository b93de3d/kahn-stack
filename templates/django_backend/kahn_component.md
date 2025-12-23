```
# kahn_component_title
Django Backend
```

```
# kahn_component_slug
_KAHN_SHORT_NAME__core
```

```sh
# kahn_setup
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

sudo cp example_config.json /etc/_KAHN_PROJECT_SLUG_.json

python manage.py makemigrations
python manage.py migrate

MIGRATE_PROD=true python manage.py makemigrations
MIGRATE_PROD=true python manage.py migrate
```

```sh
# kahn_run_dev
python manage.py runserver
```

```yaml
# kahn_docker_snippet
name: YES
docker:
  bro: false
```
