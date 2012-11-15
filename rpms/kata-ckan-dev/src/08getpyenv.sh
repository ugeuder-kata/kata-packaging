#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP08 ]
then
  echo "Skipping 08"
  exit 0
fi
instloc=$1
cd $instloc
mkdir -p ${instloc}/download
cd ${instloc}/download
curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
cd ..
# --no-site-packages option should be used according to updated installation
# instructions
# however, it causes a deprecation warning, would only be required on 
# older versions, so we drop it
#python download/virtualenv.py --no-site-packages pyenv
python download/virtualenv.py pyenv
