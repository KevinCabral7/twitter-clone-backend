echo 'Running collecstatic...'
python manage.py collectstatic --no-input

echo 'Applying migrations...'
python manage.py migrate

echo 'Running server...'
gunicorn bookstore.wsgi:application --bind 0.0.0.0:$PORT