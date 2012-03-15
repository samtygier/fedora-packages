%define dbus_version            0.90

Summary: 	Desktop Mate Notification Daemon
Name: 		mate-notification-daemon
Version: 	1.2.0
Release: 	1%{?dist}
URL: 		http://mate-desktop.org
Source0: 	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
License: 	GPLv2+
Group: 		System Environment/Libraries
Provides: 	desktop-notification-daemon

BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: libmatenotify-devel
BuildRequires: libcanberra-devel
BuildRequires: intltool
BuildRequires: mate-common
BuildRequires: mate-conf-devel
BuildRequires: libwnck-devel

Provides: mate-notification-daemon
Provides: mate-notification-daemon-engine-slider = %{version}-%{release}

%description
mate-notification-daemon is the server implementation of the freedesktop.org
desktop notification specification. Notifications can be used to inform
the user about an event or display some form of information without getting
in the user's way.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
	--disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/mate-notification-daemon.schemas \
	> /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/mate-notification-daemon.schemas \
	> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/mate-notification-daemon.schemas \
	> /dev/null || :
fi



%files -f %{name}.lang
%doc COPYING AUTHORS NEWS

%{_libexecdir}/mate-notification-daemon
%{_datadir}/applications/mate-notification-properties.desktop
%{_sysconfdir}/mateconf/schemas/mate-notification-daemon.schemas
%{_bindir}/mate-notification-properties
%{_libdir}/mate-notification-daemon/engines/*
%{_datadir}/dbus-1/services/org.freedesktop.mate.Notifications.service
%{_datadir}/icons/hicolor/*
%{_datadir}/mate-notification-daemon/mate-notification-properties.ui


%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Fri Mar 02 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- fix mock build error

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- fixed scriplet error
- rebuild for enable builds for .i686

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-notification-daemon.spec based on notification-daemon-0.7.3-2.fc17 spec

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for glibc bug#747377

