Summary: Kata CKAN production
Name: kata-ckan-prod
Version: 0.1
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: GPLv2+ (to be verified)
#Url: http://not.sure.yet
Source: kata-ckan-prod-%{version}.tgz
Requires: libxml2
Requires: libxslt
Requires: postgresql
Requires: postgresql-server
Requires: sudo
Conflicts: kata-ckan-dev
# Fedora documentation says one should use...
#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# but the old-style(?) default %{_topdir}/BUILDROOT/... seems to work nicely
# so we don't clutter yet another place in the directory tree

%define ckanuser ckan
%define scriptdir %{_datadir}/%{name}/setup-scripts

%description
Installs a complete Kata CKAN environment
This package is for the production server.

%prep
%setup -q

%build
echo "nothing to be built here"
touch foo


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
* Mon May 22 2012 Uwe Geuder <uwe.geuder@nomovok.com>
- Initial version
