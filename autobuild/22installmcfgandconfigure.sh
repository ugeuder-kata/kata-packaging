#! /bin/sh
cd rpmbuild/RPMS/noarch
sudo yum install -y mcfg-[0-9][0-9][0-9][0-9][0-9][0-9]-1.el6.noarch.rpm
#TODO use host specific file from abuild-input
sudo cp /usr/share/mcfg/examples/kata-master.ini /root
cd
sudo cp abuild-input/abuild-dev-sp-cert.pem /root/sp-cert.pem
sudo cp abuild-input/abuild-dev-sp-cert.pem /root/sp-key.pem 
