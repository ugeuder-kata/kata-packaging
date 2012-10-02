#!/bin/sh
set -x
instloc=$1
ckanuser=$2

cd $instloc
cd pyenv/src
source ../bin/activate
pip install -e git+git://github.com/kata-csc/ckanext-kata.git#egg=ckanext-kata

