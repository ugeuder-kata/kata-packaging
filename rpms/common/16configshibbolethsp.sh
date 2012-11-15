#!/bin/sh
set -x
if [ -f /tmp/kata-SKIP16 ]
then
  echo "Skipping 16"
  exit 0
fi
packagedir=$1

pushd /etc/shibboleth >/dev/null
patch -b -p2 -i "${packagedir}/setup-patches/shibboleth2.xml.patch"
patch -b -p2 -i "${packagedir}/setup-patches/attribute-map.xml.patch"
patch -b -p2 -i "${packagedir}/setup-patches/attribute-policy.xml.patch"
popd >/dev/null

cp /etc/httpd/conf.d/shib.conf /etc/httpd/conf.d/shib.conf.bak
pushd /etc/httpd/conf.d >/dev/null
patch -b -p2 -i "${packagedir}/setup-patches/shib.conf.patch"
popd >/dev/null

/usr/bin/python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 16

chown shibd:shibd /etc/shibboleth/spkey.pem
chmod og= /etc/shibboleth/spkey.pem
# even if Apache uses the same key these protections will not be a
# problem, because Apache reads the key while still being root

# rename the generated key & certificate to prevent human confusion,
# it has happened...
# (But don't delete them, we might use them to bootstrap a new SP
# instance, e.g. in autobuild, see autobuild/README)
mv  /etc/shibboleth/sp-key.pem /etc/shibboleth/sp-key.pem.notused
mv  /etc/shibboleth/sp-cert.pem /etc/shibboleth/sp-cert.pem.notused

# chkconfig shibd not required, obviously done by its own rpm

# shibd not started here, will be done at the end of the installation
