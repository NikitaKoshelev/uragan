#!/usr/bin/env bash

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata mydata.json
python manage.py createsuperuser
