#! /bin/sh
set -x
if [ -f /tmp/kata-SKIP71 ]
then
  echo "Skipping 71"
  exit 0
fi
datadir=$1
mv /tmp/pip.freeze.current ${datadir}
chown root:root ${datadir}/pip.freeze.current
