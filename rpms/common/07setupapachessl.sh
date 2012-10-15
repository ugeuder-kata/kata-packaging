#!/bin/sh
set -x
packagedir=$1

#cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak 
#pushd /etc/httpd/conf/ >/dev/null
#patch -b -p2 -i "${packagedir}/setup-patches/httpd.conf"

cp /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/ssl.conf.bak
pushd /etc/httpd/conf.d/ >/dev/null
patch -b -p2 -i "${packagedir}/setup-patches/ssl.conf"
popd >/dev/null

/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 7

