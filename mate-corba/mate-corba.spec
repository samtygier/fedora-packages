%define libidl_version 0.8.2-1
%define glib2_version 2.2.0

Summary: 		A high-performance CORBA Object Request Broker
Name: 			mate-corba
Version: 		1.2.2
Release: 		1%{?dist}
Source: 		http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
Group: 			System Environment/Daemons
License: 		LGPLv2+ and GPLv2+
URL: 			http://pub.mate-desktop.org
BuildRequires: 	libIDL-devel >= %{libidl_version}
BuildRequires: 	glib2-devel >= %{glib2_version}
BuildRequires: 	pkgconfig >= 0.14
BuildRequires: 	libtool
BuildRequires: 	autoconf
BuildRequires: 	automake
BuildRequires: 	gtk-doc
BuildRequires: 	mate-common

# Fedora-specific script for packaging:
Source1000: mate-corba-get-snapshot.sh
# To generate tarball for Source0:
#   sh mate-corba-snapshot.sh %{githash}

# handle ref leaks in the a11y stack more gracefully
Patch0: mate-corba-2.14.3-ref-leaks.patch

%description
mate-corba is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker). It allows programs to
send requests and receive replies from other programs, regardless
of the locations of the two programs. CORBA is an architecture that
enables communication between program objects, regardless of the
programming language they're written in or the operating system they
run on.

You will need to install this package and mate-corba-devel if you want to
write programs that use CORBA technology.

%package devel
Summary: Development libraries, header files and utilities for mate-corba
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: indent
Requires: libIDL-devel >= %{libidl_version}
Requires: glib2-devel >= %{glib2_version}
# we install a pc file
Requires: pkgconfig
# we install an automake macro
Requires: automake

%description devel
mate-corba is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker) with support for the
C language.

This package contains the header files, libraries and utilities
necessary to write programs that use CORBA technology.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .ref-leaks
NOCONFIGURE=1 ./autogen.sh

%build

# let's use the ./autogen.sh hammer for now.
%configure \
	--disable-static \
	--enable-gtk-doc \
	--enable-purify

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

#rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
#rm -f $RPM_BUILD_ROOT%{_libdir}/matecorba-2.0/*.*a

# fix multilib conflict caused by matecorba-config.h
%ifarch x86_64 s390x ia64 ppc64 alpha sparc64
%define wordsize 64
%else
%define wordsize 32
%endif

mv $RPM_BUILD_ROOT%{_includedir}/matecorba-2.0/matecorba/matecorba-config.h \
   $RPM_BUILD_ROOT%{_includedir}/matecorba-2.0/matecorba/matecorba-config-%{wordsize}.h

cat >$RPM_BUILD_ROOT%{_includedir}/matecorba-2.0/matecorba/matecorba-config.h <<EOF
#ifndef MATECORBA_MULTILIB
#define MATECORBA_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "matecorba-config-32.h"
#elif __WORDSIZE == 64
# include "matecorba-config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
%{_libdir}/*.so.*
%dir %{_libdir}/matecorba-2.0
%{_libdir}/matecorba-2.0/*.so*
%{_libdir}/libMateCORBA-2.la
%{_libdir}/libMateCORBA-imodule-2.la
%{_libdir}/libMateCORBACosNaming-2.la
%{_libdir}/matecorba-2.0/Everything_module.la


%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
# this is needed by matecomponent
%{_libdir}/libname-matecorba-server-2.a
%{_libdir}/pkgconfig/*
%{_bindir}/matecorba-idl-2
%{_bindir}/matecorba-typelib-dump
%{_bindir}/matecorba2-config
%{_bindir}/matecorba-ior-decode-2
%{_includedir}/*
%{_datadir}/aclocal/*
%{_datadir}/idl/matecorba-2.0
%{_bindir}/matecorba-linc-cleanup-sockets
%{_datadir}/gtk-doc

%changelog
* Tue Mar 27 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.2-1
- update to 1.2.2

* Thu Mar 01 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
-update verion to 1.2

* Sun Feb 19 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- fix rpmbuild error mate-netspeed-applet

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Wed Jan 10 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- jump to new version 1.1.0

* Sun Nov 13 2011 Eric Smith <eric@brouhaha.com> - 1.0-1.20111112gitebd4a9bf6a
- mate-corba spec based on Fedora 14 ORBit-2.14.19-1 spec
