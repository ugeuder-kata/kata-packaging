#!/bin/bash
. /home/ckan/pyenv/bin/activate
sources=`/home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester sources --config=/home/ckan/pyenv/src/ckan/development.ini |grep "Source id:"|cut -c 12-`
for source in $sources;
do
    /home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester job $source --config=/home/ckan/pyenv/src/ckan/development.ini;
done
/home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester run --config=/home/ckan/pyenv/src/ckan/development.ini