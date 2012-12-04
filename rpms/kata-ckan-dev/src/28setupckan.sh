#! /bin/sh
# remember: we are not root here (%ckanuser from the spec file)
set -x
if [ -f /tmp/kata-SKIP28 ]
then
  echo "Skipping 28"
  exit 0
fi
instloc=$1
cd $instloc
source pyenv/bin/activate
cd pyenv/src/ckan
paster make-config ckan development.ini
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/development.ini.patch
myip=$(ip addr show dev eth0 | grep "inet " | sed -E "s/ +inet +([^/]+).+/\1/")
# TODO: needs to be really configurable
ckanusermail=root@localhost
sed -e "s/%%myip%%/${myip}/" -e "s/%%ckanusermail%%/${ckanusermail}/" development.ini > development.ini.1
mv development.ini.1 development.ini
if [ \! -e /tmp/kata-SKIP-dbinit ]
then
  paster --plugin=ckan db init
fi
mkdir data sstore data_tree
