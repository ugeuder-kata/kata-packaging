#! /bin/sh
# configure our dependencies (packages which have been installed before)
set -x
patchdir=$1

service tomcat6 stop
cd /etc/tomcat6
patch -b -p2 -i "${patchdir}/tomcat6.conf.patch"
python /usr/share/mcfg/tool/mcfg.py run /usr/share/mcfg/config/kata-template.ini /root/kata-master.ini 1
service tomcat6 start
