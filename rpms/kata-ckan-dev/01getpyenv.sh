#! /bin/sh
set -x
cd
pwd
mkdir download
cd download
wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
cd
python download/virtualenv.py pyenv

