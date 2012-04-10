Name:           mate-settings-daemon
Version:        1.2.0
Release:        1%{?dist}
Summary:        The daemon sharing settings from MATE to GTK+/KDE applications

Group:          System Environment/Daemons
License:        GPLv2+
URL:            https://github.com/mate-desktop/mate-settings-daemon
Source:         http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

Requires(pre): 	mate-conf >= 1.1.0
Requires(preun): mate-conf >= 1.1.0
Requires(post): mate-conf >= 1.1.0
Requires: 		mate-control-center-filesystem

BuildRequires:  dbus-glib-devel
BuildRequires:  mate-conf-devel
BuildRequires:  gtk2-devel
BuildRequires:  mate-desktop-devel
BuildRequires:  libglade2-devel
BuildRequires:  libmateui-devel
BuildRequires:  libmate-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  libmatekbd-devel
BuildRequires:  libmatenotify-devel
BuildRequires:  gettext intltool
BuildRequires:  fontconfig-devel
BuildRequires:  libcanberra-devel
BuildRequires:  mate-polkit-devel
BuildRequires:  autoconf automake libtool
BuildRequires:  mate-common
BuildRequires:  nss-devel

# change font rendering
Patch3: slight-hinting.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=610319
Patch4: keyboard-icon.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=628538
Patch5: display-capplet.patch

%description
A daemon to share settings from MATE to other applications. It also
handles global keybindings, as well as a number of desktop-wide settings.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       dbus-glib-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch3 -p1 -b .slight-hinting
%patch4 -p1 -b .keyboard-icon
%patch5 -p1 -b .display-capplet

NOCONFIGURE=1 ./autogen.sh

%build

%configure \
    --disable-static \
	--with-nssdb \
	--enable-polkit

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT


make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{name}

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_housekeeping.schemas \
	%{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_keybindings.schemas \
	%{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_xrandr.schemas \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_font_rendering.schemas \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_keybindings.schemas \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_touchpad.schemas \
	%{_sysconfdir}/mateconf/schemas/mate-settings-daemon.schemas \
	> /dev/null || :

touch --no-create %{_datadir}/icons/mate >&/dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_housekeeping.schemas \
	%{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_keybindings.schemas \
	%{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_xrandr.schemas \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_font_rendering.schemas \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_keybindings.schemas \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_touchpad.schemas \
	%{_sysconfdir}/mateconf/schemas/mate-settings-daemon.schemas \
	> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_housekeeping.schemas \
	%{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_keybindings.schemas \
	%{_sysconfdir}/mateconf/schemas/apps_mate_settings_daemon_xrandr.schemas \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_font_rendering.schemas \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_keybindings.schemas \
	%{_sysconfdir}/mateconf/schemas/desktop_mate_peripherals_touchpad.schemas \
	%{_sysconfdir}/mateconf/schemas/mate-settings-daemon.schemas \
	> /dev/null || :
fi

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/mate >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/mate >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/mate >&/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS
%{_sysconfdir}/mateconf/schemas/*
%dir %{_sysconfdir}/mate-settings-daemon
%dir %{_sysconfdir}/mate-settings-daemon/xrandr
%{_libdir}/mate-settings-daemon-%{version}
%{_libexecdir}/mate-settings-daemon
%{_libexecdir}/msd-locate-pointer
%{_libexecdir}/msd-datetime-mechanism
%{_datadir}/mate-settings-daemon/
%{_datadir}/mate-control-center/keybindings/50-accessibility.xml
%{_datadir}/dbus-1/services/org.mate.SettingsDaemon.service
%{_sysconfdir}/xdg/autostart/mate-settings-daemon.desktop
%{_datadir}/icons/mate/*/apps/*
%{_datadir}/icons/mate/*/actions/*
%{_sysconfdir}/dbus-1/system.d/org.mate.SettingsDaemon.DateTimeMechanism.conf
%{_datadir}/dbus-1/system-services/org.mate.SettingsDaemon.DateTimeMechanism.service
%{_datadir}/polkit-1/actions/org.mate.settingsdaemon.datetimemechanism.policy

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/mate-settings-daemon.pc
%{_includedir}/mate-settings-daemon/*.h


%changelog
* Wed Feb 29 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2

* Tue Feb 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-5
- rebuild for enable builds for .i686

* Mon Jan 23 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-4
- complete renamed gsd to msd
- added fedora patches 

* Mon Jan 23 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- move /usr/libexec/mate back to /usr/libexec to avoid mdm login error
- gsd-locate-pointer and gsd-datetime-mechanism stay in /usr/libexec/mate
- hope that's work!

* Mon Jan 23 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- move /usr/libexec to /usr/libexec/mate to avoid conflicts with gnome-setting-daemon
- add support for gstreamer/alsa/oss instead of pulse for media-keys from git upstream

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-settings-daemon.spec based on gnome-settings-daemon-2.32.1-1.fc14 spec

* Mon Nov 15 2010 Bastien Nocera <bnocera@redhat.com> 2.32.1-1
- Update to 2.32.1

