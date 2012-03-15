Name:		mate-bluetooth
Version:	1.2.0
Release:	1%{?dist}
Summary:	Bluetooth graphical utilities

Group:		Applications/Communications
License:	GPLv2+
URL:		http://pub.mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
Source1:	61-mate-bluetooth-rfkill.rules

BuildRequires:	mate-conf-devel
BuildRequires:	gtk2-devel
BuildRequires:	unique-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	libnotify-devel
BuildRequires:	libmx-devel
BuildRequires:	mate-doc-utils rarian-compat
BuildRequires:	caja-sendto-devel
BuildRequires:  libmatenotify-devel

BuildRequires:	intltool desktop-file-utils gettext gtk-doc libtool mate-common

BuildRequires:	gobject-introspection-devel

Provides:	dbus-bluez-pin-helper

# Otherwise we might end up with mismatching version
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gvfs-obexftp
Requires:	bluez >= 4.42
Requires:	obexd
Requires:	mate-notification-daemon
#Requires:	pulseaudio-module-bluetooth
Requires:	mate-control-center

Requires(post):		desktop-file-utils
Requires(postun):	desktop-file-utils

%description
The mate-bluetooth package contains graphical utilities to setup,
monitor and use Bluetooth devices.

%package libs
Summary:	GTK+ Bluetooth device selection widgets
Group:		System Environment/Libraries
License:	LGPLv2+
Requires:	gobject-introspection

%description libs
This package contains libraries needed for applications that
want to display a Bluetooth device selection widget.

%package libs-devel
Summary:	Development files for %{name}-libs
Group:		Development/Libraries
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk-doc pkgconfig gobject-introspection-devel
Provides:	mate-bluetooth-devel = %{version}

%description libs-devel
This package contains the libraries and header files that are needed
for writing applications that require a Bluetooth device selection widget.

#%package moblin
#Summary:	Moblin Bluetooth management utility
#Group:		Development/Libraries
#License:	LGPLv2+
#Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

#%description moblin
#This package contains the Moblin user interface for gnome-bluetooth.

%prep
%setup -q

libtoolize  -fi
glib-gettextize -f
intltoolize -f
gtkdocize
mate-doc-common
mate-doc-prepare -f
aclocal --force
autoheader -f
automake --add-missing --copy
autoconf -f

