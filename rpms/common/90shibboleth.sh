#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
pip install -e git+git://github.com/harripal/ckanext-shibboleth.git#egg=ckanext-shibboleth

patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/who.ini.patch
#patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/shibboleth2.xml.patch
#patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/attribute-map.xml.patch
#patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/attribute-policy.xml.patch

service shibd restart
service httpd restart
