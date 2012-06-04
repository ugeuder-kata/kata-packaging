#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP01 ]
then
  echo "Skipping 01"
  exit 0
fi
instloc=$1
cd $instloc
mkdir -p ${instloc}/download
cd ${instloc}/download
wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
cd ..
python download/virtualenv.py pyenv
