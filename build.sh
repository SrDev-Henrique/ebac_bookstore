#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Poetry and project dependencies (main group only)
pip install --upgrade pip
pip install poetry
poetry config virtualenvs.create false
poetry install --only main --no-root

python manage.py collectstatic --no-input
python manage.py migrate
