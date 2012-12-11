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
myipcmd=$(dirname $0)/myip.sh
myip=$($myipcmd)
# TODO: needs to be really configurable
# ckanusermail kept from dev env
sed -e "s,\(ckan.site_url = http://\)[^ ]*,\1${myip}," development.ini > development.ini.1
mv development.ini.1 development.ini
if [ \! -e /tmp/kata-SKIP-dbinit ]
then
  paster --plugin=ckan db init
fi
