%define dbus_version		0.90
%define dbus_glib_version	0.70

Summary: 		Desktop notification library
Name: 			libmatenotify
Version: 		1.2.0
Release: 		1%{?dist}
URL: 			https://github.com/mate-desktop/libmatenotify
Source0: 		%{name}-%{version}.tar.gz
License: 		LGPLv2+
Group: 			System Environment/Libraries
BuildRequires: 	libtool
BuildRequires: 	glib2-devel >= %{glib2_version}
BuildRequires: 	gdk-pixbuf2-devel
BuildRequires: 	dbus-devel >= %{dbus_version}
BuildRequires: 	dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: 	gobject-introspection-devel
BuildRequires:  mate-common
BuildRequires:  gtk-doc
BuildRequires:  gtk2-devel
Requires: 		glib2 >= %{glib2_version}


%description
libnotify is a library for sending desktop notifications to a notification
daemon, as defined in the freedesktop.org Desktop Notifications spec. These
notifications can be used to inform the user about an event or display some
form of information without getting in the user's way.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:   glib2-devel >= %{glib2_version}
Requires:	dbus-devel >= %{dbus_version}
Requires:	dbus-glib-devel >= %{dbus_glib_version}
Requires:	pkgconfig

%description devel
This package contains libraries and header files needed for
development of programs using %{name}.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static \

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING NEWS AUTHORS

%{_bindir}/mate-notify-send
%{_libdir}/libmatenotify.so.*

%files devel
%dir %{_includedir}/libmatenotify
%{_includedir}/libmatenotify/*
%{_libdir}/libmatenotify.so
%{_libdir}/pkgconfig/libmatenotify.pc
%dir %{_datadir}/gtk-doc/html/libmatenotify
%{_datadir}/gtk-doc/html/libmatenotify/*


%changelog
* Thu Mar 01 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
-update verion to 1.2

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> 1.1.0-1
- libmatenotify.spec based on libnotify-0.7.4-1.fc16.spec

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.4-1
- Update to 0.7.4
