#! /bin/sh
set -x
datadir=$1
mv /tmp/pip.freeze.current ${datadir}
chown root:root ${datadir}/pip.freeze.current

