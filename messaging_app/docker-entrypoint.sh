#!/bin/sh
# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."

until python3 -c "import MySQLdb; MySQLdb.connect(host='db', user='${MYSQL_USER}', passwd='${MYSQL_PASSWORD}', db='${MYSQL_DB}')" 2>/dev/null; do
  echo "MySQL is unavailable - sleeping"
  sleep 2
done

echo "MySQL is up - executing migrations and starting server"
python manage.py migrate --noinput
python3 manage.py runserver 0.0.0.0:8000
