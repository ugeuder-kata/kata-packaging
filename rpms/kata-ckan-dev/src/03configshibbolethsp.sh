#!/bin/sh
set -x
instloc=$1

cp /etc/shibboleth/shibboleth2.xml /etc/shibboleth/shibboleth2.xml.bak
pushd /etc/shibboleth >/dev/null
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/shibboleth2.xml.patch
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/attribute-map.xml.patch
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/attribute-policy.xml.patch
popd >/dev/null

cp /etc/httpd/conf.d/shib.conf /etc/httpd/conf.d/shib.conf.bak
pushd /etc/httpd/conf.d >/dev/null
patch -b -p2 -i /usr/share/kata-ckan-dev/setup-patches/shib.conf.patch
popd >/dev/null

/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/master.ini 3
