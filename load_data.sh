#!/usr/bin/env bash

source ${VIRTUAL_ENV}bin/activate
cd ${OPENSHIFT_REPO_DIR}wsgi/Uragan

python manage.py loaddata mydata.json