#!/bin/sh

python manage.py makemigrations

# Apply database migrations
python manage.py migrate  --run-syncdb
python manage.py migrate --run-syncdb

# Create a superuser (modify as needed)
python -c "import django;django.setup();from users.models import User;User.objects.create_superuser('rms@rms.com', 'rms')"

