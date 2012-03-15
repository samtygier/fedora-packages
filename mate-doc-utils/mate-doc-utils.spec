%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

### Abstract ###

Name: 		mate-doc-utils
Version: 	1.2.1
Release: 	1%{?dist}
License: 	GPLv2+ and LGPLv2+ and GFDL
Group: 		Development/Tools
Summary: 	Documentation utilities for MATE
URL: 		https://github.com/mate-desktop/mate-doc-utils
Source: 	%{name}-%{version}.tar.gz

BuildArch: noarch

### Patches ###

# Fedora-specific script for packaging:
#Source1000: mate-doc-utils-get-snapshot.sh
# To generate tarball for Source0:
#   sh mate-doc-utils-get-snapshot.sh %{githash}

# RH bug #438638 / GNOME bug #524207
Patch1: mate-doc-utils-0.14.0-package.patch

Patch2: mate-doc-utils_rename.patch

### Dependencies ###

Requires: libxml2 >= 2.6.12
Requires: libxslt >= 1.1.8
Requires: libxml2-python
# for /usr/share/aclocal
Requires: automake
# for /usr/share/mate/help
Requires: mate-doc-utils-stylesheets = %{version}-%{release}

### Build Dependencies ###

BuildRequires: libxml2-devel >= 2.6.12
BuildRequires: libxslt-devel >= 1.1.8
BuildRequires: libxml2-python

BuildRequires: intltool
BuildRequires: gettext
BuildRequires: scrollkeeper
BuildRequires: rarian-devel
BuildRequires: mate-common
BuildRequires: mate-doc-utils


%description
mate-doc-utils is a collection of documentation utilities for the MATE
project. Notably, it contains utilities for building documentation and
all auxiliary files in your source tree.

# note that this is an "inverse dependency" subpackage
%package stylesheets
Summary: XSL stylesheets used by mate-doc-utils
License: LGPLv2+
Group: Development/Tools
# for /usr/share/pkgconfig
Requires: pkgconfig
# for /usr/share/xml
Requires: xml-common

%description stylesheets
The mate-doc-utils-stylesheets package contains XSL stylesheets which
are used by the tools in mate-doc-utils.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .package
%patch2 -p1 -b .mate-doc-utils_rename

# need for complete mate-doc-utils_rename.patch
mv -f $RPM_BUILD_DIR/%{name}-%{version}/xml2po/xml2po.pc.in $RPM_BUILD_DIR/%{name}-%{version}/xml2po/matexml2po.pc.in
mv -f $RPM_BUILD_DIR/%{name}-%{version}/xml2po/xml2po.1 $RPM_BUILD_DIR/%{name}-%{version}/xml2po/matexml2po.1
mv -f $RPM_BUILD_DIR/%{name}-%{version}/xml2po/xml2po.1.xml $RPM_BUILD_DIR/%{name}-%{version}/xml2po/matexml2po.1.xml
mv -f $RPM_BUILD_DIR/%{name}-%{version}/xml2po/xml2po/xml2po.py.in $RPM_BUILD_DIR/%{name}-%{version}/xml2po/xml2po/matexml2po.py.in
mv -f $RPM_BUILD_DIR/%{name}-%{version}/rng/mallard/mallard.rnc $RPM_BUILD_DIR/%{name}-%{version}/rng/mallard/matemallard.rnc
mv -f $RPM_BUILD_DIR/%{name}-%{version}/rng/mallard/mallard.rng $RPM_BUILD_DIR/%{name}-%{version}/rng/mallard/matemallard.rng

NOCONFIGURE=1 ./autogen.sh

%build
%configure --disable-scrollkeeper --enable-build-utils
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

sed -i -e '/^Requires:/d' $RPM_BUILD_ROOT%{_datadir}/pkgconfig/matexml2po.pc

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS README NEWS COPYING COPYING.GPL COPYING.LGPL
%{_bindir}/*
%{_datadir}/pkgconfig/mate-doc-utils.pc
%{_datadir}/aclocal/mate-doc-utils.m4
%{_datadir}/mate/help/mate-doc-make
%{_datadir}/mate/help/mate-doc-xslt
%{_datadir}/omf/mate-doc-make
%{_datadir}/omf/mate-doc-xslt
%{_datadir}/mate-doc-utils
%doc %{_mandir}/man1/matexml2po.1.gz
%{python_sitelib}/matexml2po/

%files stylesheets
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/matexml2po.pc
%{_datadir}/xml/mate
%{_datadir}/xml/mallard

%changelog
* Thu Mar 01 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
- update version to 1.2
- rename the xml2po and mallard part to avoid conflicts with gnome-doc-utils

* Mon Jan 10 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- jump to new version 1.1.0

* Sun Nov 13 2011 Eric Smith <eric@brouhaha.com> - 1.0.0-1.20111112gitebd4a9bf6a
- mate-doc-utils spec based on Fedora 14 gnome-doc-utils-0.20.2-1 spec
