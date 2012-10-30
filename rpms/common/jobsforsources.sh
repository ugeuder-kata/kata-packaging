#!/bin/bash
. /home/ckan/pyenv/bin/activate
sources=`/home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester sources|grep "Source id:"|cut -c 12-`
for source in sources;
do
    /home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester job $source > /dev/null 2>&1;
done
/home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester run --config=/home/ckan/pyenv/src/ckan/development.ini > /dev/null 2>&1