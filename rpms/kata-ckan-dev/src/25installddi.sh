#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
git clone https://github.com/locusf/ckanext-ddi.git
cd ckanext-ddi
python setup.py install