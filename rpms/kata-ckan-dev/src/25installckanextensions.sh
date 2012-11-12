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

pip install -e git+https://github.com/kata-csc/ckanext-urn.git#egg=ckanext-urn

pip install -e git+https://github.com/kata-csc/ckanext-oaipmh.git#egg=ckanext-oaipmh

pip install -e git+https://github.com/kata-csc/ckanext-ddi.git#egg=ckanext-ddi

pip install -e git+https://github.com/kata-csc/ckanext-sitemap.git#egg=ckanext-sitemap

pip install -e git+git://github.com/kata-csc/ckanext-shibboleth.git#egg=ckanext-shibboleth
pushd ${instloc}/pyenv/src/ckan >/dev/null
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/who.ini.patch
popd >/dev/null

pip install -e git+git://github.com/kata-csc/ckanext-kata.git#egg=ckanext-kata


