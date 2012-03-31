%define gettext_package mate-control-center-2.0

%define glib2_version 2.13.0
%define gtk2_version 2.21
%define mate_conf_version 1.1.0
%define mate_desktop_version 1.1.0
%define desktop_file_utils_version 0.9
%define xft_version 2.1.7
%define fontconfig_version 1.0.0
%define redhat_menus_version 1.8
%define marco_version 1.1.0
%define libxklavier_version 4.0
%define mate_menus_version 1.1.1
%define usermode_version 1.83
%define libmatekbd_version 1.1.0
%define libXrandr_version 1.2.99

Summary: 	Utilities to configure the Mate desktop
Name: 		mate-control-center
Version: 	1.2.1
Release: 	1%{?dist}
License: 	GPLv2+ and GFDL
Group: 		User Interface/Desktops
Source: 	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
URL: 		http://mate-desktop.org

Patch0: mate-control-center_add_audacious_to_default-applications.patch
Patch1: mate-control-center_add_videoplayers_to_default-applications.patch

Requires: mate-settings-daemon >= 1.1.0
Requires: redhat-menus >= %{redhat_menus_version}
Requires: mate-icon-theme
Requires: alsa-lib
Requires: mate-menus >= %{mate_menus_version}
Requires: mate-desktop >= %{mate_desktop_version}
Requires: dbus-x11
Requires: mate-control-center-filesystem = %{version}-%{release}
# we need XRRGetScreenResourcesCurrent
Requires: libXrandr >= %{libXrandr_version}

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: librsvg2-devel
BuildRequires: mate-conf-devel >= %{mate_conf_version}
BuildRequires: mate-desktop-devel >= %{mate_desktop_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: libxklavier-devel >= %{libxklavier_version}
BuildRequires: libXcursor-devel
BuildRequires: libXrandr-devel >= %{libXrandr_version}
BuildRequires: gettext
BuildRequires: mate-menus-devel >= %{mate_menus_version}
BuildRequires: libmatekbd-devel >= %{libmatekbd_version}
BuildRequires: mate-settings-daemon-devel
BuildRequires: intltool >= 0.37.1
BuildRequires: libXxf86misc-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: mate-doc-utils
BuildRequires: libglade2-devel
BuildRequires: libxml2-devel
BuildRequires: dbus-devel >= 0.90
BuildRequires: dbus-glib-devel >= 0.70
BuildRequires: scrollkeeper
BuildRequires: libcanberra-devel
BuildRequires: unique-devel
BuildRequires: marco-devel
BuildRequires: mate-common

Requires(preun): mate-conf
Requires(pre): mate-conf
Requires(post): mate-conf
Requires(post): desktop-file-utils >= %{desktop_file_utils_version}
Requires(post): shared-mime-info
Requires(postun): desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun): shared-mime-info

Provides: mate-control-center-extra = %{version}-%{release}

%description
This package contains configuration utilities for the MATE desktop, which
allow to configure accessibility options, desktop fonts, keyboard and mouse
properties, sound setup, desktop theme and background, user interface
properties, screen resolution, and other settings.

%package devel
Summary: Development files for the MATE control-center
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Th control-center package contains configuration utilities for the
MATE desktop.

This package contains libraries and header files needed for integrating
configuration of applications such as window managers with the control-center
utilities.

%package filesystem
Summary: MATE Control Center directories
Group: Development/Libraries
# NOTE: this is an "inverse dep" subpackage. It gets pulled in
# NOTE: by the main package an MUST not depend on the main package

%description filesystem
The MATE control-center provides a number of extension points
for applications. This package contains directories where applications
can install configuration files that are picked up by the control-center
utilities.


%prep
%setup -q -n mate-control-center-%{version}
%patch0 -p1 -b .mate-control-center_add_audacious_to_default-applications
%patch1 -p1 -b .mate-control-center_add_videoplayers_to_default-applications

NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-scrollkeeper    \
    --disable-static \
    --disable-update-mimedb

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}

%install
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

