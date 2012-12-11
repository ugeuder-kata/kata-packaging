Summary: Provides dummy dependencies for Kata CKAN
Name: dummy-deps
%define autov %(echo $AUTOV)
# we had some check here to abort if AUTOV is not set, but it did not
# work. See git history for details
Version: %autov
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: AGPL
#Url: http://not.sure.yet
Source0: dummy-deps-%{version}.tgz
Provides: redhat-lsb-printing
Provides: redhat-lsb-graphics
# Fedora documentation says one should use...
#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# but the old-style(?) default %{_topdir}/BUILDROOT/... seems to work nicely
# so we don't clutter yet another place in the directory tree

%description
This package provides dummy dependencies for Kata. In other words it
claims to provide some packages, which we do not need, but which other
packages depend on. man.rpm is the classic example. It is not needed
on the production server (in fact indexing cronjob disturbs) but it is
pulled in via some dependencies.

%define katadocdir %{_defaultdocdir}/%{name}

%prep
%setup

%build
ln -s dummy.sh man


%install
install -d $RPM_BUILD_ROOT/%{katadocdir}
install README $RPM_BUILD_ROOT/%{katadocdir}/
# redhat-lsb requires /usr/bin/man
install -d $RPM_BUILD_ROOT/usr/bin
install man $RPM_BUILD_ROOT/usr/bin/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{katadocdir}/README
/usr/bin/man


%changelog
* Tue Oct 30 2012 Uwe Geuder <uwe.geuder@nomovok.com>
- Initial version
- for further changes see git history
