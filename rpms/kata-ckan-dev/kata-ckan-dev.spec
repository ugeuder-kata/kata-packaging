Summary: Development and packaging environment for Kata CKAN
Name: kata-ckan-dev
%define autov %(echo $AUTOV)
%if !%{autov}
%{error:AUTOV not set}
%endif
Version: %autov
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: GPLv2+ (to be verified)
#Url: http://not.sure.yet
# just use plain source files instead of archive, easier for development
#Source99: kata-ckan-dev-%{version}.tgz
Source0: 01getpyenv.sh
Source2: 80backuphome.sh
Requires: gcc
Requires: git
Requires: libxml2-devel
Requires: libxslt-devel
Requires: mercurial
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

%description
Installs a CKAN environment using pip.
This package is for internal development use only. Not intended to be used
on production systems. After installing a development system build
a kata-ckan-prod.rpm package to capture the result of this installation.

%prep
%setup -c -T
cp ../../SOURCES/01getpyenv.sh .
cp ../../SOURCES/80backuphome.sh .

%build
echo "nothing to be built here"


%install
install -d $RPM_BUILD_ROOT/%{scriptdir}
install 01getpyenv.sh $RPM_BUILD_ROOT/%{scriptdir}/
install 80backuphome.sh $RPM_BUILD_ROOT/%{scriptdir}/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{scriptdir}/01getpyenv.sh
%{scriptdir}/80backuphome.sh

%post
useradd %{ckanuser}  # needs to be removed if ckanuser were changed to httpd
sudo -u %{ckanuser} %{scriptdir}/01getpyenv.sh /home/%{ckanuser}

%preun
%{scriptdir}/80backuphome.sh /home/%{ckanuser}

%postun
echo "Uninstallation not fully supported yet, better get a clean VM to be sure"
echo "User account %{ckanuser} not deleted"

%changelog
* Mon May 21 2012 Uwe Geuder <uwe.geuder@nomvok.com>
- Initial version
