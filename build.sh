#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python Cargovio/manage.py collectstatic --no-input
python Cargovio/manage.py migrate 