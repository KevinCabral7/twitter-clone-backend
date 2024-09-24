export DJANGO_SETTINGS_MODULE=Api.settings

echo 'Applying migrations...'
python manage.py migrate

echo 'Running server...'
daphne -b 0.0.0.0 -p $PORT Api.asgi:application