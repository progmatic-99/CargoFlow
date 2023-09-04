#!/bin/sh

python manage.py makemigrations
# Apply database migrations
python manage.py migrate

# Create a superuser (modify as needed)
python -c "import django;django.setup();django.contrib.auth.models.User.objects.create_superuser('rms', 'rms@rms.com', 'rms')"
