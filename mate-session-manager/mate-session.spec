%define gtk_version 2.20
%define dbus_glib_version 0.70
%define dbus_version 0.90
%define mate_keyring_version 1.1.0
%define mate_conf_version 1.1.0
%define libmatenotify_version 1.1.0

Summary: 	MATE session manager
Name: 		mate-session
Version: 	1.2.0
Release: 	1%{?dist}
URL: 		http://pub.mate-desktop.org
Source0: 	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
License: 	GPLv2+
Group: 		User Interface/Desktops

Requires: system-logos
# required to get mateconf-sanity-check-2 in the right place
Requires: mate-conf-gtk >= %{mate_conf_version}
# Needed for mate-settings-daemon
Requires: mate-control-center

# pull in dbus-x11, see bug 209924
Requires: dbus-x11
# we need an authentication agent in the session
Requires: mate-polkit
# and we want good defaults
Requires: polkit-desktop-policy

BuildRequires: gtk2-devel >= %{gtk_version}
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: mate-keyring-devel >= %{mate_keyring_version}
BuildRequires: libmatenotify-devel >= %{libnotify_version}
BuildRequires: mate-conf-devel >= %{mate_conf_version}
BuildRequires: mate-conf-gtk >= %{mate_conf_version}
BuildRequires: pango-devel
BuildRequires: mate-settings-daemon-devel
BuildRequires: desktop-file-utils
BuildRequires: libXau-devel
BuildRequires: libXrandr-devel
BuildRequires: xorg-x11-xtrans-devel

# this is so the configure checks find /usr/bin/halt etc.
BuildRequires: usermode

BuildRequires: intltool, autoconf, automake
BuildRequires: libtool
BuildRequires: gettext
BuildRequires: libX11-devel libXt-devel
BuildRequires: libXtst-devel
BuildRequires: xmlto
BuildRequires: upower-devel
BuildRequires: mate-common

# for patch3
BuildRequires: libmatenotify-devel

Requires(pre): mate-conf >= %{mate_conf_version}
Requires(post): mate-conf >= %{mate_conf_version}
Requires(preun): mate-conf >= %{mate_conf_version}

# https://bugzilla.gnome.org/show_bug.cgi?id=597030
Patch3: 0001-Add-ability-to-perform-actions-after-a-period-of-idl.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=607094
Patch4: nag-root-user.patch

Patch7: gnome-session-cflags.patch

%description
mate-session manages a MATE desktop or GDM / MDM login session. It starts up
the other core MATE components and handles logout and saving the session.

%package xsession
Summary: mate-session desktop file
Group: User Interface/Desktop
Requires: mate-session = %{version}-%{release}

%description xsession
Desktop file to add MATE to display manager session menu.

%prep
%setup -q
%patch3 -p1 -b .max-idle
%patch4 -p1 -b .nag-root-user
%patch7 -p1 -b .cflags
./autogen.sh

%build

%configure \
    --disable-static \
	--with-default-wm=marco \
	--enable-ipv6 \

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

mkdir -p $RPM_BUILD_ROOT%{_datadir}/mate/autostart

cp AUTHORS COPYING NEWS README $RPM_BUILD_ROOT%{_datadir}/doc/mate-session

%find_lang mate-session --all-name

%post
/sbin/ldconfig
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
mateconftool-2 --makefile-install-rule %{_sysconfdir}/mateconf/schemas/mate-session.schemas >& /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule %{_sysconfdir}/mateconf/schemas/mate-session.schemas >& /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule %{_sysconfdir}/mateconf/schemas/mate-session.schemas >& /dev/null || :
fi

%postun -p /sbin/ldconfig

%files xsession
%defattr(-,root,root)
%{_datadir}/xsessions/*

%files -f mate-session.lang
%defattr(-,root,root)
%doc %dir %{_datadir}/doc/mate-session
%doc %{_datadir}/doc/mate-session/AUTHORS
%doc %{_datadir}/doc/mate-session/COPYING
%doc %{_datadir}/doc/mate-session/NEWS
%doc %{_datadir}/doc/mate-session/README
%doc %dir %{_datadir}/doc/mate-session/dbus
%doc %{_datadir}/doc/mate-session/dbus/*
%doc %{_mandir}/man*/*
%{_datadir}/applications/mate-session-properties.desktop
%dir %{_datadir}/mate-session
%{_datadir}/mate/autostart
%{_bindir}/*
%{_sysconfdir}/mateconf/schemas/*.schemas
%{_datadir}/mate-session/gsm-inhibit-dialog.ui
%{_datadir}/mate-session/session-properties.ui
%{_datadir}/icons/hicolor/*/apps/mate-session-properties.png
%{_datadir}/icons/hicolor/scalable/apps/mate-session-properties.svg


%changelog
* Sun Mar 11 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0

* Tue Feb 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-3
- rebuild for enable builds for .i686
- enable last missing fedora patch

* Tue Jan 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-2
- added fedora patches from gnome-session-2.32.0-1.fc14

* Tue Jan 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.2-1
- updated to 1.1.2 version

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-file-manager.spec based on gnome-session-2.32.0-1.fc14 spec

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

