#! /bin/sh
arch=$(AUTOV=1 rpm -q --qf '%{arch}\n' --specfile rpms/kata-ckan-dev/kata-ckan-dev.spec | head -n 1)
cd rpmbuild/RPMS/
mkdir allrpms
ln -s ${arch}/solr-[0-9]*.rpm allrpms/
ln -s ${arch}/kata-ckan-prod-[0-9]*.rpm allprpms/
ln -s noarch/mcfg-[0-9]*.rpm allrpms/
tar chf rpms.tar allrpms

