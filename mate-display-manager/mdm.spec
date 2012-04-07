%define libauditver 1.0.6
%define DBUS_GLIB_REQUIRED_VERSION 0.74
%define GLIB_REQUIRED_VERSION 2.22.0
%define MATECONF_REQUIRED_VERSION 1.1.0
%define MATE_PANEL_REQUIRED_VERSION 1.1.0
%define LIBCANBERRA_GTK_REQUIRED_VERSION 0.4
%define pango_version 1.3.0
%define gtk2_version 2.20.0
%define libglade2_version 2.0.0
%define libmateui_version 1.1.2
%define scrollkeeper_version 0.1.4
%define pam_version 0.99.8.1-11
%define desktop_file_utils_version 0.2.90
%define gail_version 1.2.0
%define nss_version 3.11.1
%define consolekit_version 0.3.0-9
%define fontconfig_version 2.5.0
%define _default_patch_fuzz 999

Summary: 	The MATE Display Manager
Name: 		mdm
Version: 	1.1.1
Release: 	6%{?dist}
License: 	GPLv2+
Group: 		User Interface/X
URL: 		https://github.com/mate-desktop/mate-display-manager
Source: 	%{name}-%{version}.tar.gz
Source1: mdm-pam
Source2: mdm-autologin-pam
Source3: mdm-password.pam
Source4: mdm-smartcard.pam
Source5: mdm-fingerprint.pam
Source6: mdm-smartcard-16.png
Source7: mdm-smartcard-48.png
Source8: mdm-fingerprint-16.png
Source9: mdm-fingerprint-48.png

Requires(pre): /usr/sbin/useradd

Requires: pam >= 0:%{pam_version}
Requires: /sbin/nologin
Requires: system-logos
Requires: xorg-x11-server-utils
Requires: setxkbmap
Requires: xorg-x11-xinit
Requires: ConsoleKit >= %{consolekit_version}
Requires: mate-settings-daemon >= 1.1.0
Requires: iso-codes
Requires: mate-session
Requires: mate-polkit
# since we use it, and pam spams the log if the module is missing
Requires: mate-keyring-pam
#Requires: plymouth-gdm-hooks
#Requires: pulseaudio-gdm-hooks
# We need 1.0.4-5 since it lets us use "localhost" in auth cookies
Requires: libXau >= 1.0.4-4
Requires: numlockx

BuildRequires: dbus-glib-devel >= %{DBUS_GLIB_REQUIRED_VERSION}
BuildRequires: glib-devel >= %{GLIB_REQUIRED_VERSION}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: pango-devel >= %{pango_version} 
BuildRequires: scrollkeeper >= %{scrollkeeper_version} 
BuildRequires: mate-conf-devel >= %{MATECONF_REQUIRED_VERSION} 
BuildRequires: mate-panel-devel >= %{MATE_PANEL_REQUIRED_VERSION}
BuildRequires: libxklavier-devel >= 4.0 
BuildRequires: libcanberra-gtk2 >= %{LIBCANBERRA_GTK_REQUIRED_VERSION} 
BuildRequires: fontconfig >= %{fontconfig_version} 
BuildRequires: upower-devel >= 0.9.0 
BuildRequires: pam-devel >= %{pam_version}
BuildRequires: libselinux-devel 
BuildRequires: libXdmcp-devel 
BuildRequires: ConsoleKit
BuildRequires: iso-codes-devel
BuildRequires: check-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: mate-doc-utils
BuildRequires: pkgconfig(libcanberra-gtk)
BuildRequires: libattr-devel
BuildRequires: mate-common
BuildRequires: nss-devel

%ifnarch s390 s390x ppc64
BuildRequires: xorg-x11-server-Xorg
%endif

BuildRequires: libmateui-devel >= %{libmateui_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}

Provides: service(graphical-login) = %{name}
Requires: audit-libs >= %{libauditver}
Requires: mate-accountsservice
Patch2: plymouth.patch

Patch96: gdm-multistack.patch
# Fedora-specific
Patch97: gdm-bubble-location.patch
Patch98: tray-padding.patch
Patch99: gdm-2.23.1-fedora-logo.patch

# change to mate-accountsservice
Patch101: mate-accountsservice-enable_1.patch
Patch102: mate-accountsservice-enable_2.patch

Patch103: mdm_first_background_patch.patch

#numlock
Patch104: mdm_numlock_on.patch

