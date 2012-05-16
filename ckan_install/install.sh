#!/bin/bash
# Please make sure that git, subversion, libxml2-devel, libxslt-devel, postgresql-devel, gcc, mercurial, python-devel
# are installed
# Modify these variables according to installation directory
CKAN_DIR='/srv/ckan/ckan'
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
paster make-config ckan development.ini
deactivate
