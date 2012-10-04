#! /bin/sh
cd rpmbuild/RPMS/noarch
sudo yum install -y mcfg-[0-9][0-9][0-9][0-9][0-9][0-9]-1.el6.noarch.rpm
cd
if [ -r abuild-input/abuild-dev-kata-master.ini ]
then
  sudo cp abuild-input/abuild-dev-kata-master.ini /root/kata-master.ini
else
  sudo cp /usr/share/mcfg/examples/kata-master.ini /root
fi

sudo cp abuild-input/abuild-dev-sp-cert.pem /root/sp-cert.pem
sudo cp abuild-input/abuild-dev-sp-key.pem /root/sp-key.pem 
