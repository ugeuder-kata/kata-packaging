#!/bin/bash
# PLEASE RUN AS ROOT:
CKAN_DIR='/srv/ckan/ckan'
SOLR_DIR='/opt/solr'
read -d '' APACHE_TEMPLATE <<"EOF"
WSGIPythonPath CKAN/lib/python2.6/site-packages
WSGIPythonHome CKAN
<VirtualHost *:80>
ServerName ckan
ServerAlias ckan
WSGIScriptAlias / CKAN/bin/ckan.py
# pass authorization info on (needed for rest api)
WSGIPassAuthorization On
ErrorLog /var/log/httpd/ckan.error.log
CustomLog /var/log/httpd/ckan.custom.log combined
</VirtualHost>
EOF

read -d '' WSGI_TEMPLATE <<"EOF"
import os
import sys
sys.stdout = sys.stderr
#import site
#site.addsitedir('CKAN/lib/python2.6/site-packages')
instance_dir = 'CKAN'
config_file = 'CKAN/src/ckan/development.ini'
pyenv_bin_dir = os.path.join(instance_dir, 'bin')
activate_this = os.path.join(pyenv_bin_dir, 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
from paste.deploy import loadapp
config_filepath = os.path.join(instance_dir, config_file)
from paste.script.util.logging_config import fileConfig
fileConfig(config_filepath)
application = loadapp('config:%s' % config_filepath)
EOF
apache_out="${APACHE_TEMPLATE//CKAN/$CKAN_DIR}"
#echo $apache_out
wsgi_out="${WSGI_TEMPLATE//CKAN/$CKAN_DIR}"
#echo $wsgi_out
# Setup db, preferable to be run manually
# also edit /var/lib/pgsql/data/pg_hba.conf
# to replace ident with trust before these steps
#export PGPASSWORD="pass"
#sudo -u postgres createuser -S -D -R -P ckanuser
#sudo -u postgres createdb -O ckanuser ckantest
source ${CKAN_DIR}/bin/activate
cd ${CKAN_DIR}/src/ckan
paster --plugin=ckan db init
# Lets install solr 
#mkdir -p ${SOLR_DIR}
#cd ${SOLR_DIR}
#curl "http://www.nic.funet.fi/pub/mirrors/apache.org/lucene/solr/3.6.0/apache-solr-3.6.0.tgz"|tar xzf --
#mv apache-solr-3.6.0/example .

