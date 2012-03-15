%define glib2_version 2.25.9
%define pango_version 1.1.3
%define gtk2_version 2.21.2
%define mate_icon_theme_version 1.1.0
%define libxml2_version 2.4.20
%define desktop_file_utils_version 0.7
%define mate_desktop_version 1.1.0
%define redhat_menus_version 0.25
%define startup_notification_version 0.5
%define libexif_version 0.5.12
%define mateconf_version 1.1.0
%define exempi_version 1.99.5
%define unique_version 1.0.4

Name:			caja
Summary:    	File manager for MATE
Version:		1.2.0
Release:		1%{?dist}
License:		GPLv2+
Group:          User Interface/Desktops
Source:			http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
URL: 			http://mate-desktop.org
Requires:		gamin
Requires:       filesystem >= 2.1.1-1
Requires:       redhat-menus >= %{redhat_menus_version}
Requires:       gvfs >= 1.4.0
Requires:       mate-icon-theme >= %{mate_icon_theme_version}
Requires:       libexif >= %{libexif_version}

BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	pango-devel >= %{pango_version}
BuildRequires:	gtk2-devel >= %{gtk2_version}
BuildRequires:	libxml2-devel >= %{libxml2_version}
BuildRequires:  mate-desktop-devel >= %{mate_desktop_version}
BuildRequires:	gamin-devel
BuildRequires:	gvfs-devel
BuildRequires:  intltool >= 0.40.6-2
BuildRequires:  libX11-devel
BuildRequires:  libXt-devel
BuildRequires:  fontconfig
BuildRequires:  desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires:  libtool >= 1.4.2-10
BuildRequires:  startup-notification-devel >= %{startup_notification_version}
BuildRequires:  libexif-devel >= %{libexif_version}
BuildRequires:  exempi-devel >= %{exempi_version}
BuildRequires:  gettext
BuildRequires:  libselinux-devel
BuildRequires:  gtk-doc
BuildRequires:  scrollkeeper
BuildRequires:  gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires:  unique-devel
BuildRequires:  mate-conf-devel
BuildRequires:  mate-common
BuildRequires:  cairo-gobject-devel

Requires(pre): mate-conf >= %{mategconf_version}
Requires(preun): mate-conf >= %{mateconf_version}
Requires(post): mate-conf >= %{mateconf_version}
Requires:	mate-desktop >= %{mate_desktop_version}


# the main binary links against libcaja-extension.so
# don't depend on soname, rather on exact version
Requires:	caja-extensions = %{version}-%{release}

Obsoletes:      eel2 < 2.26.0-3
Provides:       eel2 = 2.26.0-3

# Some changes to default config
Patch1:         nautilus-config.patch

Patch7:		caja-rtl-fix.patch

# http://bugzilla.gnome.org/show_bug.cgi?id=519743
Patch17:	nautilus-filetype-symlink-fix.patch

# [bn_IN, gu_IN][nautilus] - Its crashing, when drag any file
# https://bugzilla.redhat.com/show_bug.cgi?id=583559
Patch23:	nautilus-578086-po.patch

Patch24: caja_add_location_togglebutton.patch


%description
Caja is the file manager and graphical shell for the MATE desktop
that makes it easy to manage your files and the rest of your system.
It allows to browse directories on local and remote filesystems, preview
files and launch applications associated with them.
It is also responsible for handling the icons on the GNOME desktop.

%package extensions
Summary: Caja extensions library
License: LGPLv2+
Group: Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description extensions
This package provides the libraries used by caja extensions.

%package devel
Summary: Support for developing caja extensions
License: LGPLv2+
Group: Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig
Obsoletes:      eel2-devel < 2.26.0-3
Provides:       eel2-devel = 2.26.0-3

%description devel
This package provides libraries and header files needed
for developing caja extensions.

%prep
%setup -q -n %{name}-%{version}

# let's use the ./autogen.sh hammer for now.
NOCONFIGURE=1 ./autogen.sh

%patch1 -p1 -b .config
%patch7 -p1 -b .caja-rtl-fix
%patch17 -p0 -b .symlink
%patch23 -p1 -b .gu_IN-crash
%patch24 -p1 -b .add_location_togglebutton