%package user-switch-applet
Summary:   MDM User Switcher Panel Applet
Group:     User Interface/Desktops
Requires:  mdm >= 1.1.0
Requires:  mate-accountsdialog

%package plugin-smartcard
Summary:   MDM smartcard plugin
Group:     User Interface/Desktops
Requires:  mdm >= 1.1.0
Requires:  pam_pkcs11

%package plugin-fingerprint
Summary:   MDM fingerprint plugin
Group:     User Interface/Desktops
Requires:  mdm >= 1.1.0
Requires:  fprintd-pam

%description
MDM provides the graphical login screen, shown shortly after boot up,
log out, and when user-switching.

%description user-switch-applet
The MDM user switcher applet provides a mechanism for changing among
multiple simulanteous logged in users.

%description plugin-smartcard
The MDM smartcard plugin provides functionality necessary to use a smart card with MDM.

%description plugin-fingerprint
The MDM fingerprint plugin provides functionality necessary to use a fingerprint reader with MDM.


%prep
%setup -q
%patch2 -p1 -b .plymouth
%patch96 -p1 -b .multistack
%patch97 -p1 -b .bubble-location
%patch98 -p1 -b .tray-padding
%patch99 -p1 -b .fedora-logo
%patch101 -p1 -b .mate-accountsservice-enable_1
%patch102 -p1 -b .mate-accountsservice-enable_2
%patch103 -p1 -b .mdm_first_background_patch
%patch104 -p1 -b .mdm_numlock_on
NOCONFIGURE=1 ./autogen.sh


%build
cp -f %{SOURCE1} data/mdm
cp -f %{SOURCE2} data/mdm-autologin
cp -f %{SOURCE3} gui/simple-greeter/plugins/password/mdm-password.pam
cp -f %{SOURCE4} gui/simple-greeter/plugins/smartcard/mdm-smartcard.pam
cp -f %{SOURCE5} gui/simple-greeter/plugins/fingerprint/mdm-fingerprint.pam
cp -f %{SOURCE6} gui/simple-greeter/plugins/smartcard/icons/16x16/mdm-smartcard.png
cp -f %{SOURCE7} gui/simple-greeter/plugins/smartcard/icons/48x48/mdm-smartcard.png
cp -f %{SOURCE8} gui/simple-greeter/plugins/fingerprint/icons/16x16/mdm-fingerprint.png
cp -f %{SOURCE9} gui/simple-greeter/plugins/fingerprint/icons/48x48/mdm-fingerprint.png

%configure \
	--disable-static \
	--enable-console-helper \
	--with-selinux \
	--with-pam-prefix=%{_sysconfdir} \
	--with-dbus-sys=%{_sysconfdir}/dbus-1/system.d/ \
	--disable-scrollkeeper  \
	--with-console-kit      \
	--enable-profiling

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}


%install

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# docs go elsewhere
rm -rf $RPM_BUILD_ROOT/%{_prefix}/doc

# create log dir
mkdir -p $RPM_BUILD_ROOT/var/log/mdm

# and a spool dir
mkdir -p $RPM_BUILD_ROOT/var/spool/mdm

# remove the mdm Xsession as we're using the xdm one
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/mdm/Xsession
(cd $RPM_BUILD_ROOT%{_sysconfdir}/mdm; ln -sf ../X11/xinit/Xsession .)

rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/mdm/greeter

rm -rf $RPM_BUILD_ROOT%{_localstatedir}/scrollkeeper

find $RPM_BUILD_ROOT -name '*.a' -delete
find $RPM_BUILD_ROOT -name '*.la' -delete

rm -f $RPM_BUILD_ROOT%{_includedir}/mdm/simple-greeter/mdm-greeter-extension.h
rm -f $RPM_BUILD_ROOT%{_libdir}/pkmateconfig/mdmsimplegreeter.pc

mv -v $RPM_BUILD_ROOT%{_datadir}/pixmaps/nobody.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/mate-nobody.png
mv -v $RPM_BUILD_ROOT%{_datadir}/pixmaps/nohost.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/mate-nohost.png

%find_lang mdm --all-name

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/mdm-simple-greeter.schemas \
	> /dev/null || :
fi

/usr/sbin/useradd -M -d /var/lib/mdm -s /sbin/nologin -r mdm > /dev/null 2>&1
/usr/sbin/usermod -d /var/lib/gdm -s /sbin/nologin gdm >/dev/null 2>&1
# ignore errors, as we can't disambiguate between mdm already existed
# and couldn't create account with the current adduser.
exit 0

