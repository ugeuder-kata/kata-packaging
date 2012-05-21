Summary: Development and packaging environment for Kata CKAN
Name: kata-ckan-dev
Version: 0.1
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: GPLv2+ (to be verified)
#Url: http://not.sure.yet
Source: kata-ckan-dev-%{version}.tgz
#Patch1: tree-1.2-carrot.patch
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

%changelog
* Mon May 21 2012 Uwe Geuder <uwe.geuder@nomvok.com>
- Initial version
