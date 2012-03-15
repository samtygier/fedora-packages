%define gettext_package mate-panel-2.0

%define mate_desktop_version 1.1.0
%define glib2_version 2.25.12
%define gtk2_version 2.11.3
%define libmate_version 1.1.2
%define libmateui_version 1.1.2
%define libmatecomponentui_version 1.1.1
%define mate_cobra_version 1.1.0
%define libwnck_version 2.19.5
%define mate_conf_version 1.1.0
%define mate_menus_version 1.1.1
%define cairo_version 1.0.0
%define dbus_version 0.60
%define dbus_glib_version 0.60
%define mate_doc_utils_version 1.1.0
%define libmateweather_version 1.1.0
%define evolution_data_server_version 1.9.1

%define use_evolution_data_server 0


Summary: 			MATE panel
Name: 				mate-panel
Version: 			1.2.1
Release: 			1%{?dist}
URL: 				http://pub.mate-desktop.org
Source0: 			http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
Source3: 			redhat-panel-default-setup.entries
Source4: 			gnome-compiler-flags.m4
Source5: 			redhat-panel-backwards-compat-config.schemas
Source6: 			add-translations.sh
License: 			GPLv2+ and LGPLv2+ and GFDL
Group: 				User Interface/Desktops

Requires: 			mate-desktop >= %{mate_desktop_version}
Requires: 			libwnck >= %{libwnck_version}
Requires: 			mate-menus >= %{mate_menus_version}
%if %{use_evolution_data_server}
Requires: evolution-data-server >= %{evolution_data_server_version}
%endif
Requires: 			mate-session-xsession
Requires: 			%{name}-libs = %{version}-%{release}

Requires(post): 	mate-conf >= %{mate_conf_version}
Requires(post): 	hicolor-icon-theme
Requires(pre): 		mate-conf >= %{mate_conf_version}
Requires(preun): 	mate-conf >= %{mate_conf_version}

BuildRequires: 		libxml2-python
BuildRequires: 		intltool
BuildRequires: 		gettext
BuildRequires: 		automake
BuildRequires: 		autoconf
BuildRequires: 		libtool
BuildRequires: 		scrollkeeper
BuildRequires: 		libxslt
BuildRequires: 		libX11-devel
BuildRequires: 		libXt-devel
BuildRequires: 		mate-desktop-devel >= %{mate_desktop_version}
BuildRequires: 		glib2-devel >= %{glib2_version}
BuildRequires: 		gtk2-devel >= %{gtk2_version}
BuildRequires: 		libmate-devel >= %{libmate_version}
BuildRequires: 		libmateui-devel >= %{libmateui_version}
BuildRequires: 		libmatecomponentui-devel >= %{libmatecomponentui_version}
BuildRequires: 		libwnck-devel >= %{libwnck_version}
BuildRequires: 		mate-conf-devel >= %{mate_conf_version}
BuildRequires: 		mate-menus-devel >= %{mate_menus_version}
BuildRequires: 		cairo-devel >= %{cairo_version}
BuildRequires: 		mate-doc-utils >= %{mate_doc_utils_version}
BuildRequires: 		dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: 		gtk-doc
BuildRequires: 		pango-devel
BuildRequires: 		libmatecomponent-devel
BuildRequires: 		libXau-devel
BuildRequires: 		libXrandr-devel
BuildRequires: 		polkit-devel >= 0.92
BuildRequires: 		libmateweather-devel >= %{libmateweather_version}
BuildRequires: 		librsvg2-devel
BuildRequires:    	NetworkManager-devel
BuildRequires: 		intltool
BuildRequires: 		gettext-devel
BuildRequires: 		libtool
BuildRequires: 		libcanberra-devel
%if %{use_evolution_data_server}
BuildRequires:		evolution-data-server-devel >= %{evolution_data_server_version}
BuildRequires: 		mate-corba-devel >= %{mate_corba_version}}
BuildRequires:		dbus-devel >= %{dbus_version}
%endif

BuildRequires: 		mate-common
BuildRequires: 		gobject-introspection-devel

Patch0: gnome-panel-vendor.patch
Patch1: gnome-panel-2.10.1-speak-to-us-ye-old-wise-fish.patch
Patch2: gnome-panel-search.patch
Patch3: gnome-panel-about.patch

