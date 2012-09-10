#! /bin/sh
cd rpmbuild/SOURCES
wget http://archive.apache.org/dist/lucene/solr/3.5.0/apache-solr-3.5.0.tgz
cd ../SPECS
ln -s ../../rpms/solr/solr.spec
rpmbuild -ba solr.spec
