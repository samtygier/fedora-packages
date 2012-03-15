%define _default_patch_fuzz 999

Summary: 		Unobtrusive window manager
Name: 			marco
Version: 		1.2.0
Release: 		1%{?dist}
URL: 			http://mate-desktop.org
Source0: 		http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

Patch0: 		Should-set-RestartStyleHint-to-RestartIfRunning-wh.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=558723
Patch4: stop-spamming-xsession-errors.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=135056
Patch5: dnd-keynav.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=336750
Patch10: screenshot-forkbomb.patch

# fedora specific patches
Patch11: workspaces.patch
Patch12: fresh-tooltips.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=598995
Patch16: Dont-focus-ancestor-window-on-a-different-workspac.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=599097
Patch18: For-mouse-and-sloppy-focus-return-to-mouse-mode-on.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=599248
Patch19: Add-nofocuswindows-preference-to-list-windows-that.patch
#Patch119: Exclude-the-current-application-from-no_focus_window.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=599261
Patch20: Add-a-newwindowsalwaysontop-preference.patch
Patch120: Apply-new_windows_always_on_top-to-newly-raised-acti.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=559816
Patch24: metacity-2.28-empty-keybindings.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=604319
Patch25: metacity-2.28-xioerror-unknown-display.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=599181
#Patch28: Stop-confusing-GDK-s-grab-tracking.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=622517
Patch29: Allow-breaking-out-from-maximization-during-mouse.patch

# default window icon: https://bugzilla.gnome.org/show_bug.cgi?id=616246
#Patch30: default-window-icon.patch

License: 		GPLv2+
Group: 			User Interface/Desktops
BuildRequires: 	gtk2-devel 
BuildRequires: 	pango-devel 
BuildRequires: 	fontconfig-devel
BuildRequires: 	mate-conf-devel 
BuildRequires: 	desktop-file-utils
BuildRequires: 	libglade2-devel 
BuildRequires: 	autoconf, automake, libtool, mate-common
BuildRequires: 	intltool
BuildRequires: 	startup-notification-devel 
BuildRequires: 	libtool automake autoconf gettext
BuildRequires: 	xorg-x11-proto-devel 
BuildRequires: 	libSM-devel, libICE-devel, libX11-devel
BuildRequires: 	libXext-devel, libXinerama-devel, libXrandr-devel, libXrender-devel
BuildRequires: 	libXcursor-devel
BuildRequires: 	libXcomposite-devel, libXdamage-devel
BuildRequires: 	dbus-devel
BuildRequires: 	libcanberra-devel
BuildRequires:  mate-doc-utils
BuildRequires:  mate-dialogs

Requires: 		startup-notification 
# for /usr/share/mate-control-center/keybindings, /usr/share/mate/wm-properties
Requires: 		mate-control-center-filesystem
# for /etc/mateconf/schemas
Requires: 		mate-conf
Requires: 		mate-dialogs

Requires(post): mate-conf
Requires(pre): 	mate-conf 
Requires(preun): mate-conf

# http://bugzilla.redhat.com/605675
Provides: firstboot(windowmanager) = marco

%description
Marco is a window manager that integrates nicely with the MATE desktop.
It strives to be quiet, small, stable, get on with its job, and stay out of
your attention.

%package devel
Group: Development/Libraries
Summary: Development files for marco
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the files needed for compiling programs using
the marco-private library. Note that you are not supposed to write
programs using the marco-private library, since it is a private
API. This package exists purely for technical reasons.

%prep
%setup -q
%patch0 -p1 -b .Should-set-RestartStyleHint-to-RestartIfRunning-wh
%patch4 -p1 -b .stop-spamming-xsession-errors
%patch5 -p1 -b .dnd-keynav
%patch10 -p1 -b .screenshot-forkbomb
%patch11 -p1 -b .workspaces
%patch12 -p1 -b .fresh-tooltips
%patch16 -p1 -b .focus-different-workspace
%patch18 -p1 -b .focus-on-motion
%patch19 -p1 -b .no-focus-windows
#%patch119 -p1 -b .no-focus-windows-current-app
%patch20 -p1 -b .always-on-top
%patch120 -p1 -b .always-on-top-activate
%patch24 -p1 -b .empty-keybindings
%patch25 -p1 -b .xioerror-unknown-display
#%patch28 -p1 -b .grab-tracking
%patch29 -p1 -b .mouse-unmaximize

#%patch30 -p1 -b .window-icon
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static


SHOULD_HAVE_DEFINED="HAVE_SM HAVE_XINERAMA HAVE_XFREE_XINERAMA HAVE_SHAPE HAVE_RANDR HAVE_STARTUP_NOTIFICATION"

for I in $SHOULD_HAVE_DEFINED; do
  if ! grep -q "define $I" config.h; then
    echo "$I was not defined in config.h"
    grep "$I" config.h
    exit 1
  else
    echo "$I was defined as it should have been"
    grep "$I" config.h
  fi
done

make CPPFLAGS="$CPPFLAGS" LIBS="$LIBS" %{?_smp_mflags}



%install
rm -rf $RPM_BUILD_ROOT
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang marco

%post
/sbin/ldconfig
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/marco.schemas \
	> /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/marco.schemas \
	> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/marco.schemas \
	> /dev/null || :
fi

%postun -p /sbin/ldconfig

%files -f marco.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS HACKING doc/theme-format.txt doc/marco-theme.dtd rationales.txt
%{_bindir}/marco
%{_bindir}/marco-message
%{_sysconfdir}/mateconf/schemas/*.schemas
%{_datadir}/marco
%{_datadir}/themes/*
%{_datadir}/mate-control-center/keybindings/*
%{_libdir}/lib*.so.*
%{_mandir}/man1/marco.1.gz
%{_mandir}/man1/marco-message.1.gz
%{_datadir}/applications/marco.desktop
%{_datadir}/mate/wm-properties/marco-wm.desktop
%{_datadir}/mate/help/creating-marco-themes

%files devel
%defattr(-,root,root,-)
%{_bindir}/marco-theme-viewer
%{_bindir}/marco-window-demo
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man1/marco-theme-viewer.1.gz
%{_mandir}/man1/marco-window-demo.1.gz

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- rebuild for enable builds for .i686

* Wed Feb 08 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- added fedora patches

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-window-manager.spec based on metacity-2.34.1-1.fc16 spec

* Wed Jul  6 2011 Matthias Clasen <mclasen@redhat.com> - 2.34.1-1
- Update to 2.34.1

