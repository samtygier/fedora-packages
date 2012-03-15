%define glib2_version 2.15.3
%define pango_version 1.2.0
%define gtk2_version 2.6.0
%define libmate_version 1.1.2
%define libmateui_version 1.1.2
%define libglade_version 2.4.0
%define mate_panel_version 1.1.0
%define libgtop2_version 2.12.0
%define gail_version 1.2.0
%define libmatecomponentui_version 1.1.0
%define gstreamer_version 0.10.14
%define gstreamer_plugins_version 0.10.14
%define gstreamer_plugins_good_version 0.10.6
%define libxklavier_version 4.0
%define libwnck_version 2.9.3
%define mate_desktop_version 1.1.0
%define mate_utils_version 1.1.0
%define dbus_version 0.90
%define dbus_glib_version 0.70
%define libmatenotify_version 1.1.0
%define pygobject_version 2.6
%define pygtk_version 2.6
%define mate_python2_version 1.1.0
%define mate_conf_version 1.1.0
%define libmatekbd_version 1.1.0
%define mate_polkit_version 1.1.0

%define po_package mate-applets-2.0

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define build_stickynotes 0

Summary:        Small applications for the MATE panel
Name:			mate-applets
Version:		1.2.0
Release:        1%{?dist}
License:		GPLv2+ and GFDL
Group:          User Interface/Desktops
URL:			http://pub.mate-desktop.org
Source: 		http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
Patch51:        pymod-check.patch

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gtk2-devel >= %{gtk2_version}
BuildRequires:  libmateui-devel >= %{libmateui_version}
BuildRequires:  libmate-devel >= %{libmate_version}
BuildRequires:  mate-panel-devel >= %{mate_panel_version}
BuildRequires:  libglade2-devel >= %{libglade_version}
BuildRequires:  libgtop2-devel >= %{libgtop2_version}
BuildRequires:  pango-devel >= %{pango_version}
BuildRequires:  gail-devel >= %{gail_version}
BuildRequires:  libxklavier-devel >= %{libxklavier_version}
BuildRequires:  gstreamer-devel >= %{gstreamer_version}
BuildRequires:  gstreamer-plugins-base-devel >= %{gstreamer_plugins_version}
BuildRequires:  gstreamer-plugins-good-devel >= %{gstreamer_plugins_good_version}
BuildRequires:  libmatecomponentui-devel >= %{libmatecomponentui_version}
BuildRequires:  libwnck-devel >= %{libwnck_version}
BuildRequires:  mate-desktop-devel >= %{libmate_desktop_version}
BuildRequires:  mate-utils >= %{mate_utils_version}
BuildRequires:  libmatenotify-devel >= %{libmatenotify_version}
BuildRequires:  pygobject2-devel >= %{pygobject_version}
BuildRequires:  pygtk2-devel >= %{pygtk_version}
BuildRequires:  mate-python2-devel >= %{mate_python2_version}
BuildRequires:  mate-charmap-devel
BuildRequires:  dbus-devel >= %{dbus_version}
BuildRequires:  dbus-glib-devel >= %{dbus_glib_version}
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  mate-doc-utils
BuildRequires:  which
BuildRequires:  libtool autoconf gettext intltool
BuildRequires:  pkgconfig
BuildRequires:  mate-icon-theme
BuildRequires:  libmatekbd-devel >= %{libmatekbd_version}
BuildRequires:  libxslt
BuildRequires:  mate-polkit-devel >= %{mate_polkit_version}
BuildRequires:  libmateweather-devel >= 1.1.0
BuildRequires:  mate-common
BuildRequires:  xorg-x11-server-utils
BuildRequires:  scrollkeeper

Requires:		mate-panel >= %{mate_panel_version}
Requires:		libxklavier >= %{libxklavier_version}
Requires:		gstreamer-plugins-base >= %{gstreamer_plugins_version}
Requires:		gstreamer-plugins-good >= %{gstreamer_plugins_good_version}
Requires:		dbus >= %{dbus_version}

Requires(pre): mate-conf >= %{mate_conf_version}
Requires(preun): mate-conf >= %{mate_conf_version}
Requires(post): mate-conf >= %{mate_conf_version}

# since we are installing .pc files
Requires:	pkgconfig

%description
The mate-applets package contains small applications which generally
run in the background and display their output to the MATE  panel.
It includes a clock, a character palette, load monitors, little toys,
and more.

%prep
%setup -q
%patch51 -p1 -b .pymod
NOCONFIGURE=1 ./autogen.sh

%build
export DISPLAY=:0.0
xhost +

%configure \
	--disable-scrollkeeper    \
	--disable-static          \
	--disable-scrollkeeper 	\
	--enable-mixer-applet \
	--enable-polkit \
	--enable-ipv6 \
	--disable-cpufreq

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make

