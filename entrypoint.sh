echo 'Applying migrations...'
python manage.py migrate

echo 'Running server...'
gunicorn Api.wsgi:application --bind 0.0.0.0:$PORT