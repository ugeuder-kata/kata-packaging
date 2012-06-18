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
echo "nothing to be built"


%install
# cpio: we need to be root to be able to read, but we don't preserve the 
# ownership because rpmbuild will in trouble later with such files. 
# %attr will take care of ownership eventually
# sudo is somewhat nasty here (interactive command) but building is
# only carried out by people who know what they are doing...
me=$(whoami)
sudo find /home/%{ckanuser}/pyenv -depth | sudo cpio -pdm --owner ${me}: $RPM_BUILD_ROOT/
# not sure why, but testings show that the following 2 directories are not
# owned by ${me}
sudo chown ${me} $RPM_BUILD_ROOT/home
sudo chown ${me} $RPM_BUILD_ROOT/home/%{ckanuser}
find $RPM_BUILD_ROOT/home/%{ckanuser} -name .git -print0 | xargs rm -rf
find $RPM_BUILD_ROOT/home/%{ckanuser} -name .svn -print0 | xargs rm -rf
#install -d $RPM_BUILD_ROOT/%{scriptdir}
#install getpyenv.sh $RPM_BUILD_ROOT/%{scriptdir}/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{ckanuser},%{ckanuser})
/home/%{ckanuser}/pyenv
#%{scriptdir}/getpyenv.sh

%pre
useradd %{ckanuser}  # needs to be removed if ckanuser were changed to httpd

%post
echo Done

%postun
userdel -r %{ckanuser}
echo "Uninstallation not supported yet, better get a clean VM..."

%changelog
* Mon May 22 2012 Uwe Geuder <uwe.geuder@nomovok.com>
- Initial version
