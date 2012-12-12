#! /bin/sh
# this script is run as root (previous NNsetupckan.sh as %ckanuser)
set -x
if [ -f /tmp/kata-SKIP31 ]
then
  echo "Skipping 31"
  exit 0
fi
ckauser=$1
mkdir -p /opt/data/ckan
pushd /opt/data/ckan >/dev/null
mkdir data sstore data_tree
chown ${ckauser}:${ckanuser} data sstore data_tree
# Apache setup script will later change this again, but let's simulate the
# previous behavior when these directories where still in the pyenv code
# tree and created by ckanuser