%install
rm -rf $RPM_BUILD_ROOT
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# save space by linking identical images in translated docs
for helpdir in $RPM_BUILD_ROOT%{_datadir}/mate/help/*; do
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
done

%find_lang %{po_package} --all-name

# Clean up unpackaged files
rm -rf $RPM_BUILD_ROOT%{_localstatedir}/scrollkeeper

# drop non-XKB support files
rm -rf $RPM_BUILD_ROOT%{_datadir}/xmodmap


%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
touch --no-create %{_datadir}/icons/mate
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/mate
fi

export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
mateconftool-2 --makefile-install-rule                                        \
	    %{_sysconfdir}/mateconf/schemas/battstat.schemas                  \
	    %{_sysconfdir}/mateconf/schemas/charpick.schemas                  \
	    %{_sysconfdir}/mateconf/schemas/drivemount.schemas                \
	    %{_sysconfdir}/mateconf/schemas/geyes.schemas                     \
	    %{_sysconfdir}/mateconf/schemas/mixer.schemas            \
%if %{build_stickynotes}
	    %{_sysconfdir}/mateconf/schemas/stickynotes.schemas               \
%endif
	    %{_sysconfdir}/mateconf/schemas/multiload.schemas \
		>& /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule                                    \
	    %{_sysconfdir}/mateconf/schemas/battstat.schemas                  \
	    %{_sysconfdir}/mateconf/schemas/charpick.schemas                  \
	    %{_sysconfdir}/mateconf/schemas/drivemount.schemas                \
	    %{_sysconfdir}/mateconf/schemas/geyes.schemas                     \
	    %{_sysconfdir}/mateconf/schemas/mixer.schemas            \
%if %{build_stickynotes}
	    %{_sysconfdir}/mateconf/schemas/stickynotes.schemas               \
%endif
	    %{_sysconfdir}/mateconf/schemas/multiload.schemas >& /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule                                    \
	    %{_sysconfdir}/mateconf/schemas/battstat.schemas                  \
	    %{_sysconfdir}/mateconf/schemas/charpick.schemas                  \
	    %{_sysconfdir}/mateconf/schemas/drivemount.schemas                \
	    %{_sysconfdir}/mateconf/schemas/geyes.schemas                     \
	    %{_sysconfdir}/mateconf/schemas/mixer.schemas            \
%if %{build_stickynotes}
	    %{_sysconfdir}/mateconf/schemas/stickynotes.schemas               \
%endif
	    %{_sysconfdir}/mateconf/schemas/multiload.schemas >& /dev/null || :
fi

%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
touch --no-create %{_datadir}/icons/mate
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/mate
fi

%files -f %{po_package}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README
%{_bindir}/mate-invest-chart
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/16x16/apps/*
%{_datadir}/icons/hicolor/22x22/apps/*
%{_datadir}/icons/hicolor/24x24/apps/*
%{_datadir}/icons/hicolor/32x32/apps/*
%{_datadir}/icons/hicolor/48x48/apps/*
%{_datadir}/icons/hicolor/scalable/apps/*
%{_datadir}/icons/mate/*
%{_datadir}/mate-2.0/ui/*
%{_datadir}/mate-applets
%{_libdir}/matecomponent/servers/*
%{_libexecdir}/accessx-status-applet
%{_libexecdir}/charpick_applet2
%{_libexecdir}/drivemount_applet2
%{_libexecdir}/geyes_applet2
#%{_libexecdir}/mate-applets/
%{_libexecdir}/mateweather-applet-2
#%{_libexecdir}/mini_commander_applet
%{_libexecdir}/multiload-applet-2
%{_libexecdir}/null_applet
%{_libexecdir}/battstat-applet-2
%{_libexecdir}/mixer_applet2
%{_libexecdir}/stickynotes_applet
%{_libexecdir}/trashapplet
%{_libexecdir}/invest-applet
%{_sysconfdir}/mateconf/schemas/*
%{_sysconfdir}/sound/events/mate-battstat_applet.soundlist
%{_datadir}/dbus-1/services/*
%{_datadir}/mate-panel/applets/*
%{_datadir}/mate/help/*
%{_datadir}/omf/*
%{python_sitelib}/mate_invest/



%changelog
* Sun Mar 11 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.3-4
- rebuild for enable builds for .i686
- disable mini-commander because it doesn't work
- switch from mate-character-map to mate-charmap

* Thu Feb 02 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.3-3
- fix mate python applets

* Sat Jan 27 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.3-2
- correct mateconf files installation

* Fri Jan 26 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.3-1
- update to version 1.1.3
- change invest-applet to mate_invest

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-1
- update to version 1.1.1
- enable invest-applet

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mateapplets.spec based on gnome-applets-2.32.0-3.fc14 spec

* Mon Jan 03 2011 Adam Williamson <awilliam@redhat.com> - 1:2.32.0-3
- fix invest applet display (RH #631912, upstream #631418)

