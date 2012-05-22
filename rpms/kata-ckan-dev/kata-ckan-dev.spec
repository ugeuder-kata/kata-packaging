Summary: Development and packaging environment for Kata CKAN
Name: kata-ckan-dev
Version: 0.1
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: GPLv2+ (to be verified)
#Url: http://not.sure.yet
# just use plain source files instead of archive, easier for development
#Source99: kata-ckan-dev-%{version}.tgz
Source0: getpyenv.sh
Requires: gcc
Requires: git
Requires: libxml2-devel
Requires: libxslt-devel
Requires: mercurial
Requires: postgresql-devel
Requires: postgresql-server
Requires: python-devel
Requires: subversion
Requires: sudo
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
cp ../../SOURCES/getpyenv.sh .

%build
echo "nothing to be built here"


%install
install -d $RPM_BUILD_ROOT/%{scriptdir}
install getpyenv.sh $RPM_BUILD_ROOT/%{scriptdir}/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{scriptdir}/getpyenv.sh

%post
useradd %{ckanuser}  # needs to be removed if ckanuser were changed to httpd
sudo -u %{ckanuser} %{scriptdir}/getpyenv.sh

%postun
echo "Uninstallation not supported yet, better get a clean VM..."

%changelog
* Mon May 21 2012 Uwe Geuder <uwe.geuder@nomvok.com>
- Initial version
