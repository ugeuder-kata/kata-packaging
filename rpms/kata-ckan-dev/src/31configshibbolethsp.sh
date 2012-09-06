#!/bin/sh
set -x
instloc=$1

cp /etc/shibboleth/shibboleth2.xml /etc/shibboleth/shibboleth2.xml.bak
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/shibboleth2.xml.patch
/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/master.ini 31
