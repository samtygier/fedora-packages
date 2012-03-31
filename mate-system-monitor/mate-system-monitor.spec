# Note that this is NOT a relocatable package

%define libgtop2_version 2.23.1
%define libwnck_version 2.9.92
%define pango_version 1.2.0
%define gtk2_version 2.12
%define desktop_file_utils_version 0.2.90
%define libselinux_version 1.23.2
%define mate_conf_version 1.1.0

Summary: 	Process and resource monitor
Name: 		mate-system-monitor
Version: 	1.2.1
Release: 	1%{?dist}
License: 	GPLv2+
Group: 		Applications/System
URL: 		http://pub.mate-desktop.org
Source: 	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

BuildRequires: mate-conf-devel
BuildRequires: mate-vfs-devel
BuildRequires: libgtop2-devel >= %{libgtop2_version}
BuildRequires: libwnck-devel >= %{libwnck_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: gtkmm24-devel
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: startup-notification-devel
BuildRequires: intltool scrollkeeper gettext
BuildRequires: libselinux-devel >= %{libselinux_version}
BuildRequires: mate-icon-theme
BuildRequires: pcre-devel
BuildRequires: librsvg2-devel
BuildRequires: mate-doc-utils >= 1.0.0
BuildRequires: mate-common
BuildRequires: dbus-glib-devel

# needed for autoreconf
BuildRequires: autoconf, automake, libtool

Requires(pre): mate-conf >= %{mate_conf_version}
Requires(post): mate-conf >= %{mate_conf_version}
Requires(preun): mate-conf >= %{mate_conf_version}

%description
mate-system-monitor allows to graphically view and manipulate the running
processes on your system. It also provides an overview of available resources
such as CPU and memory.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

autoreconf -i -f


%build

%configure \
	--disable-static \
	--disable-scrollkeeper \
	--enable-compile-warnings=minimum

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

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

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
mateconftool-2 --makefile-install-rule %{_sysconfdir}/mateconf/schemas/mate-system-monitor.schemas > /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
    export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
    mateconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/mateconf/schemas/mate-system-monitor.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
    export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
    mateconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/mateconf/schemas/mate-system-monitor.schemas > /dev/null || :
fi

%files -f %{name}.lang
%defattr(-, root, root,-)
%doc AUTHORS NEWS COPYING README
%{_sysconfdir}/mateconf/schemas/*
%{_bindir}/mate-system-monitor
%{_datadir}/applications/*
%{_datadir}/pixmaps/mate-system-monitor/
%{_datadir}/mate/help/mate-system-monitor/
%{_datadir}/omf/mate-system-monitor/

%changelog
* Tue Mar 27 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
- update to 1.2.1

* Thu Mar 08 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2

* Tue Feb 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686
- enable fedora patches

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-system-monitor.spec based on gnome-system-monitor-2.28.2-1.fc14 spec

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.2-1
- Update to 2.28.2

