export DJANGO_SETTINGS_MODULE=Api.settings

echo 'Applying migrations...'
python manage.py migrate

echo 'Running server...'
uvicorn Api.asgi:application --host 0.0.0.0 --port $PORT