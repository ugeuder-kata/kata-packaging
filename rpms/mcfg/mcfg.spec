Summary: Master configuration tool (mcfg) packaged for Kata CKAN
Name: mcfg
%define autov %(echo $AUTOV)
# we had some check here to abort if AUTOV is not set, but it did not
# work. See git history for details
Version: %autov
Release: 1%{?dist}
Group: Applications/File (to be verified)
License: AGPLv3+
#Url: http://not.sure.yet
Source0: mcfg-%{version}.tgz
Requires: python
#
# according to http://fedoraproject.org/wiki/Packaging:Python#BuildRequires
# we need
#
# BuildRequires: python2-devel
#
# but it works wothout in a clean machine so we leave it commented out
#
BuildArch: noarch
# Fedora documentation says one should use...
#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# but the old-style(?) default %{_topdir}/BUILDROOT/... seems to work nicely
# so we don't clutter yet another place in the directory tree

%define pydir %{_datadir}/%{name}/tool
%define docdir %{_defaultdocdir}/%{name}
%define configdir %{_datadir}/%{name}/config
%define exampledir %{_datadir}/%{name}/examples


%description
The master configuration tool.
Allows scripted "editing" of configuration files. 
The tool is fully generic and easily extensible. The configuration files
are specified in a template .ini by a packager. This package comes
with the template.ini for kata. The template is not supposed to be
edited by the adminitstrator. Also a sample master .ini for kata is
provided, this one needs to be edited by the adminstrator before
kata installation. 


%prep
%setup


%build
python test/testedfuncs.py


%install
install -d $RPM_BUILD_ROOT/%{pydir}
install -d $RPM_BUILD_ROOT/%{docdir}
install -d $RPM_BUILD_ROOT/%{configdir}
install -d $RPM_BUILD_ROOT/%{exampledir}
install edfuncs.py $RPM_BUILD_ROOT/%{pydir}/
install editor.py $RPM_BUILD_ROOT/%{pydir}/
install target.py $RPM_BUILD_ROOT/%{pydir}/
install mcfg.py $RPM_BUILD_ROOT/%{pydir}/
install DESIGN.txt $RPM_BUILD_ROOT/%{docdir}/
install samples/kata-template.ini $RPM_BUILD_ROOT/%{configdir}/
install samples/kata-master.ini $RPM_BUILD_ROOT/%{exampledir}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{pydir}/edfuncs.py*
%{pydir}/editor.py*
%{pydir}/target.py*
%{pydir}/mcfg.py*
%{docdir}/DESIGN.txt
%{configdir}/kata-template.ini
%{exampledir}/kata-master.ini



%changelog
* Mon Aug 28 2012 Uwe Geuder <uwe.geuder@nomovok.com>
- Initial version
- see git for details
