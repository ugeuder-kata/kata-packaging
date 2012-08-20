#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
pip install -e git+http://harripal.kapsi.fi/gits/ckanext-shibboleth.git#egg=ckanext-shibboleth
