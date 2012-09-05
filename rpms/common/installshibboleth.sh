#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
pip install -e git+git://github.com/harripal/ckanext-shibboleth.git#egg=ckanext-shibboleth
