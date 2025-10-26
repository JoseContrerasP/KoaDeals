echo "RUNNING SERVER"

echo "WAITING FOR MYSQL"

until mysqladmin ping -h db -u root -p$MYSQL_ROOT_PASSWORD --silent --skip-ssl; do
    sleep 2
done

echo "MIGRATING"

# python pylink/manage.py makemigrations
# python pylink/manage.py migrate

# python pylink/manage.py runserver 0:8000

python manage.py collectstatic --no-input

# cd KoaDeals

gunicorn KoaDeals.wsgi:application --bind 0:8000