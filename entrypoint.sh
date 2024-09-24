export DJANGO_SETTINGS_MODULE=Api.settings

echo 'Applying migrations...'
python manage.py migrate

echo 'Catching static files...'
python manage.py collectstatic --noinput

echo 'Running server...'
daphne -b 0.0.0.0 -p $PORT Api.asgi:application