%build

# -fno-tree-vrp is needed to avoid gcc-4.4.0 optimization failure
# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=39233
CFLAGS="$RPM_OPT_FLAGS -g -DUGLY_HACK_TO_DETECT_KDE -DCAJA_OMIT_SELF_CHECK -fno-tree-vrp"

%configure \
	--disable-static \
	--enable-empty-view \
	--enable-unique \
	--enable-introspection=yes


# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

export tagname=CC
LANG=en_US make %{?_smp_mflags}

# strip unneeded translations from .mo files
cd po
grep -v ".*[.]desktop[.]in.*\|.*[.]server[.]in$" POTFILES.in > POTFILES.keep
mv POTFILES.keep POTFILES.in
intltool-update --pot
for p in *.po; do
  msgmerge $p caja.pot > $p.out
  msgfmt -o `basename $p .po`.gmo $p.out
done
# refresh the files in ./po after touching POTFILES.in
make

%install
rm -rf $RPM_BUILD_ROOT
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
export tagname=CC
LANG=en_US %makeinstall LIBTOOL=/usr/bin/libtool
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

rm -f $RPM_BUILD_ROOT%{_libdir}/matecomponent/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

rm -f $RPM_BUILD_ROOT%{_libdir}/matecomponent/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/.icon-theme.cache

mkdir -p $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/mate
mv -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/* $RPM_BUILD_ROOT%{_datadir}/icons/mate

%find_lang caja

%post
/sbin/ldconfig
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null

export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
mateconftool-2 --makefile-install-rule %{_sysconfdir}/mateconf/schemas/apps_caja_preferences.schemas > /dev/null || :

touch --no-create %{_datadir}/icons/mate >&/dev/null || :

%pre
if [ "$1" -gt 1 ]; then
    export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
    mateconftool-2 --makefile-uninstall-rule %{_sysconfdir}/mateconf/schemas/apps_caja_preferences.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
    export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
    mateconftool-2 --makefile-uninstall-rule %{_sysconfdir}/mateconf/schemas/apps_caja_preferences.schemas > /dev/null || :
fi

%postun
/sbin/ldconfig

if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/mate >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/mate >&/dev/null || :
fi

%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null

%posttrans
gtk-update-icon-cache %{_datadir}/icons/mate >&/dev/null || :

%files  -f caja.lang
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING-DOCS COPYING.LIB NEWS README
%{_datadir}/caja
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_bindir}/*
%{_sysconfdir}/mateconf/schemas/*
%{_datadir}/icons/mate/*/apps/caja.png
%{_datadir}/icons/mate/scalable/apps/caja.svg
%{_mandir}/man1/caja-connect-server.1.gz
%{_mandir}/man1/caja-file-management-properties.1.gz
%{_mandir}/man1/caja.1.gz
%{_libexecdir}/caja-convert-metadata
%{_datadir}/mime/*

%files extensions
%defattr(-, root, root)
%{_libdir}/libcaja-extension.so.*
%{_libdir}/girepository-1.0/*.typelib
%dir %{_libdir}/caja
%dir %{_libdir}/caja/extensions-2.0

%files devel
%defattr(-, root, root)
%{_includedir}/caja
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/gir-1.0/*.gir
%doc %{_datadir}/gtk-doc/html/libcaja-extension/*


%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Fri Mar 02 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-8
- fix mock build error
- add nautilus-filetype-symlink-fix.patch from fedora

* Thu Mar 01 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-7
- add caja_add_location_togglebutton.patch

* Fri Feb 24 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-6
- revert build error for i686
* Thu Feb 23 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-5
- fixed build error for i686
- add gnome-disk-utility-libs dependency

* Tue Feb 14 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-4
- fix %postun error

* Sun Feb 12 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-3
- rebuild for enable builds for .i686

* Tue Jan 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-2
- added some patches from nautilus-2.32.0-1.fc14
- updated to new git version 

* Tue Jan 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-1
- updated to 1.1.2 version

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-file-manager.spec based on nautilus-2.32.0-1.fc14 spec

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

