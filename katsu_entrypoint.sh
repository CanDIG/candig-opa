#!/bin/sh

# This line is necessary in order to give the database that is in another Docker container
# enough time to finish initializing
sleep 5

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000