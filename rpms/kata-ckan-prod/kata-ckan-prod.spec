# TODO: following comment is partially obsolete/incorrect. See
# autobuild/README for further sudo info
#
# Note: spec file contains calls to sudo. Will not work if not run
# from a terminal or the user executing is not in sudoers appropriately
# This is of course a HACK, but it's caused by the fact the we work
# with a user specific pyenv instead of a system wide installation. 
#
Summary: Kata CKAN production
Name: kata-ckan-prod
%define autov %(echo $AUTOV)
# we had some check here to abort if AUTOV is not set, but it did not
# work. See git history of dev.spec for details
Version: %autov
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: GPLv2+ (to be verified)
#Url: http://not.sure.yet
Source: kata-ckan-prod-%{version}.tgz
Requires: postgresql
Requires: postgresql-server
Requires: patch
Requires: libxslt
Requires: rabbitmq-server
Requires: apache-solr
Requires: supervisor
Requires: mod_wsgi
Requires: shibboleth
Requires: mcfg
Requires: mod_ssl
Conflicts: kata-ckan-dev
BuildRequires: kata-ckan-dev
# Fedora documentation says one should use...
#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# but the old-style(?) default %{_topdir}/BUILDROOT/... seems to work nicely
# so we don't clutter yet another place in the directory tree

%define ckanuser ckan
%define scriptdir %{_datadir}/%{name}/setup-scripts
%define patchdir %{_datadir}/%{name}/setup-patches

%description
Installs a complete Kata CKAN environment
This package is for the production server.

%prep
%setup


%build
diff -u patches/orig/attribute-map.xml patches/kata/attribute-map.xml >attribute-map.xml.patch || true
diff -u patches/orig/attribute-policy.xml patches/kata/attribute-policy.xml >attribute-policy.xml.patch || true
diff -u patches/orig/httpd.conf patches/kata/httpd.conf >httpd.conf.patch || true
diff -u patches/orig/ssl.conf patches/kata/ssl.conf >ssl.conf.patch || true
diff -u patches/orig/pg_hba.conf patches/kata/pg_hba.conf >pg_hba.conf.patch || true
diff -u patches/orig/shib.conf patches/kata/shib.conf >shib.conf.patch || true
diff -u patches/orig/shibboleth2.xml patches/kata/shibboleth2.xml >shibboleth2.xml.patch || true
diff -u patches/orig/tomcat6.conf patches/kata/tomcat6.conf >tomcat6.conf.patch || true
diff -u patches/orig/who.ini patches/kata/who.ini >who.ini.patch || true

%install
# cpio: we need to be root to be able to read, but we don't preserve the 
# ownership because rpmbuild will in trouble later with such files. 
# %attr will take care of ownership eventually
# sudo is somewhat nasty here (interactive command) but building is
# only carried out by people who know what they are doing...
me=$(whoami)
# run a dummy sudo first. Two sudo commands in a pipe sometimes screw up
# the terminal when both prompting for the password
sudo true
sudo find /home/%{ckanuser}/pyenv -depth | sudo cpio -pdm --owner ${me}: $RPM_BUILD_ROOT/
# not sure why, but testings show that the following 2 directories are not
# owned by ${me}
sudo chown ${me} $RPM_BUILD_ROOT/home
sudo chown ${me} $RPM_BUILD_ROOT/home/%{ckanuser}
find $RPM_BUILD_ROOT/home/%{ckanuser} -name .git -print0 | xargs -0 rm -rf
find $RPM_BUILD_ROOT/home/%{ckanuser} -name .svn -print0 | xargs -0 rm -rf
install -d $RPM_BUILD_ROOT/%{scriptdir}
install -d $RPM_BUILD_ROOT/%{patchdir}
install -d $RPM_BUILD_ROOT/etc/cron.d
install -d $RPM_BUILD_ROOT/etc/httpd/conf.d
# setup scripts (keep them numerically ordered)
install 04configuredependencies.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 16configshibbolethsp.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 20setuppostgres.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 24setupapachessl.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 26setupckanprod.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 32setupckanservice.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 35setupharvester.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 40configsolr.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 61setupsources.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 80backuphome.sh $RPM_BUILD_ROOT/%{scriptdir}/
# misc scripts (keep them alphabetically ordered by filename)
install myip.sh $RPM_BUILD_ROOT/%{scriptdir}/
install runharvester.sh $RPM_BUILD_ROOT/%{scriptdir}/
# patches (keep them alphabetically ordered by filename)
install attribute-map.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install attribute-policy.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install httpd.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install pg_hba.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install shib.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install shibboleth2.xml.patch $RPM_BUILD_ROOT/%{patchdir}/
install ssl.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install tomcat6.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install who.ini.patch $RPM_BUILD_ROOT/%{patchdir}/

