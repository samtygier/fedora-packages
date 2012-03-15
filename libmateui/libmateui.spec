
Summary: 		MATE base GUI library
Name: 			libmateui
Version: 		1.2.0
Release: 		1%{?dist}
URL: 			https://github.com/mate-desktop/libmateui
Source0: 		%{name}-%{version}.tar.gz
License: 		LGPLv2+
Group: 			System Environment/Libraries

# https://bugzilla.gnome.org/show_bug.cgi?id=606437
Patch0: libgnomeui-2.23.4-disable-event-sounds.patch

BuildRequires: 	glib2-devel
BuildRequires: 	pango-devel
BuildRequires: 	gtk2-devel
BuildRequires: 	mate-conf-devel
BuildRequires: 	mate-vfs-devel
BuildRequires: 	libmatecanvas-devel
BuildRequires: 	libmatecomponent-devel
BuildRequires: 	libxml2-devel
BuildRequires: 	libmate-devel
BuildRequires: 	libart_lgpl-devel
BuildRequires: 	libglade2-devel
BuildRequires: 	mate-keyring-devel
BuildRequires: 	libSM-devel
BuildRequires: 	fontconfig-devel
BuildRequires: 	gettext
BuildRequires: 	automake, autoconf, libtool
BuildRequires: 	intltool
BuildRequires:  mate-common
BuildRequires:  libmatecomponentui-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  openssl-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  avahi-glib-devel
BuildRequires:  libselinux-devel

%description
MATE is a user-friendly set of
GUI applications and desktop tools to be used in conjunction with a
window manager for the X Window System. The libgmateui package
includes GUI-related libraries that are needed to run MATE. (The
libgnome package includes the library features that don\'t use the X
Window System.)

%package devel
Summary: Libraries and headers for libgnome
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libSM-devel
Requires: libICE-devel

%description devel
You should install the libmateui-devel package if you would like to
compile MATE applications. You do not need to install
libmateui-devel if you just want to use the MATE desktop
environment.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh
%patch0 -p1 -b .disable-sound-events

libtoolize --force --copy
autoreconf

%build

%configure \
	--disable-static \
	--disable-gtk-doc \
	PKG_CONFIG_PATH=/usr/lib64/pkgconfig

#sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%find_lang libmateui

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libmateui.lang
%defattr(-,root,root,-)
%doc COPYING.LIB NEWS ChangeLog
%{_libdir}/lib*.so.*
%{_datadir}/pixmaps/*
%{_libdir}/libglade/2.0/*.so

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/libmateui
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Wed Feb 29 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
-update verion to 1.2

* Thu Feb 16 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-2
- rebuild for enable builds for .i686
- enable fedora patch

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-1
- libmateui.spec based on libgnomeui-2.24.5-2.fc15.spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

