#!/bin/sh
/home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester run --config=/home/ckan/pyenv/src/ckan/development.ini > /dev/null 2>&1
/home/ckan/pyenv/bin/paster --plugin=ckanext-harvest harvester run --config=/home/ckan/pyenv/src/ckan/development.ini > /dev/null 2>&1