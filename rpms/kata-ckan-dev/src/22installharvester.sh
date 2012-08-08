#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
pip install -e git+https://github.com/okfn/ckanext-harvest.git#egg=ckanext-harvest
pip install carrot
paster --plugin=ckanext-harvest harvester initdb --config=$instloc/pyenv/src/ckan/development.ini
paster --plugin=ckan user add harvester password=harvester --config=$instloc/pyenv/src/ckan/development.ini
paster --plugin=ckan sysadmin add harvester --config=$instloc/pyenv/src/ckan/development.ini