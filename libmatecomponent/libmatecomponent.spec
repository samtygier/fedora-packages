%define libxml2_version 2.4.21
%define mate_corba_version 1.1.0

Summary: 		libmate component system
Name: 			libmatecomponent
Version: 		1.2.0
Release: 		1%{?dist}
URL: 			http://mate-desktop.org
Source0: 		http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
License: 		GPLv2+ and LGPLv2+
Group: 			System Environment/Libraries
BuildRequires: 	libxml2-devel >= %{libxml2_version}
BuildRequires: 	mate-corba-devel >= %{mate_corba_version}
BuildRequires: 	intltool >= 0.14-1
BuildRequires: 	automake autoconf libtool
BuildRequires: 	gtk-doc
BuildRequires: 	flex, bison, zlib-devel, popt-devel
BuildRequires: 	dbus-glib-devel
BuildRequires: 	gettext
BuildRequires:  mate-common
Provides: 		libmatecomponent-activation = %{version}-%{release}

Patch0: libbonobo-multishlib.patch

%description
libmatecomponent is a component system based on CORBA, used by the MATE desktop.

%package devel
Summary: 	Libraries and headers for libmatecomponent
Group: 		Development/Libraries
Requires:  	%name = %{version}-%{release}
Requires:  	mate-corba-devel >= %{mate_corba_version}
Requires:  	libxml2-devel >= %{libxml2_version}
Requires:  	popt-devel
Provides: 	libmatecomponent-activation-devel = %{version}-%{release}

%description devel
libmatecomponent is a component system based on CORBA, used by the MATE desktop.

This package contains header files used to compile programs that
use libmatecomponent.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .multishlib
NOCONFIGURE=1 ./autogen.sh 

%build
%configure \
	--disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

## kill other stuff
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/matecomponent/monikers/*.la
rm $RPM_BUILD_ROOT%{_libdir}/matecorba-2.0/*.la

for serverfile in $RPM_BUILD_ROOT%{_libdir}/matecomponent/servers/*.server; do
    sed -i -e 's|location *= *"/usr/lib\(64\)*/|location="/usr/$LIB/|' $serverfile
done

# noarch packages install to /usr/lib/matecomponent/servers
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/matecomponent/servers

%find_lang libmatecomponent

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libmatecomponent.lang
%defattr(-,root,root)

%doc AUTHORS COPYING NEWS README doc/NAMESPACE

%{_libdir}/lib*.so.*
%{_libdir}/matecomponent
%{_libdir}/matecorba-2.0/*.so*
%{_bindir}/*
%{_libexecdir}/*
%{_sbindir}/*
%dir %{_prefix}/lib/matecomponent/servers
%dir %{_prefix}/lib/matecomponent
%dir %{_sysconfdir}/matecomponent-activation
%config %{_sysconfdir}/matecomponent-activation/*
%{_datadir}/man/man*/*
%{_libdir}/matecomponent-2.0/samples/matecomponent-echo-2

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/idl/*
%{_datadir}/gtk-doc/html/libmatecomponent
%{_datadir}/gtk-doc/html/matecomponent-activation/*

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Thu Feb 16 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Sat Dec 24 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- libmatecomponent.spec based on libbonobo-2.32.1-1.fc16.spec

* Mon Apr  4 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.32.1-1
- Update to 2.32.1
