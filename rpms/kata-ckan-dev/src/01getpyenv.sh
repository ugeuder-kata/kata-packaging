#! /bin/sh
set -x
instloc=$1
cd $instloc
mkdir -p ${instloc}/download
cd ${instloc}/download
wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
cd ..
python download/virtualenv.py pyenv

