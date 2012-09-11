#!/bin/sh
set -x
instloc=$1
service rabbitmq-server start
chkconfig rabbitmq-server on
$instloc/pyenv/bin/paster --plugin=ckanext-harvest harvester source http://www.fsd.uta.fi/fi/aineistot/luettelo/fsd-ddi-records-uris-fi.txt Metadata --config=/home/ckan/pyenv/src/ckan/development.ini
$instloc/pyenv/bin/paster --plugin=ckanext-harvest harvester source http://helda.helsinki.fi/oai/request Metadata --config=/home/ckan/pyenv/src/ckan/development.ini
# Harvesting will only work after this
service httpd restart
chkconfig supervisord on
service supervisord restart