# the next three patches belong together
# http://bugzilla.gnome.org/show_bug.cgi?id=470966
Patch8: launcher-desktop-files.patch
Patch9: desktop-file-monitoring.patch
Patch10: preferred-apps.patch

# don't pop up an error dialog if an applet from the
# default configuration is missing; we don't want to
# add a hard dependency on e.g. tomboy
Patch11: applet-error.patch

# http://bugzilla.gnome.org/show_bug.cgi?id=520111
Patch24: gnome-panel-2.21.92-allow-spurious-view-done-signals.patch

# http://bugzilla.gnome.org/show_bug.cgi?id=579092
Patch38: clock-network.patch

Patch40: clock-home.patch

# http://bugzilla.gnome.org/show_bug.cgi?id=343436
Patch43: panel-padding.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=537798
Patch47: fix-clock-crash.patch

Patch49: mate-panel_rest_of_fedora_patches.patch

%description
The MATE panel provides the window list, workspace switcher, menus, and other
features for the MATE desktop.

%package libs
Summary: Libraries for Panel Applets
License: LGPLv2+
Group: Development/Libraries

%description libs
This package contains the libpanel-applet library that
is needed by Panel Applets.

%package devel
Summary: 	Headers and libraries for Panel Applet development
License: 	LGPLv2+
Group: 		Development/Libraries
Requires: 	%{name}-libs = %{version}-%{release}
Requires: 	gtk2-devel >= %{gtk2_version}
Requires: 	libmatecomponentui-devel >= %{libmatecomponentui_version}
Requires: 	libmateui-devel >= %{libmateui_version}

%description devel
Panel Applet development package. Contains files needed for developing
Panel Applets using the libpanel-applet library.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1 -b .vendor
%patch1 -p1 -b .speak-to-us-ye-old-wise-fish
%patch2 -p1 -b .search
%patch3 -p1 -b .about
%patch8 -p1 -b .launcher-desktop-files
%patch9 -p1 -b .desktop-file-monitoring
%patch10 -p1 -b .preferred-apps
%patch11 -p1 -b .applet-error
%patch24 -p1 -b .allow-spurious-view-done-signals
%patch38 -p1 -b .clock-network
%patch40 -p1 -b .clock-home
%patch43 -p1 -b .panel-padding
%patch47 -p1 -b .fix-clock-crash
%patch49 -p1 -b .mate-panel_rest_of_fedora_patches.patch

cp -f %{SOURCE3} mate-panel/panel-default-setup.entries
cp -f %{SOURCE4} m4
cp -f %{SOURCE5} mate-panel/panel-compatibility.schemas
NOCONFIGURE=1 ./autogen.sh


%build

%configure \
	--disable-static \
	--with-in-process-applets=all \
	--enable-matecomponent \
	--disable-scrollkeeper \
	--enable-gtk-doc \
	--enable-network-manager \
%if %{use_evolution_data_server}
   --enable-eds=yes
%else
   --enable-eds=no
%endif

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make V=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

#
# Create pager and tasklist schemas for compatibility with older
# configurations which reference the old schema names
#
sed -e 's|/schemas/apps/window_list_applet/prefs/|/schemas/apps/tasklist_applet/prefs/|' $RPM_BUILD_ROOT%{_sysconfdir}/mateconf/schemas/window-list.schemas > $RPM_BUILD_ROOT%{_sysconfdir}/mateconf/schemas/tasklist.schemas
sed -e 's|/schemas/apps/workspace_switcher_applet/prefs/|/schemas/apps/pager_applet/prefs/|; s|<default>1</default>|<default>2</default>|' $RPM_BUILD_ROOT%{_sysconfdir}/mateconf/schemas/workspace-switcher.schemas > $RPM_BUILD_ROOT%{_sysconfdir}/mateconf/schemas/pager.schemas

## blow away stuff we don't want
rm -rf $RPM_BUILD_ROOT/var/scrollkeeper
rm -f $RPM_BUILD_ROOT%{_libdir}/libmate-panel-applet-2.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/libmate-panel-applet-3.*a


%find_lang %{gettext_package} --all-name

