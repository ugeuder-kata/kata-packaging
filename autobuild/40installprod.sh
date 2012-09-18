#! /bin/sh
tar xf rpms-*.tar
cd allrpms
sudo yum install -y mcfg-*.rpm
echo "TODO: editing mcfg master.ini comes here"
sudo yum install -y apache-solr-*.rpm
sudo yum install -y kata-ckan-prod-*.rpm
