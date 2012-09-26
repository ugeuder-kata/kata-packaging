Summary: Development and packaging environment for Kata CKAN
Name: kata-ckan-dev
%define autov %(echo $AUTOV)
# we had some check here to abort if AUTOV is not set, but it did not
# work. See git history for details
Version: %autov
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: GPLv2+ (to be verified)
#Url: http://not.sure.yet
Source0: kata-ckan-dev-%{version}.tgz
Requires: gcc
Requires: git
Requires: patch
Requires: postgresql-devel
Requires: postgresql-server
Requires: python-devel
Requires: wget
Requires: libxslt-devel
Requires: rabbitmq-server
Requires: apache-solr
Requires: supervisor
Requires: mod_wsgi
Requires: shibboleth
Requires: mcfg
Conflicts: kata-ckan-prod
# Fedora documentation says one should use...
#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# but the old-style(?) default %{_topdir}/BUILDROOT/... seems to work nicely
# so we don't clutter yet another place in the directory tree

%define ckanuser ckan
%define scriptdir %{_datadir}/%{name}/setup-scripts
%define patchdir %{_datadir}/%{name}/setup-patches
%define katadatadir %{_datadir}/%{name}/setup-data

%description
Installs a CKAN environment using pip.
This package is for internal development use only. Not intended to be used
on production systems. After installing a development system build
a kata-ckan-prod.rpm package to capture the result of this installation.


%prep
%setup

%build
diff -u patches/orig/attribute-map.xml patches/kata/attribute-map.xml >attribute-map.xml.patch || true
diff -u patches/orig/attribute-policy.xml patches/kata/attribute-policy.xml >attribute-policy.xml.patch || true
diff -u patches/orig/development.ini patches/kata/development.ini >development.ini.patch || true
diff -u patches/orig/httpd.conf patches/kata/httpd.conf >httpd.conf.patch || true
diff -u patches/orig/pg_hba.conf patches/kata/pg_hba.conf >pg_hba.conf.patch || true
diff -u patches/orig/shib.conf patches/kata/shib.conf >shib.conf.patch || true
diff -u patches/orig/shibboleth2.xml patches/kata/shibboleth2.xml >shibboleth2.xml.patch || true
diff -u patches/orig/who.ini patches/kata/who.ini >who.ini.patch || true

%install
install -d $RPM_BUILD_ROOT/%{scriptdir}
install -d $RPM_BUILD_ROOT/%{patchdir}
install -d $RPM_BUILD_ROOT/%{katadatadir}
install -d $RPM_BUILD_ROOT/etc/cron.d
install -d $RPM_BUILD_ROOT/etc/httpd/conf.d

# setup scripts (keep them numerically ordered)
install 01getpyenv.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 02getpythonpackages.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 03configshibbolethsp.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 05setuppostgres.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 10setupckan.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 14openfirewall.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 20setupckanservice.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 22installharvester.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 23installurn.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 24installoaipmh.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 25installddi.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 26installsitemap.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 27installshibboleth.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 28installkataexts.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 30configsolr.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 60installextensions.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 61setupsources.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 70checkpythonpackages.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 71storepythonpackages.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 80backuphome.sh $RPM_BUILD_ROOT/%{scriptdir}/

# misc scripts (keep them alphabetically ordered by filename)
install myip.sh $RPM_BUILD_ROOT/%{scriptdir}/
install runharvester.sh $RPM_BUILD_ROOT/%{katadatadir}/

# patches (keep them alphabetically ordered by filename)
install attribute-map.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install attribute-policy.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install development.ini.patch $RPM_BUILD_ROOT/%{patchdir}/
install httpd.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install pg_hba.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install shib.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install shibboleth2.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install who.ini.patch $RPM_BUILD_ROOT/%{patchdir}/

# misc data/conf files (keep them alphabetically ordered by filename)
install harvester $RPM_BUILD_ROOT/etc/cron.d/
install harvester.conf $RPM_BUILD_ROOT/%{katadatadir}/
install kata.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/
install log/pip.freeze.lastknown $RPM_BUILD_ROOT/%{katadatadir}/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
# same order as above
%{scriptdir}/01getpyenv.sh
%{scriptdir}/02getpythonpackages.sh
%{scriptdir}/03configshibbolethsp.sh
%{scriptdir}/05setuppostgres.sh
%{scriptdir}/10setupckan.sh
%{scriptdir}/14openfirewall.sh
%{scriptdir}/20setupckanservice.sh
%{scriptdir}/22installharvester.sh
%{scriptdir}/23installurn.sh
%{scriptdir}/24installoaipmh.sh
%{scriptdir}/25installddi.sh
%{scriptdir}/26installsitemap.sh
%{scriptdir}/27installshibboleth.sh
%{scriptdir}/28installkataexts.sh
%{scriptdir}/30configsolr.sh
%{scriptdir}/60installextensions.sh
%{scriptdir}/61setupsources.sh
%{scriptdir}/70checkpythonpackages.sh
%{scriptdir}/71storepythonpackages.sh
%{scriptdir}/80backuphome.sh
%{scriptdir}/myip.sh

