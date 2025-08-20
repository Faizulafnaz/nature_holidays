#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
# Ensure superuser exists and has a usable password (configurable via env)
python manage.py shell -c "from django.contrib.auth import get_user_model; import os; User=get_user_model(); username='admin'; email='admin@example.com'; password='1234'; user, created = User.objects.get_or_create(username=username, defaults={'email': email}); user.is_staff=True; user.is_superuser=True; (created or (not user.has_usable_password())) and user.set_password(password); user.email=email; user.save()"
python manage.py populate_sample_data
