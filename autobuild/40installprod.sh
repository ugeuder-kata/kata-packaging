#! /bin/sh
tar xf rpms-*.tar
cd allrpms
sudo yum install -y mcfg-*.rpm
if [ -r ~abuild/abuild-input/abuild-prod-kata-master.ini ]
then
  sudo cp ~abuild/abuild-input/abuild-prod-kata-master.ini /root/kata-master.ini
else
  sudo cp /usr/share/mcfg/examples/kata-master.ini /root
fi
sudo cp ~/abuild-input/abuild-prod-sp-cert.pem /root/sp-cert.pem
sudo cp ~/abuild-input/abuild-prod-sp-key.pem /root/sp-key.pem 
sudo yum install -y apache-solr-*.rpm
script -c 'sudo yum install -y 'kata-ckan-prod-*.rpm
