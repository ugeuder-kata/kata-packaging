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
Requires: sudo
Conflicts: kata-ckan-dev
BuildRequires: kata-ckan-dev
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
%setup


%build
sudo find /home/ckan ! -type d >ckanfiles.list 


%install
sudo find /home/%{ckanuser} -depth | sudo cpio -pdm $RPM_BUILD_ROOT/home/%{ckanuser}
#install -d $RPM_BUILD_ROOT/%{scriptdir}
#install getpyenv.sh $RPM_BUILD_ROOT/%{scriptdir}/


%clean
rm -rf $RPM_BUILD_ROOT

%files -f ckanfiles.list
%defattr(-,{%ckanuser},%{ckanuser})
#%{scriptdir}/getpyenv.sh

%pre
useradd %{ckanuser}  # needs to be removed if ckanuser were changed to httpd

%post
echo Done

%postun
echo "Uninstallation not supported yet, better get a clean VM..."

%changelog
* Mon May 22 2012 Uwe Geuder <uwe.geuder@nomovok.com>
- Initial version
