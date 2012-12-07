#!/bin/sh
set -x
if [ -f /tmp/kata-SKIP22 ]
then
  echo "Skipping 22"
  exit 0
fi
instloc=$1
cp /opt/solr/conf/schema.xml /opt/solr/conf/schema.xml.bak
cp $instloc/pyenv/src/ckan/ckan/config/solr/schema-2.0.xml /opt/solr/conf/schema.xml
service tomcat6 restart
chkconfig tomcat6 on
