#!/bin/sh
set -x
if [ -f /tmp/kata-SKIP24 ]
then
  echo "Skipping 24"
  exit 0
fi
packagedir=$1

pushd /etc/httpd/conf.d/ >/dev/null
patch -b -p2 -i "${packagedir}/setup-patches/ssl.conf.patch"
/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 24
popd >/dev/null

