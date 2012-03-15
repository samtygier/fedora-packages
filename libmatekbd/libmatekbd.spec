Name:           libmatekbd
Version:        1.2.0
Release:        1%{?dist}
Summary:        A keyboard configuration library

Group:          System Environment/Libraries
License:        LGPLv2+
URL: 			http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

BuildRequires:  cairo-devel
BuildRequires:  libxklavier-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  mate-conf-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk2-devel
BuildRequires:  mate-common

Requires(post): mate-conf

%description
The libmatekbd package contains a MATE library which manages
keyboard configuration and offers various widgets related to
keyboard configuration.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The libgnomekbd-devel package contains libraries and header files for
developing applications that use libmatekbd.


%package        capplet
Summary:        A configuration applet to select libmatekbd plugins
Group:          User Interface/Desktops
Requires:       %{name} = %{version}-%{release}

%description    capplet
The libmatekbd-capplet package contains a configuration applet to
select libmatekbd plugins. These plugins can modify the appearance
of the keyboard indicator applet.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_keyboard_xkb.schemas \
	> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_keyboard_xkb.schemas \
	> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_keyboard_xkb.schemas \
	> /dev/null || :
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB
%{_libdir}/*.so.*
%{_datadir}/libmatekbd
%{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_keyboard_xkb.schemas


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files capplet
%defattr(-,root,root,-)
%{_bindir}/matekbd-indicator-plugins-capplet
%{_datadir}/applications/matekbd-indicator-plugins-capplet.desktop

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Thu Feb 16 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- libmatekbd.spec based on libgnomekbd-2.30.2-1.fc13 spec