# misc data/conf files (keep them alphabetically ordered by filename)
install harvester-prod $RPM_BUILD_ROOT/etc/cron.d/
install harvester.conf $RPM_BUILD_ROOT/%{scriptdir}/
install kata.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%attr(-,%{ckanuser},%{ckanuser}) /home/%{ckanuser}/pyenv
%{scriptdir}/04configuredependencies.sh
%{scriptdir}/16configshibbolethsp.sh
%{scriptdir}/20setuppostgres.sh
%{scriptdir}/24setupapachessl.sh
%{scriptdir}/26setupckanprod.sh
%{scriptdir}/32setupckanservice.sh
%{scriptdir}/35setupharvester.sh
%{scriptdir}/40configsolr.sh
%{scriptdir}/61setupsources.sh
%{scriptdir}/80backuphome.sh
%{scriptdir}/myip.sh
%{scriptdir}/runharvester.sh
%{patchdir}/httpd.conf.patch
%{patchdir}/pg_hba.conf.patch
%attr(0644,root,root)/etc/cron.d/harvester-prod
%{scriptdir}/harvester.conf
/etc/httpd/conf.d/kata.conf

%{patchdir}/attribute-map.xml.patch
%{patchdir}/attribute-policy.xml.patch
%{patchdir}/shib.conf.patch
%{patchdir}/shibboleth2.xml.patch
%{patchdir}/ssl.conf.patch
%{patchdir}/tomcat6.conf.patch
%{patchdir}/who.ini.patch


%pre
useradd %{ckanuser}  # needs to be removed if ckanuser were changed to httpd

%post
%{scriptdir}/04configuredependencies.sh %{patchdir}
%{scriptdir}/20setuppostgres.sh %{patchdir}
su -c "%{scriptdir}/26setupckanprod.sh /home/%{ckanuser}" %{ckanuser}
su -c "%{scriptdir}/35setupharvester.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/16configshibbolethsp.sh "/usr/share/kata-ckan-prod"
%{scriptdir}/24setupapachessl.sh "/usr/share/kata-ckan-prod"
%{scriptdir}/32setupckanservice.sh %{patchdir}

# Lets do this last so our harvesters are correctly picked up by the daemons.
cat /usr/share/kata-ckan-prod/setup-scripts/harvester.conf >> /etc/supervisord.conf
# Enable tmp directory for logging. Otherwise goes to /
sed -i 's/;directory/directory/' /etc/supervisord.conf
chkconfig supervisord on
%{scriptdir}/40configsolr.sh /home/%{ckanuser}
%{scriptdir}/61setupsources.sh /home/%{ckanuser}
service atd restart
at -f %{scriptdir}/runharvester.sh 'now + 3 minute'

service shibd start
service httpd start
service supervisord start

%preun
service ckan-dev stop
# design assumption is that kata is on a "single purpose" server, we 
# initialize postgres during installation, so we also stop it here
service postgresql stop

%postun
userdel -r %{ckanuser}
# TODO: we must support updates, but we must never ever lose the production
# database
echo 'Consider "rm -rf /var/lib/pgsql/data"' 
echo "Uninstallation not really supported yet, better get a clean VM..."

%changelog
* Tue Sep 11 2012 Harri Palojärvi <harri.palojarvi@nomovok.com>
- Added shibboleth

* Mon May 22 2012 Uwe Geuder <uwe.geuder@nomovok.com>
- Initial version