%post
/sbin/ldconfig
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/mdm-simple-greeter.schemas \
	> /dev/null || :
touch --no-create /usr/share/icons/hicolor >&/dev/null || :

# if the user already has a config file, then migrate it to the new
# location; rpm will ensure that old file will be renamed

custom=/etc/mdm/custom.conf

if [ $1 -ge 2 ] ; then
    if [ -f /usr/share/mdm/config/mdm.conf-custom ]; then
        oldconffile=/usr/share/mdm/config/mdm.conf-custom
    elif [ -f /etc/X11/mdm/mdm.conf ]; then
        oldconffile=/etc/X11/mdm/mdm.conf
    fi

    # Comment out some entries from the custom config file that may
    # have changed locations in the update.  Also move various
    # elements to their new locations.

    [ -n "$oldconffile" ] && sed \
    -e 's@^command=/usr/X11R6/bin/X@#command=/usr/bin/Xorg@' \
    -e 's@^Xnest=/usr/X11R6/bin/Xnest@#Xnest=/usr/X11R6/bin/Xnest@' \
    -e 's@^BaseXsession=/etc/X11/xdm/Xsession@#BaseXsession=/etc/X11/xinit/Xsession@' \
    -e 's@^BaseXsession=/etc/X11/mdm/Xsession@#&@' \
    -e 's@^BaseXsession=/etc/mdm/Xsession@#&@' \
    -e 's@^Greeter=/usr/bin/mdmgreeter@#Greeter=/usr/libexec/mdmgreeter@' \
    -e 's@^RemoteGreeter=/usr/bin/mdmlogin@#RemoteGreeter=/usr/libexec/mdmlogin@' \
    -e 's@^GraphicalTheme=Bluecurve@#&@' \
    -e 's@^BackgroundColor=#20305a@#&@' \
    -e 's@^DefaultPath=/usr/local/bin:/usr/bin:/bin:/usr/X11R6/bin@#&@' \
    -e 's@^RootPath=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/X11R6/bin@#&@' \
    -e 's@^HostImageDir=/usr/share/hosts/@#HostImageDir=/usr/share/pixmaps/faces/@' \
    -e 's@^LogDir=/var/log/mdm@#&@' \
    -e 's@^PostLoginScriptDir=/etc/X11/mdm/PostLogin@#&@' \
    -e 's@^PreLoginScriptDir=/etc/X11/mdm/PreLogin@#&@' \
    -e 's@^PreSessionScriptDir=/etc/X11/mdm/PreSession@#&@' \
    -e 's@^PostSessionScriptDir=/etc/X11/mdm/PostSession@#&@' \
    -e 's@^DisplayInitDir=/var/run/mdm.pid@#&@' \
    -e 's@^RebootCommand=/sbin/reboot;/sbin/shutdown -r now;/usr/sbin/shutdown -r now;/usr/bin/reboot@#&@' \
    -e 's@^HaltCommand=/sbin/poweroff;/sbin/shutdown -h now;/usr/sbin/shutdown -h now;/usr/bin/poweroff@#&@' \
    -e 's@^ServAuthDir=/var/mdm@#&@' \
    -e 's@^Greeter=/usr/bin/mdmlogin@Greeter=/usr/libexec/mdmlogin@' \
    -e 's@^RemoteGreeter=/usr/bin/mdmgreeter@RemoteGreeter=/usr/libexec/mdmgreeter@' \
    $oldconffile > $custom
fi

if [ $1 -ge 2 -a -f $custom ] && grep -q /etc/X11/mdm $custom ; then
   sed -i -e 's@/etc/X11/mdm@/etc/mdm@g' $custom
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/mdm-simple-greeter.schemas \
	> /dev/null || :
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/ull || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/ull || :

