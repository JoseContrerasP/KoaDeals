#!/usr/bin/env bash
# exit on error
set -o errexit

# poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

# if [[ $CREATE_SUPERUSER ]];
# then
# 	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser($SUPERUSER_USERNAME, $SUPERUSER_EMAIL, $SUPERUSER_PASSWORD)" | python manage.py shell
# fi