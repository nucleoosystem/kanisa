# Note that this is not atomic - the site is broken for the duration
# of this script. Probably just want to take each site into
# maintenance mode for the duration, since upgrades should only take
# 30 seconds or so. This is very much a work in progress.
source ~/.virtualenvs/production/bin/activate
pip uninstall kanisa -y

wheel=`ls kanisa*.whl`
pip install $wheel
rm $wheel

# In future the folders will be in a config file somewhere, and we'll
# cd to every folder in the config file, and update every site.
cd /var/www/centralbaptistchelmsford.org

# Actually do the upgrade
python manage.py syncdb
python manage.py collectstatic --noinput
touch proj/wsgi.py

deactivate