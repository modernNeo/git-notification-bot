#!/bin/sh

# Wait for DB to be ready if needed, then migrate
python manage.py migrate --noinput

# python manage.py collectstatic --noinput not needed yet

# Start the actual application
exec "$@"