#!/usr/bin/env bash
# exit on error
set -o errexit

python --version
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Optionally ensure an admin user exists when all values are provided.
# Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD in Render.
python manage.py shell -c "from django.contrib.auth import get_user_model; import os; username=os.getenv('DJANGO_SUPERUSER_USERNAME'); email=os.getenv('DJANGO_SUPERUSER_EMAIL'); password=os.getenv('DJANGO_SUPERUSER_PASSWORD'); User=get_user_model(); \
import sys; \
sys.exit(0) if not (username and email and password) else None; \
user, _ = User.objects.get_or_create(username=username, defaults={'email': email}); \
user.email=email; user.is_staff=True; user.is_superuser=True; user.set_password(password); user.save()"