%files -f mdm.lang
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README TODO
%dir %{_sysconfdir}/mdm
%config(noreplace) %{_sysconfdir}/mdm/custom.conf
%config %{_sysconfdir}/mdm/Init/*
%config %{_sysconfdir}/mdm/PostLogin/*
%config %{_sysconfdir}/mdm/PreSession/*
%config %{_sysconfdir}/mdm/PostSession/*
%config %{_sysconfdir}/pam.d/mdm
%config %{_sysconfdir}/pam.d/mdm-autologin
%config %{_sysconfdir}/pam.d/mdm-password
# not config files
%{_sysconfdir}/mdm/Xsession
%{_datadir}/mdm/mdm.schemas
%{_sysconfdir}/dbus-1/system.d/mdm.conf
%dir %{_sysconfdir}/mdm/Init
%dir %{_sysconfdir}/mdm/PreSession
%dir %{_sysconfdir}/mdm/PostSession
%dir %{_sysconfdir}/mdm/PostLogin
%{_datadir}/pixmaps/*.png
%dir %{_datadir}/pixmaps/faces
%{_datadir}/pixmaps/faces/*.png
%{_datadir}/pixmaps/faces/*.jpg
%{_datadir}/icons/hicolor/*/apps/*.png
%{_libexecdir}/mdm-factory-slave
%{_libexecdir}/mdm-host-chooser
%{_libexecdir}/mdm-product-slave
%{_libexecdir}/mdm-session-worker
%{_libexecdir}/mdm-simple-chooser
%{_libexecdir}/mdm-simple-greeter
%{_libexecdir}/mdm-simple-slave
%{_libexecdir}/mdm-xdmcp-chooser-slave
%{_sbindir}/mdm
%{_sbindir}/mdm-binary
%{_bindir}/mdmflexiserver
%{_bindir}/mdm-screenshot
%{_datadir}/mdm/*.ui
%{_datadir}/mdm/locale.alias
%{_sysconfdir}/mateconf/schemas/*.schemas
%{_datadir}/mdm/gdb-cmd
%{_libexecdir}/mdm-crash-logger
%{_libdir}/libmdm*.so*
%{_libdir}/mdm/simple-greeter/plugins/password.so
%{_datadir}/mdm/simple-greeter/extensions/password/page.ui
%dir %{_datadir}/mdm
%dir %{_datadir}/mdm/autostart
%dir %{_datadir}/mdm/autostart/LoginWindow
%config %{_datadir}/mdm/autostart/LoginWindow/*
%dir %{_localstatedir}/log/mdm
%dir %{_localstatedir}/spool/mdm
%attr(1770, mdm, mdm) %dir %{_localstatedir}/lib/mdm
%attr(1750, mdm, mdm) %dir %{_localstatedir}/lib/mdm/.mateconf.mandatory
%attr(1640, mdm, mdm) %dir %{_localstatedir}/lib/mdm/.mateconf.mandatory/%mateconf-tree.xml
%attr(1640, mdm, mdm) %dir %{_localstatedir}/lib/mdm/.mateconf.path
%attr(1770, root, mdm) %dir %{_localstatedir}/mdm
%attr(1777, root, mdm) %dir %{_localstatedir}/run/mdm
%attr(1755, root, mdm) %dir %{_localstatedir}/cache/mdm
%{_datadir}/mate/help/mdm/*
%{_datadir}/omf/mdm/

%files user-switch-applet
%defattr(-, root, root)
%{_libexecdir}/mdm-user-switch-applet
%{_libdir}/matecomponent/servers/MATE_FastUserSwitchApplet.server
%{_datadir}/mate-2.0/ui/MATE_FastUserSwitchApplet.xml

%files plugin-smartcard
%defattr(-, root, root)
%config %{_sysconfdir}/pam.d/mdm-smartcard
%{_datadir}/mdm/simple-greeter/extensions/smartcard/page.ui
%{_libdir}/mdm/simple-greeter/plugins/smartcard.so
%{_libexecdir}/mdm-smartcard-worker

%files plugin-fingerprint
%defattr(-, root, root)
%config %{_sysconfdir}/pam.d/mdm-fingerprint
%{_datadir}/mdm/simple-greeter/extensions/fingerprint/page.ui
%{_libdir}/mdm/simple-greeter/plugins/fingerprint.so


%changelog
* Fri Apr 06 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-6
- add numlock patch

* Sat Mar 25 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-5
- remove gnome-keyring dependency

* Sat Mar 10 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-4
- add gnome-keyring to mdm pam files
- add mdm_first_background_patch.patch

* Tue Mar 06 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-3
- fix mate-keyring login issue

* Tue Feb 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-2
- rebuild for enable builds for .i686

* Tue Feb 07 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-1
- update version

* Mon Feb 06 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
-test for mate-accountsservice

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- insert some patches from gdm fedora 14

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mdm.spec based on gdm-2.32.0-1.fc14 spec

* Thu Sep 30 2010 Ray Strode <rstrode@redhat.com> 2.32.0-1
- Update to 2.32.0

