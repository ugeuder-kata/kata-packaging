#!/bin/sh
set -x
if [ -f /tmp/kata-SKIP36 ]
then
  echo "Skipping 36"
  exit 0
fi
instloc=$1

cd $instloc/pyenv
source ./bin/activate
cd src/ckan
if [ -r /etc/kata-ckan-dev/versions ]
then
   source /etc/kata-ckan-dev/versions
else
   ext_harvest_version=""
   ext_urn_version=""
   ext_oaipmh_version=""
   ext_ddi_version=""
   ext_sitemap_version=""
   ext_shibboleth_version=""
   ext_kata_version=""
   # well missing assignments would have had the same effect as empty values
   # but let's have them here for clarity. Maybe we want to hard-code
   # some values here in a later project phase
fi

pip install -e git+https://github.com/okfn/ckanext-harvest.git${ext_harvest_version}#egg=ckanext-harvest
pip install carrot
paster --plugin=ckanext-harvest harvester initdb --config=development.ini
paster --plugin=ckan user add harvester password=harvester --config=development.ini
paster --plugin=ckan sysadmin add harvester --config=development.ini

pip install -e git+https://github.com/kata-csc/ckanext-urn.git${ext_urn_version}#egg=ckanext-urn

pip install -e git+https://github.com/kata-csc/ckanext-oaipmh.git${ext_oaipmh_version}#egg=ckanext-oaipmh

pip install -e git+https://github.com/kata-csc/ckanext-ddi.git${ext_ddi_version}#egg=ckanext-ddi

pip install -e git+https://github.com/kata-csc/ckanext-sitemap.git${ext_sitemap_version}#egg=ckanext-sitemap

pip install -e git+git://github.com/kata-csc/ckanext-shibboleth.git${ext_shibboleth_version}#egg=ckanext-shibboleth
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/who.ini.patch

pip install -e git+git://github.com/kata-csc/ckanext-kata.git${ext_kata_version}#egg=ckanext-kata

extensions="shibboleth harvest oaipmh_harvester synchronous_search oaipmh ddi_harvester sitemap kata kata_metadata"
cp development.ini development.ini.backup.preext
sed -i "/^ckan.plugins/s|$| $extensions|" development.ini
