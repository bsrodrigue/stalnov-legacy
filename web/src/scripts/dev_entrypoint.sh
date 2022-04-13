#!/bin/sh

# Run django migrations
python manage.py migrate

# Run django server
python manage.py runserver 0.0.0.0:8000
