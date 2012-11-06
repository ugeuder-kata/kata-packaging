#! /bin/sh
cd rpmbuild/SOURCES
curl -O http://archive.apache.org/dist/lucene/solr/3.5.0/apache-solr-3.5.0.tgz
cd ../SPECS
ln -s ../../rpms/solr/solr.spec
rpmbuild -ba solr.spec
arch=$(rpm -q --qf '%{arch}\n' --specfile solr.spec | head -n 1)
cd ../RPMS/${arch}
sudo yum install -y apache-solr-3.5.0-1.el6.${arch}.rpm
