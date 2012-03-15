%define gtk2_version           2.11.5
%define libmateui_version      1.1.2
%define libglade2_version      2.5.0
%define dbus_version           0.90
%define dbus_glib_version      0.70
%define libxml2_version        2.6.0
%define mate-conf_version      1.1.0
%define redhat_menus_version   5.0.1
%define mate_menus_version     1.1.1
%define mate_desktop_version   1.1.0
%define libexif_version        0.6.12
%define libmatekbd_version     1.1.0

Summary: 	MATE Screensaver
Name: 		mate-screensaver
Version: 	1.2.0
Release: 	2%{?dist}
License: 	GPLv2+
Group: 		Amusements/Graphics
Source0: 	%{name}-%{version}.tar.gz
URL: 		https://github.com/mate-desktop/mate-screensaver

Patch1: gnome-screensaver-2.20.0-default-theme.patch
#Patch2: gnome-screensaver-2.26.0-securitytoken.patch
Patch7: gnome-screensaver-2.20.0-blank-by-default.patch
Patch8: gnome-screensaver-2.20.0-selinux-permit.patch

BuildRequires: gtk2-devel => %{gtk2_version}
BuildRequires: libmateui-devel => %{libmateui_version}
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: mate-conf-devel >= %{mate_conf_version}
BuildRequires: mate-menus-devel >= %{mate_menus_version}
BuildRequires: mate-desktop-devel >= %{mate_desktop_version}
BuildRequires: libexif-devel >= %{libexif_version}
BuildRequires: pam-devel
BuildRequires: libX11-devel, libXScrnSaver-devel, libXext-devel
BuildRequires: libXinerama-devel libXmu-devel
BuildRequires: libmatekbd-devel >= %{libmatekbd_version}
BuildRequires: libmatenotify-devel
# this is here because the configure tests look for protocol headers
BuildRequires: xorg-x11-proto-devel
BuildRequires: gettext
BuildRequires: nss-devel
BuildRequires: automake, autoconf, libtool, intltool, mate-common
BuildRequires: libXxf86misc-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXtst-devel
BuildRequires: desktop-file-utils
BuildRequires: mate-common
Requires(pre): mate-conf >= %{mate_conf_version}
Requires(preun): mate-conf >= %{mate_conf_version}
Requires(post): mate-conf >= %{mate_conf_version}
Requires: redhat-menus >= %{redhat_menus_version}
Requires: system-logos
# since we use it, and pam spams the log if a module is missing
Requires: gnome-keyring-pam
#Requires: fedora-screensaver-theme
Conflicts: xscreensaver < 1:5.00-19


%description
mate-screensaver is a screen saver and locker that aims to have
simple, sane, secure defaults and be well integrated with the desktop.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh
%patch1 -p1 -b .use-floaters-by-default
#%patch2 -p1 -b .securitytoken
%patch7 -p1 -b .blank-by-default
%patch8 -p1 -b .selinux-permit

autoreconf -f -i

%build

%configure \
	--disable-static \
	--with-xscreensaverdir=/usr/share/xscreensaver/config \
	--with-xscreensaverhackdir=/usr/libexec/xscreensaver  \
	--enable-locking \
	--enable-pam

make %{?_smp_mflags}

%install
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

#desktop-file-install --vendor gnome --delete-original                   \
#  --dir $RPM_BUILD_ROOT%{_datadir}/applications                         \
#  --add-only-show-in GNOME                                              \
#  --add-only-show-in XFCE                                               \
#  $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

%find_lang %{name}

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/mate-screensaver.schemas \
	> /dev/null || :
%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/mate-screensaver.schemas \
	> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/mate-screensaver.schemas \
	> /dev/null || :
fi

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README COPYING
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/applications/mate-screensaver-preferences.desktop
%{_datadir}/applications/screensavers/
%{_datadir}/mate-screensaver/
%{_datadir}/backgrounds/cosmos
%{_datadir}/pixmaps/mate-logo-white.svg
%{_datadir}/desktop-directories/mate-screensaver.directory
%dir %{_datadir}/mate-background-properties
%{_datadir}/mate-background-properties/cosmos.xml
%{_sysconfdir}/mateconf/schemas/*.schemas
%{_sysconfdir}/xdg/menus/mate-screensavers.menu
%{_sysconfdir}/pam.d/*
%{_sysconfdir}/xdg/autostart/mate-screensaver.desktop
%{_datadir}/dbus-1/services/org.mate.ScreenSaver.service
%doc %{_mandir}/man1/*.1.gz

%changelog
* Sat Mar 10 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-2
- test build for switching to gnome-keyring

* Thu Mar 08 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2
- add mate-system-monitor_glib-3.1.patch

* Tue Feb 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- remove fedora-screensaver-theme bcause it's install gnome-keyring

* Tue Feb 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686
- enable fedora patches

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-screensaver.spec based on gnome-screensaver fc14 spec

* Wed Oct 13 2010 Bastien Nocera <bnocera@redhat.com> 2.30.2-2
- Really hide xscreensaver properties from the menus when
  gnome-screensaver is installed (#530318)

