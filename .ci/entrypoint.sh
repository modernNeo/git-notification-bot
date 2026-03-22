#!/bin/sh

# Wait for DB to be ready if needed, then migrate
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start the actual application
exec "$@"