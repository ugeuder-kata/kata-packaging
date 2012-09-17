#! /bin/sh
arch=$(AUTOV=1 rpm -q --qf '%{arch}\n' --specfile rpms/kata-ckan-dev/kata-ckan-dev.spec | head -n 1)
cd rpmbuild/RPMS/
mkdir allrpms
cd allrpms
ln -s ../${arch}/apache-solr-[0-9]*.rpm
ln -s ../${arch}/kata-ckan-prod-[0-9]*.rpm
ln -s ../noarch/mcfg-[0-9]*.rpm
cd ..
tar chf rpms.tar allrpms

