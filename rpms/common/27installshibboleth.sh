#!/bin/sh
set -x
instloc=$1
ckanuser=$2

cd $instloc
cd pyenv/src
source ../bin/activate
pip install -e git+git://github.com/kata-csc/ckanext-shibboleth.git#egg=ckanext-shibboleth

# Patch who.ini
cp /home/ckan/pyenv/src/ckan/who.ini /home/ckan/pyenv/src/ckan/who.ini.bak
pushd /home/ckan/pyenv/src/ckan >/dev/null
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/who.ini.patch
popd >/dev/null

chown $ckanuser:apache $instloc -R
