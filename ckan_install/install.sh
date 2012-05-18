#!/bin/bash
source dirs
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
read -d '' TOMCAT_TEMPLATE <<"EOF"
<?xml version="1.0" encoding="utf-8"?>
<Context docBase="SOLR/example/solr/solr.war" debug="0" crossContext="true">
  <Environment name="solr/home" type="java.lang.String" value="SOLR/example/solr" override="true"/>
</Context>
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
wsgi_out="${WSGI_TEMPLATE//CKAN/$CKAN_DIR}"
solr_out="${TOMCAT_TEMPLATE//SOLR/$SOLR_DIR}"

# Install CKAN
ckan_short=${CKAN_DIR%/*}
mkdir -p $ckan_short
virtualenv --no-site-packages ${CKAN_DIR}
source ${CKAN_DIR}/bin/activate
pip install --ignore-installed -e git+https://github.com/okfn/ckan.git#egg=ckan
cd ${CKAN_DIR}/src/ckan
pip install --ignore-installed -r requires/lucid_missing.txt -r requires/lucid_conflict.txt
pip install webob==1.0.8
pip install pylons==0.9.7
pip install Babel
pip install lxml
pip install psycopg
pip install repoze.who
pip install repoze.who-friendlyform
pip install repoze.who.plugins.openid
paster make-config ckan development.ini
cd
echo "${apache_out}" > ckan.conf
echo "${wsgi_out}" > ${CKAN_DIR}/bin/ckan.py
echo "${solr_out}" > solr.xml
