Name:           mate-common
Version:        1.2.1
Release:        1%{?dist}
Summary:        mate-common contains useful things common to building mate packages

Group:          Development/Tools
BuildArch:      noarch
License:        GPL
URL: 			https://github.com/mate-desktop/mate-common
Source0:        http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# This will pull in the latest version; if your package requires something older,
# well, BuildRequire it in that spec.  At least until such time as we have a
# build system that is intelligent enough to inspect your source code
# and auto-inject those requirements.

BuildRequires: automake
BuildRequires: autoconf

Requires: automake
Requires: autoconf
Requires: libtool
Requires: gettext
Requires: pkgconfig

%description
Contains files required to bootstrap various Mate modules when building
from CVS.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure

make %{?_smp_mflags}
cp doc-build/README doc-README
# No sense making a doc subdir in the rpm pkg for one file.
cp doc/usage.txt usage.txt

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc doc-README README COPYING usage.txt ChangeLog
%{_bindir}/*
%{_datadir}/aclocal/*
%{_datadir}/%{name}

%changelog
* Tue Feb 28 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
- update to version 1.2.1

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-common.spec based on gnome-common-2.28.0-3.fc15 spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

