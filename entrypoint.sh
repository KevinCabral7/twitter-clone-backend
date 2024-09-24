echo 'Applying migrations...'
python manage.py migrate

echo 'Running server...'
uvicorn Api.asgi:application --bind 0.0.0.0:$PORT