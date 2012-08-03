# See http://blog.nexcess.net/2011/12/30/installing-apache-solr-on-centos/ for required tomcat6 and java jdk.
Summary: Solr binary package
Name: apache-solr
Version: 3.5.0
Release: 1%{?dist}
Group: Applications/File
License: Apache License 2.0
Source0: apache-solr-3.5.0.tgz
Requires: tomcat6
Requires: java-1.6.0-openjdk

%description
SOLR binary package, for version 3.5.0. Installs to a tomcat6 installation as war file and example data files.

%prep
%setup

%build
# No building, we are basically just installing the example directory + war for tomcats usage.

%install
install -d $RPM_BUILD_ROOT/opt/solr
install -d $RPM_BUILD_ROOT/usr/share/tomcat6/conf/Catalina/localhost
mv $RPM_BUILD_DIR/apache-solr-3.5.0/example/solr $RPM_BUILD_ROOT/opt
mv $RPM_BUILD_DIR/apache-solr-3.5.0/dist/apache-solr-3.5.0.war $RPM_BUILD_ROOT/opt/solr/solr.war
# A bit of a kludge ... works ok though
cat > $RPM_BUILD_ROOT/usr/share/tomcat6/conf/Catalina/localhost/solr.xml <<EOF
<?xml version="1.0" encoding="utf-8"?>
<Context docBase="/opt/solr/solr.war" debug="0" crossContext="true">
  <Environment name="solr/home" type="java.lang.String" value="/opt/solr/" override="true"/>
</Context>
EOF

%post
service tomcat6 restart
%files
%attr(-,tomcat,tomcat)/opt/solr
%attr(-,tomcat,tomcat)/usr/share/tomcat6/conf/Catalina/localhost/solr.xml