# sic! following script in datadir
%{katadatadir}/runharvester.sh
%{patchdir}/attribute-map.xml.patch
%{patchdir}/attribute-policy.xml.patch
%{patchdir}/development.ini.patch
%{patchdir}/httpd.conf.patch
%{patchdir}/pg_hba.conf.patch
%{patchdir}/shib.conf.patch
%{patchdir}/shibboleth2.xml.patch
%{patchdir}/who.ini.patch
%attr(0644,root,root)/etc/cron.d/harvester
%{katadatadir}/harvester.conf
/etc/httpd/conf.d/kata.conf
%{katadatadir}/pip.freeze.lastknown

%post
useradd %{ckanuser}  # needs to be removed if ckanuser were changed to httpd
su -c "%{scriptdir}/01getpyenv.sh /home/%{ckanuser}" %{ckanuser}
su -c "%{scriptdir}/02getpythonpackages.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/03configshibbolethsp.sh "/usr/share/kata-ckan-dev"
cat > /home/%{ckanuser}/pyenv/bin/wsgi.py <<EOF
import os
instance_dir = '/home/ckan'
config_file = '/home/ckan/pyenv/src/ckan/development.ini'
pyenv_bin_dir = os.path.join(instance_dir, 'pyenv', 'bin')
activate_this = os.path.join(pyenv_bin_dir, 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
from paste.deploy import loadapp
config_filepath = os.path.join(instance_dir, config_file)
from paste.script.util.logging_config import fileConfig
fileConfig(config_filepath)
application = loadapp('config:%s' % config_filepath)
EOF
chmod 777 /home/%{ckanuser}/pyenv/bin/wsgi.py
%{scriptdir}/05setuppostgres.sh %{patchdir}
su -c "%{scriptdir}/10setupckan.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/14openfirewall.sh
%{scriptdir}/20setupckanservice.sh %{patchdir}
su -c "%{scriptdir}/22installharvester.sh /home/%{ckanuser}" %{ckanuser}
su -c "%{scriptdir}/23installurn.sh /home/%{ckanuser}" %{ckanuser}
su -c "%{scriptdir}/24installoaipmh.sh /home/%{ckanuser}" %{ckanuser}
su -c "%{scriptdir}/25installddi.sh /home/%{ckanuser}" %{ckanuser}
su -c "%{scriptdir}/26installsitemap.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/27installshibboleth.sh /home/%{ckanuser} %{ckanuser}
su -c "%{scriptdir}/28installkataexts.sh /home/%{ckanuser}" %{ckanuser}
# Lets do this last so our harvesters are correctly picked up by the daemons.
cat /usr/share/kata-ckan-dev/setup-data/harvester.conf >> /etc/supervisord.conf
# Enable tmp directory for logging. Otherwise goes to /
sed -i 's/;directory/directory/' /etc/supervisord.conf
%{scriptdir}/30configsolr.sh /home/%{ckanuser}
su -c "%{scriptdir}/60installextensions.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/61setupsources.sh /home/%{ckanuser}
service atd restart
at -f %{katadatadir}/runharvester.sh 'now + 5 minute'

service shibd restart
service httpd restart

# run this last so the user has a chance to see the output
su -c "%{scriptdir}/70checkpythonpackages.sh /home/%{ckanuser} %{katadatadir}/pip.freeze.lastknown" %{ckanuser}
# well, actually it was last but one, but we still need to do this as root
# afterwards
%{scriptdir}/71storepythonpackages.sh %{katadatadir}

%preun
service ckan-dev stop
%{scriptdir}/80backuphome.sh /home/%{ckanuser}


%postun
echo "Uninstallation not fully supported yet, better get a clean VM to be sure"
echo "User account %{ckanuser} not deleted, firewall change not reverted,"
echo "postgresql configuration not reverted"

%changelog
* Mon May 21 2012 Uwe Geuder <uwe.geuder@nomvok.com>
- Initial version
