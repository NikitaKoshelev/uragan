#!/usr/bin/env bash

source ${VIRTUAL_ENV}/bin/activate
cd ${OPENSHIFT_REPO_DIR}wsgi/Uragan
python manage.py dumpdata --format=json --all --natural-foreign --natural-primary --output=mydata.json --indent=2