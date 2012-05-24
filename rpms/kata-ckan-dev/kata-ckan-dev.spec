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
install 01getpyenv.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 02getpythonpackages.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 05setuppostgres.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 10setupckan.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 80backuphome.sh $RPM_BUILD_ROOT/%{scriptdir}/
install pg_hba.conf.patch $RPM_BUILD_ROOT/%{patchdir}/
install development.ini.patch $RPM_BUILD_ROOT/%{patchdir}/
install search__init__.py.patch $RPM_BUILD_ROOT/%{patchdir}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{scriptdir}/01getpyenv.sh
%{scriptdir}/02getpythonpackages.sh
%{scriptdir}/05setuppostgres.sh
%{scriptdir}/10setupckan.sh
%{scriptdir}/80backuphome.sh
%{patchdir}/pg_hba.conf.patch
%{patchdir}/development.ini.patch
%{patchdir}/search__init__.py.patch


%post
useradd %{ckanuser}  # needs to be removed if ckanuser were changed to httpd
sudo -u %{ckanuser} %{scriptdir}/01getpyenv.sh /home/%{ckanuser}
sudo -u %{ckanuser} %{scriptdir}/02getpythonpackages.sh /home/%{ckanuser}
%{scriptdir}/05setuppostgres.sh
sudo -u %{ckanuser} %{scriptdir}/10setupckan.sh /home/%{ckanuser}


%preun
%{scriptdir}/80backuphome.sh /home/%{ckanuser}


%postun
echo "Uninstallation not fully supported yet, better get a clean VM to be sure"
echo "User account %{ckanuser} not deleted"


%changelog
* Mon May 21 2012 Uwe Geuder <uwe.geuder@nomvok.com>
- Initial version
