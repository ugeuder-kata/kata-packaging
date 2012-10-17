#!/bin/sh
set -x
packagedir=$1

cp /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/ssl.conf.bak
pushd /etc/httpd/conf.d/ >/dev/null
patch -b -p2 -i "${packagedir}/setup-patches/ssl.conf.patch"
/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 7
popd >/dev/null

