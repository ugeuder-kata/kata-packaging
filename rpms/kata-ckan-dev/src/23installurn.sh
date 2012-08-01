#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
git clone https://github.com/locusf/ckanext-urn.git
cd ckanext-urn
python setup.py install