%post
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`

#
# Clear out the old defaults
#
mateconftool-2 --direct --config-source=$MATECONF_CONFIG_SOURCE --recursive-unset /apps/panel > /dev/null || :
mateconftool-2 --direct --config-source=$MATECONF_CONFIG_SOURCE --recursive-unset /schemas/apps/panel > /dev/null || :

#
# Install the schemas
#
mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/clock.schemas \
	%{_sysconfdir}/mateconf/schemas/fish.schemas \
	%{_sysconfdir}/mateconf/schemas/pager.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-compatibility.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-general.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-global.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-object.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-toplevel.schemas \
	%{_sysconfdir}/mateconf/schemas/tasklist.schemas \
	%{_sysconfdir}/mateconf/schemas/window-list.schemas \
	%{_sysconfdir}/mateconf/schemas/workspace-switcher.schemas \
  > /dev/null || :

#
# Install the default setup into /apps/panel and /apps/panel/default_setup
#
mateconftool-2 --direct --config-source=$MATECONF_CONFIG_SOURCE --load %{_sysconfdir}/mateconf/schemas/panel-default-setup.entries > /dev/null || :
mateconftool-2 --direct --config-source=$MATECONF_CONFIG_SOURCE --load %{_sysconfdir}/mateconf/schemas/panel-default-setup.entries /apps/panel > /dev/null || :

/sbin/ldconfig

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/clock.schemas \
	%{_sysconfdir}/mateconf/schemas/fish.schemas \
	%{_sysconfdir}/mateconf/schemas/pager.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-compatibility.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-general.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-global.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-object.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-toplevel.schemas \
	%{_sysconfdir}/mateconf/schemas/tasklist.schemas \
	%{_sysconfdir}/mateconf/schemas/window-list.schemas \
	%{_sysconfdir}/mateconf/schemas/workspace-switcher.schemas \
  > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/clock.schemas \
	%{_sysconfdir}/mateconf/schemas/fish.schemas \
	%{_sysconfdir}/mateconf/schemas/pager.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-compatibility.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-general.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-global.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-object.schemas \
	%{_sysconfdir}/mateconf/schemas/panel-toplevel.schemas \
	%{_sysconfdir}/mateconf/schemas/tasklist.schemas \
	%{_sysconfdir}/mateconf/schemas/window-list.schemas \
	%{_sysconfdir}/mateconf/schemas/workspace-switcher.schemas \
  > /dev/null || :
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache -q %{_datadir}/icons/hicolor >&/dev/null || :

%files -f %{gettext_package}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING.LIB COPYING-DOCS NEWS README
%{_datadir}/icons/hicolor/16x16/apps/*
%{_datadir}/icons/hicolor/22x22/apps/*
%{_datadir}/icons/hicolor/24x24/apps/*
%{_datadir}/icons/hicolor/32x32/apps/*
%{_datadir}/icons/hicolor/48x48/apps/*
%{_datadir}/icons/hicolor/scalable/apps/*
%{_datadir}/mate-panel
%exclude %{_datadir}/mate-panelrc
%{_datadir}/idl/mate-panel-2.0
%{_datadir}/mate-2.0/ui/*.xml
%{_datadir}/man/man*/*
%{_datadir}/applications/mate-panel.desktop
%{_bindir}/mate-panel
%{_bindir}/mate-desktop-item-edit
%{_libexecdir}/*
%{_sysconfdir}/mateconf/schemas/*.schemas
%{_sysconfdir}/mateconf/schemas/*.entries
%{_libdir}/mate-panel
%{_libdir}/girepository-1.0/MatePanelApplet-3.0.typelib
%{_datadir}/mate/help/*
%{_datadir}/omf/*

%files libs
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_bindir}/mate-panel-test-applets
%{_bindir}/panel-test-applets-matecomponent
%{_libdir}/pkgconfig/*
%{_includedir}/mate-panel-3.0/libmate-panel-applet/*
%{_includedir}/panel-2.0
%{_libdir}/*.so
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/MatePanelApplet-3.0.gir


%changelog
* Tue Mar 13 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
- update to version 1.2.1

* Wed Feb 29 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-5
- add BuildRequires: gobject-introspection-devel instead of
- mate-panel_fix_mock-build.patch

* Wed Feb 29 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-4
- insert rest of fedora patches
- fixed prefered webbrowser and mailclient icon
- fixed mock build error

* Sun Feb 19 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-3
- rebuild for enable builds for .i686

* Thu Jan 19 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-2
- insert some fedora patches
- enable NetworkManager

* Thu Jan 19 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-1
- update to version 1.1.1

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-file-manager.spec based on gnome-panel-2.32.0.2-2.fc14 spec

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0.2-1
- Update to 2.32.0.2

