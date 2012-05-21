Summary: Development and packaging environment for Kata CKAN
Name: kata-ckan-dev
Version: 0.1
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: GPLv2+ (to be verified)
#Url: http://not.sure.yet
Source: kata-ckan-dev-%{version}.tgz
#Patch1: tree-1.2-carrot.patch
BuildRequires: gcc
BuildRequires: git
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: mercurial
BuildRequires: postgresql-devel
BuildRequires: postgresql-server
BuildRequires: python-devel
BuildRequires: subversion
BuildRequires: sudo
Requires: libxml2
Requires: libxslt
Requires: postgresql
Requires: postgresql-server
Requires: sudo
Conflicts: kata-ckan-prod
#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Installs a CKAN environment using pip.
This package is for internal development use only. Not intended to be used
on production systems. After installing a development system build
a kata-ckan-prod.rpm package to capture the result of this installation.

%prep
%setup -q

%build
echo "nothing to be built here"
touch foo


%install
mkdir -p $RPM_BUILD_ROOT/tmp/foo
cp foo $RPM_BUILD_ROOT/tmp/foo


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/tmp/foo/foo

%post
echo "The real work goes here"

%postun
echo "Uninstallation not supported yet, better get a clean VM..."

%changelog
* Mon May 21 2012 Uwe Geuder <uwe.geuder@nomvok.com>
- Initial version
