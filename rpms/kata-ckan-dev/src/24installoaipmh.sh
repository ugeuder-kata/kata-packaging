#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
git clone https://github.com/locusf/ckanext-oaipmh.git
cd ckanext-oaipmh
python setup.py install