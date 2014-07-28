source /home/deploy/.virtualenvs/production/bin/activate
cd /var/www/$1

# Copy a few essential files
cp /home/deploy/.virtualenvs/production/lib/python2.7/site-packages/kanisa/proj_template/proj/*.py proj/
cp /home/deploy/.virtualenvs/production/lib/python2.7/site-packages/kanisa/proj_template/manage.py .

# Ensure we've got a few directories we'll need
mkdir -p proj/static
mkdir -p proj/media
mkdir -p proj/whoosh_index

# Update the database
python manage.py syncdb
python manage.py migrate

# Grab static files
python manage.py collectstatic --noinput

# Rebuild the search index
python manage.py rebuild_index --noinput

# Restart the site
touch proj/wsgi.py

# Cleanup
deactivate
