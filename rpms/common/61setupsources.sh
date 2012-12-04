#!/bin/sh
set -x
if [ -f /tmp/kata-SKIP61 ]
then
  echo "Skipping 61"
  exit 0
fi
instloc=$1
service rabbitmq-server start
chkconfig rabbitmq-server on
if [ \! -e /tmp/kata-SKIP-dbinit ]
then
  $instloc/pyenv/bin/paster --plugin=ckanext-harvest harvester source http://www.fsd.uta.fi/fi/aineistot/luettelo/fsd-ddi-records-uris-fi.txt DDI --config=/home/ckan/pyenv/src/ckan/development.ini
  $instloc/pyenv/bin/paster --plugin=ckanext-harvest harvester source http://helda.helsinki.fi/oai/request OAI-PMH --config=/home/ckan/pyenv/src/ckan/development.ini
fi
chkconfig supervisord on
# according to an earlier comment supervisor cannot be started before
# apache is (re)started. Because apache is nowadays started at the end
# of the installation, also starting supvisord happens there
