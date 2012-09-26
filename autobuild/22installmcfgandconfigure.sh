#! /bin/sh
cd rpmbuild/RPMS/noarch
sudo yum install -y mcfg-[0-9][0-9][0-9][0-9][0-9][0-9]-1.el6.noarch.rpm
sudo cp /usr/share/mcfg/examples/kata-master.ini /root
