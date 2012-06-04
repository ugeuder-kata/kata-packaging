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
Requires: libxml2-devel
Requires: libxslt-devel
Requires: mercurial
Requires: patch
Requires: postgresql-devel
Requires: postgresql-server
Requires: python-devel
Requires: subversion
Requires: wget
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
diff -u patches/orig/pg_hba.conf patches/kata/pg_hba.conf >pg_hba.conf.patch || true
diff -u patches/orig/development.ini patches/kata/development.ini >development.ini.patch || true
diff -u patches/orig/search/__init__.py patches/kata/search/__init__.py >search__init__.py.patch || true


%install
install -d $RPM_BUILD_ROOT/%{scriptdir}
install -d $RPM_BUILD_ROOT/%{patchdir}
install -d $RPM_BUILD_ROOT/%{katadatadir}
install -d $RPM_BUILD_ROOT/usr/bin
install -d $RPM_BUILD_ROOT/etc/init.d
install 01getpyenv.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 02getpythonpackages.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 05setuppostgres.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 10setupckan.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 14openfirewall.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 20setupckanservice.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 70checkpythonpackages.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 80backuphome.sh $RPM_BUILD_ROOT/%{scriptdir}/
install pg_hba.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install development.ini.patch $RPM_BUILD_ROOT/%{patchdir}/
install search__init__.py.patch $RPM_BUILD_ROOT/%{patchdir}/
install log/pip.freeze $RPM_BUILD_ROOT/%{katadatadir}/
install paster-ckan $RPM_BUILD_ROOT/usr/bin/
install paster-ckan2 $RPM_BUILD_ROOT/usr/bin/
install ckan-dev $RPM_BUILD_ROOT/etc/init.d/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{scriptdir}/01getpyenv.sh
%{scriptdir}/02getpythonpackages.sh
%{scriptdir}/05setuppostgres.sh
%{scriptdir}/10setupckan.sh
%{scriptdir}/14openfirewall.sh
%{scriptdir}/20setupckanservice.sh
%{scriptdir}/70checkpythonpackages.sh
%{scriptdir}/80backuphome.sh
%{patchdir}/pg_hba.conf.patch
%{patchdir}/development.ini.patch
%{patchdir}/search__init__.py.patch
%{katadatadir}/pip.freeze
/usr/bin/paster-ckan
/usr/bin/paster-ckan2
/etc/init.d/ckan-dev


%post
useradd %{ckanuser}  # needs to be removed if ckanuser were changed to httpd
su -c "%{scriptdir}/01getpyenv.sh /home/%{ckanuser}" %{ckanuser}
su -c "%{scriptdir}/02getpythonpackages.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/05setuppostgres.sh
su -c "%{scriptdir}/10setupckan.sh /home/%{ckanuser}" %{ckanuser}
%{scriptdir}/14openfirewall.sh
%{scriptdir}/20setupckanservice.sh
# run this last so the user has a chance to see the output
su -c "%{scriptdir}/70checkpythonpackages.sh /home/%{ckanuser} %{katadatadir}/pip.freeze" %{ckanuser}

%preun
%{scriptdir}/80backuphome.sh /home/%{ckanuser}


%postun
echo "Uninstallation not fully supported yet, better get a clean VM to be sure"
echo "User account %{ckanuser} not deleted, firewall change not reverted,"
echo "postgresql configuration not reverted"

%changelog
* Mon May 21 2012 Uwe Geuder <uwe.geuder@nomvok.com>
- Initial version