%build
%configure \
	--disable-desktop-update \
	--disable-icon-update \
	--enable-caja-sendto=yes \
	--disable-schemas-compile \
	--enable-gtk-doc

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export MATEGCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/libmate-bluetooth.la \
	   $RPM_BUILD_ROOT/%{_libdir}/mate-bluetooth/plugins/*.la \
	   $RPM_BUILD_ROOT/%{_libdir}/caja-sendto/plugins/*.la \
	   $RPM_BUILD_ROOT/%{_libdir}/control-center-1/panels/libbluetooth.la

#desktop-file-install --vendor=""				\
#	--delete-original					\
#	--dir=$RPM_BUILD_ROOT%{_datadir}/applications		\
#	$RPM_BUILD_ROOT%{_datadir}/applications/bluetooth-properties.desktop

#desktop-file-install --vendor=""				\
#	--delete-original					\
#	--dir=$RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/	\
#	$RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/bluetooth-applet.desktop

install -m0644 -D %{SOURCE1} $RPM_BUILD_ROOT/lib/udev/rules.d/61-mate-bluetooth-rfkill.rules

# mate-bluetooth2 is the name for the gettext domain,
# mate-bluetooth is the name in the docs
%find_lang mate-bluetooth
%find_lang %{name} --all-name
#cat %{name}.lang >> mate-bluetooth.lang

# save space by linking identical images in translated docs
helpdir=$RPM_BUILD_ROOT%{_datadir}/mate/help/%{name}
for f in $helpdir/C/figures/*.png; do
  b="$(basename $f)"
  for d in $helpdir/*; do
    if [ -d "$d" -a "$d" != "$helpdir/C" ]; then
      g="$d/figures/$b"
      if [ -f "$g" ]; then
        if cmp -s $f $g; then
          rm "$g"; ln -s "../../C/figures/$b" "$g"
        fi
      fi
    fi
  done
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database -q

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas || :

%pre
if [ "$1" -gt 1 ]; then
	export MATEGCONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	if [ -f %{_sysconfdir}/mateconf/schemas/mate-obex-server.schemas ] ; then
		mateconftool-2 --makefile-uninstall-rule \
		%{_sysconfdir}/gconf/matechemas/mate-obex-server.schemas >/dev/null || :
	fi
	if [ -f %{_sysconfdir}/mateconf/schemas/bluetooth-manager.schemas ] ; then
		mateconftool-2 --makefile-uninstall-rule 				\
		%{_sysconfdir}/mateconf/schemas/bluetooth-manager.schemas		\
		>& /dev/null || :
	fi
fi

%preun
if [ "$1" -eq 0 ]; then
	export MATEGCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
	if [ -f %{_sysconfdir}/mateconf/schemas/mate-obex-server.schemas ] ; then
		gconftool-2 --makefile-uninstall-rule \
		%{_sysconfdir}/mateconf/schemas/mate-obex-server.schemas > /dev/null || :
	fi
	if [ -f %{_sysconfdir}/mateconf/schemas/bluetooth-manager.schemas ] ; then
		mateconftool-2 --makefile-uninstall-rule 				\
		%{_sysconfdir}/mateconf/schemas/bluetooth-manager.schemas		\
		>& /dev/null || :
	fi
fi

%postun
update-desktop-database -q
glib-compile-schemas %{_datadir}/glib-2.0/schemas || :
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/mate &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/mate &>/dev/null || :
fi

%post libs
/sbin/ldconfig
touch --no-create %{_datadir}/icons/mate &>/dev/null || :

%posttrans libs
gtk-update-icon-cache %{_datadir}/icons/mate &>/dev/null || :

%postun libs
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/mate &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/mate &>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc README NEWS COPYING
%{_sysconfdir}/xdg/autostart/mate-bluetooth-applet.desktop
%{_bindir}/mate-bluetooth-applet
%{_bindir}/mate-bluetooth-sendto
%{_bindir}/mate-bluetooth-wizard
%{_bindir}/mate-bluetooth-properties
%{_libdir}/mate-bluetooth/
%{_datadir}/applications/*.desktop
%{_datadir}/mate-bluetooth/
%{_mandir}/man1/*
%{_libdir}/caja-sendto/plugins/*.so
/lib/udev/rules.d/61-mate-bluetooth-rfkill.rules
%{_datadir}/MateConf/gsettings/*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/mate/help/mate-bluetooth/
%{_datadir}/omf/mate-bluetooth/

%files -f mate-bluetooth.lang libs
%defattr(-,root,root,-)
%doc COPYING.LIB
%{_libdir}/libmate-bluetooth.so.*
%{_libdir}/girepository-1.0/MateBluetooth-1.0.typelib
%{_datadir}/icons/mate/*/apps/*
%{_datadir}/icons/mate/*/status/*

%files libs-devel
%defattr(-,root,root,-)
%{_includedir}/mate-bluetooth/
%{_libdir}/libmate-bluetooth.so
%{_libdir}/pkgconfig/mate-bluetooth-1.0.pc
%{_datadir}/gir-1.0/MateBluetooth-1.0.gir
%{_datadir}/gtk-doc/html/mate-bluetooth/

#%files moblin
#%defattr(-,root,root,-)
#%{_sysconfdir}/xdg/autostart/bluetooth-panel.desktop
#%{_datadir}/dbus-1/services/org.moblin.UX.Shell.Panels.bluetooth.service
#%{_bindir}/bluetooth-panel
#%{_datadir}/mutter-moblin/panels/bluetooth-panel.desktop

%changelog
* Thu Mar 15 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- correct icon path for gtk-update-icon-cache command in spec file

* Tue Jan 31 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-bluetooth.spec based on gnome-bluetooth-2.31.6-4.fc14 spec

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> 2.31.6-4
- Rebuild against nautilus-sendto