for i in apps_mate_settings_daemon_default_editor.schemas		\
	    apps_mate_settings_daemon_keybindings.schemas		\
	    apps_mate_settings_daemon_screensaver.schemas		\
	    desktop_mate_font_rendering.schemas ; do			\
	    rm -f $RPM_BUILD_ROOT%{_sysconfdir}/mateconf/schemas/$i ;	\
done

# we do want this
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mate/wm-properties

# we don't want these
#rm -rf $RPM_BUILD_ROOT%{_datadir}/mate/autostart
#rm -rf $RPM_BUILD_ROOT%{_datadir}/mate/cursor-fonts
rm $RPM_BUILD_ROOT%{_datadir}/applications/mimeinfo.cache

# remove useless libtool archive files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} \;

%find_lang %{gettext_package} --all-name

%post
/sbin/ldconfig
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/fontilus.schemas \
	%{_sysconfdir}/mateconf/schemas/mate-control-center.schemas \
	%{_sysconfdir}/mateconf/schemas/control-center.schemas \
	> /dev/null || :

update-desktop-database --quiet %{_datadir}/applications
update-mime-database %{_datadir}/mime > /dev/null
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/fontilus.schemas \
	%{_sysconfdir}/mateconf/schemas/mate-control-center.schemas \
	%{_sysconfdir}/mateconf/schemas/control-center.schemas \
	> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/fontilus.schemas \
	%{_sysconfdir}/mateconf/schemas/mate-control-center.schemas \
	%{_sysconfdir}/mateconf/schemas/control-center.schemas \
	> /dev/null || :
fi


%postun
/sbin/ldconfig
update-desktop-database --quiet %{_datadir}/applications
update-mime-database %{_datadir}/mime > /dev/null
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files -f %{gettext_package}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README
%{_datadir}/mate-control-center/keybindings/*.xml
%{_datadir}/mate-control-center/default-apps/*.xml
%{_datadir}/mate-control-center/ui
%{_datadir}/mate-control-center/pixmaps
%{_datadir}/applications/*.desktop
%{_datadir}/desktop-directories/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/polkit-1/actions/*
%{_datadir}/pkgconfig/mate-keybindings.pc
%{_datadir}/pkgconfig/mate-default-applications.pc
# list all binaries explicitly, so we notice if one goes missing
%{_bindir}/mate-at-mobility
%{_bindir}/mate-at-visual
%{_bindir}/mate-control-center
%{_bindir}/mate-typing-monitor
%{_bindir}/mate-font-viewer
%{_bindir}/mate-thumbnail-font
%{_bindir}/mate-appearance-properties
%{_bindir}/mate-at-properties
%{_bindir}/mate-default-applications-properties
%{_bindir}/mate-display-properties
%{_bindir}/mate-keybinding-properties
%{_bindir}/mate-keyboard-properties
%{_bindir}/mate-mouse-properties
%{_bindir}/mate-network-properties
%{_bindir}/mate-window-properties
%{_libdir}/*.so.*
%{_sysconfdir}/mateconf/schemas/control-center.schemas
%{_sysconfdir}/mateconf/schemas/mate-control-center.schemas
%{_sysconfdir}/mateconf/schemas/fontilus.schemas
%{_sysconfdir}/xdg/menus/matecc.menu
%{_sysconfdir}/xdg/autostart/mate-at-session.desktop
%{_libdir}/window-manager-settings
%{_sbindir}/mate-display-properties-install-systemwide
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/mate/cursor-fonts/*
%{_datadir}/mate/help/mate-control-center/*/*.xml
%{_datadir}/omf/mate-control-center/*.omf

%files devel
%defattr(-,root,root)
%{_includedir}/mate-window-settings-2.0
%{_libdir}/libmate-window-settings.so
%{_libdir}/pkgconfig/*

%files filesystem
%defattr(-,root,root)
%dir %{_datadir}/mate/wm-properties
%dir %{_datadir}/mate-control-center
%dir %{_datadir}/mate-control-center/keybindings
%dir %{_datadir}/mate-control-center/default-apps


%changelog
* Tue Mar 27 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
- update to 1.2.1

* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Mon Mar 05 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- add default applications

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-control-center.spec based on control-center-2.32.0-1.fc14 spec

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

