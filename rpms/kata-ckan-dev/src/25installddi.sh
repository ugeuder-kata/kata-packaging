#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
pip install -e git+https://github.com/martinblech/xmltodict.git#egg=xmltodict
pip install -e git+https://github.com/locusf/ckanext-ddi.git#egg=ckanext-ddi