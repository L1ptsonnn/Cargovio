#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python 3.12.3
pyenv install 3.12.3
pyenv global 3.12.3

pip install -r requirements.txt

python Cargovio/manage.py collectstatic --no-input
python Cargovio/manage.py migrate 