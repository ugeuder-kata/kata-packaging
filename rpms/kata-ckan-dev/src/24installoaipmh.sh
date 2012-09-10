#!/bin/sh
set -x
instloc=$1

cd $instloc
cd pyenv/src
source ../bin/activate
pip install -e git+https://github.com/kata-csc/ckanext-oaipmh.git#egg=ckanext-oaipmh
