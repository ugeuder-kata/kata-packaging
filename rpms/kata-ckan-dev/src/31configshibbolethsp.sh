#!/bin/sh
set -x
instloc=$1

echo "SHIBBOLEHT"
env
whoami
stat -L /proc/self/root
md5sum /root/master.ini
ls -l /root/

cp /etc/shibboleth/shibboleth2.xml /etc/shibboleth/shibboleth2.xml.bak

pushd /etc/shibboleth >/dev/null
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/shibboleth2.xml.patch
popd >/dev/null
/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/master.ini 31

echo "SHIBBOLEHT"
