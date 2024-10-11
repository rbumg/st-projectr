#!/bin/sh

# Wait for the PostgreSQL database to be ready
./wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT --timeout=60 --strict -- echo "PostgreSQL is up"

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Load initial data
python manage.py seed

# Start the Django server
poetry run python manage.py runserver 0.0.0.0:8000
