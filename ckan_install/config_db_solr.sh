#!/bin/bash

source dirs
# Run this after setting up db and editing development.ini
source ${CKAN_DIR}/bin/activate
cd ${CKAN_DIR}/src/ckan/
paster --plugin=ckan db init

# Setup db, preferable to be run manually
# also edit /var/lib/pgsql/data/pg_hba.conf
# to replace ident with trust before these steps
#export PGPASSWORD="pass"
#sudo -u postgres createuser -S -D -R -P ckanuser
#sudo -u postgres createdb -O ckanuser ckantest
# Lets install solr 
mkdir -p ${SOLR_DIR}
cd ${SOLR_DIR}
$(curl "http://www.nic.funet.fi/pub/mirrors/apache.org/lucene/solr/3.6.0/apache-solr-3.6.0.tgz"|tar xzf -)
mv apache-solr-3.6.0/example .
mv apache-solr-3.6.0/dist/apache-solr-3.6.0.war example/solr/solr.war
