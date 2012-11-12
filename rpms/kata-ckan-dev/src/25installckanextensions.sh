#!/bin/sh
set -x
instloc=$1

cd $instloc
source ./bin/activate
cd pyenv/src/ckan

pip install -e git+https://github.com/okfn/ckanext-harvest.git#egg=ckanext-harvest
pip install carrot
paster --plugin=ckanext-harvest harvester initdb --config=development.ini
paster --plugin=ckan user add harvester password=harvester --config=development.ini
paster --plugin=ckan sysadmin add harvester --config=development.ini

pip install -e git+https://github.com/kata-csc/ckanext-urn.git#egg=ckanext-urn

pip install -e git+https://github.com/kata-csc/ckanext-oaipmh.git#egg=ckanext-oaipmh

pip install -e git+https://github.com/kata-csc/ckanext-ddi.git#egg=ckanext-ddi

pip install -e git+https://github.com/kata-csc/ckanext-sitemap.git#egg=ckanext-sitemap

pip install -e git+git://github.com/kata-csc/ckanext-shibboleth.git#egg=ckanext-shibboleth
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/who.ini.patch

pip install -e git+git://github.com/kata-csc/ckanext-kata.git#egg=ckanext-kata

extensions="shibboleth harvest oaipmh_harvester synchronous_search oaipmh ddi_harvester sitemap kata kata_metadata"
cp development.ini development.ini.backup.preext
sed -i "/^ckan.plugins/s|$| $extensions|" development.ini
