#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP10 ]
then
  echo "Skipping 10"
  exit 0
fi
instloc=$1
cd $instloc
source pyenv/bin/activate
cd pyenv/src/ckan
paster make-config ckan development.ini
patch -p2 -i /usr/share/kata-ckan-dev/setup-patches/development.ini.patch
