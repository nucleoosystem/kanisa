source /home/deploy/.virtualenvs/production/bin/activate
cd /var/www/$1
python manage.py syncdb
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py rebuild_index --noinput
touch proj/wsgi.py
deactivate
