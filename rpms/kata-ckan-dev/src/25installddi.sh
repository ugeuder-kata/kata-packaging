#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
pip install -e git+https://github.com/martinblech/xmltodict.git#egg=xmltodict
git clone https://github.com/locusf/ckanext-ddi.git
cd ckanext-ddi
python setup.py install