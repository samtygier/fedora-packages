Summary: 	PolicyKit integration for the MATE desktop
Name: 		mate-polkit
Version: 	1.2.0
Release: 	1%{?dist}
License: 	LGPLv2+
URL: 		http://mate-desktop.org
Group: 		Applications/System
Source0: 	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

BuildRequires: gtk2-devel
BuildRequires: glib2-devel >= 2.25.11
BuildRequires: polkit-devel >= 0.97-1
BuildRequires: desktop-file-utils
BuildRequires: intltool
BuildRequires: gobject-introspection-devel
BuildRequires: gtk-doc
BuildRequires: mate-common
BuildRequires: cairo-gobject-devel

Provides: polkit-mate-1 = 1.1.0
Provides: libpolkit-gtk-mate-1 = 1.1.0

Provides: polkit-mate-authentication-agent-1

Requires: polkit >= 0.97

%description
mate-polkit provides an authentication agent for PolicyKit
that matches the look and feel of the MATE desktop.

%package devel
Summary: Development files for mate-polkit
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: %name-docs = %{version}-%{release}
Requires: polkit-devel
Provides: mate-polkit-devel = 1.1.0
Provides: mate-polkit-demo = 1.1.0

%description devel
Development files for mate-polkit.

%package docs
Summary: Development documentation for mate-polkit
Group: Development/Libraries
Requires: %name-devel = %{version}-%{release}

%description docs
Development documentation for mate-polkit.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static \
	--enable-examples \
	--enable-introspection \
	--enable-gtk-doc

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang polkit-mate-1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f polkit-mate-1.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS README
%{_sysconfdir}/xdg/autostart/*
%{_libexecdir}/*
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gir-1.0/*.gir

%files docs
%defattr(-,root,root,-)
%{_datadir}/gtk-doc


%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Sun Feb 19 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-polkit.spec based on polkit-gnome-0.97-8.fc15 spec

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

