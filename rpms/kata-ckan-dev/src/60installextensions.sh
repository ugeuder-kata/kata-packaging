#!/bin/sh
set -x
instloc=$1
extensions="harvest oaipmh_harvester synchronous_search oaipmh ddi_harvester"
sed -i "/^ckan.plugins/s|$| $extensions|" $instloc/pyenv/src/ckan/development.ini
# make it so
service ckan-dev restart