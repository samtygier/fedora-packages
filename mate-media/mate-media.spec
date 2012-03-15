%define glib2_version 2.4.0
%define pango_version 1.4.0
%define gtk2_version 2.10.0
%define libmate_version 1.1.2
%define libmateui_version 1.1.2
%define gail_version 1.2
%define desktop_file_utils_version 0.2.90
%define gstreamer_version 0.10.3

%define gettext_package mate-media

Summary:        MATE media programs
Name:           mate-media
Version:        1.2.0
Release:        1%{?dist}
License:        GPLv2+ and GFDL
Group:          Applications/Multimedia
Source:         http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
URL:            http://pub.mate-desktop.org
ExcludeArch:    s390 s390x

Requires(post): mate-conf >= 1.1.0
Requires(pre): mate-conf >= 1.1.0
Requires(preun): mate-conf >= 1.1.0

BuildRequires:  gtk2-devel >= %{gtk2_version}
BuildRequires:  mate-conf-devel
BuildRequires:  desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires:  gstreamer-devel >= %{gstreamer_version}
BuildRequires:  gstreamer-plugins-base-devel >= %{gstreamer_version}
BuildRequires:  gstreamer-plugins-good-devel
BuildRequires:  unique-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  libcanberra-devel
BuildRequires:  mate-doc-utils
BuildRequires:  intltool
BuildRequires:  mate-control-center-devel
BuildRequires:  scrollkeeper
BuildRequires:  mate-common

%description
This package contains a few media utilities for the MATE desktop,
including a volume control and a configuration utility for audio profiles.

%package apps
Summary: Some media-related applications for the MATE desktop
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description apps
This package contains an application to record and play sound files
in various formats and a configuration utility for the gstreamer media
framework.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
export LDFLAGS="-lm"
%configure \
	--disable-static \
	--enable-gstmix \
	--enable-gstprops \
	--disable-scrollkeeper \
	--disable-profiles
	

make %{?_smp_mflags}

# strip unneeded translations from .mo files
# ideally intltool (ha!) would do that for us
# http://bugzilla.gnome.org/show_bug.cgi?id=474987
cd po
grep -v ".*[.]desktop[.]in[.]in$\|.*[.]server[.]in[.]in$" POTFILES.in > POTFILES.keep
mv POTFILES.keep POTFILES.in
intltool-update --pot
for p in *.po; do
  msgmerge $p %{gettext_package}.pot > $p.out
  msgfmt -o `basename $p .po`.gmo $p.out
done

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/control-center-1/panels/lib*.*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/glade3/modules/lib*.*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

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

%find_lang %{gettext_package}

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
mateconftool-2 --makefile-install-rule \
    %{_sysconfdir}/mateconf/schemas/mate-volume-control.schemas \
    > /dev/null || :
touch --no-create %{_datadir}/icons/mate >&/dev/null || :

%post apps
touch --no-create %{_datadir}/icons/mate >&/dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
    if [ -f %{_sysconfdir}/mateconf/schemas/mate-volume-control.schemas ] ; then
    mateconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/mateconf/schemas/mate-volume-control.schemas \
      > /dev/null || :
  fi
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
    if [ -f %{_sysconfdir}/mateconf/schemas/mate-volume-control.schemas ] ; then
    mateconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/mateconf/schemas/mate-volume-control.schemas \
      > /dev/null || :
  fi
fi

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/mate >&/dev/null || :
  gtk-update-icon-cache --quiet %{_datadir}/icons/mate >&/dev/null || :
fi

%postun apps
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/mate >&/dev/null || :
  gtk-update-icon-cache --quiet %{_datadir}/icons/mate >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache --quiet %{_datadir}/icons/mate >&/dev/null || :

%posttrans apps
gtk-update-icon-cache --quiet %{_datadir}/icons/mate >&/dev/null || :

%files
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README
%{_bindir}/mate-volume-control
%config %{_sysconfdir}/mateconf/schemas/mate-volume-control.schemas
%{_datadir}/applications/mate-volume-control.desktop
%{_datadir}/mate-media
%{_datadir}/sounds/mate/
%{_datadir}/mate/help/mate-volume-control/*
%{_datadir}/omf/mate-volume-control/*
%{_datadir}/locale/

%files apps
%defattr(-, root, root)
%{_datadir}/icons/mate/*
%{_bindir}/mate-gstreamer-properties
%{_datadir}/mate-gstreamer-properties
%{_datadir}/applications/mate-gstreamer-properties.desktop
%{_datadir}/mate/help/mate-gstreamer-properties/*
%{_datadir}/omf/mate-gstreamer-properties/*


%changelog
* Wed Mar 14 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Sun Feb 19 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-media.spec based on gnome-media-2.32.0-1.fc14 spec

* Tue Sep 28 2010 Bastien Nocera <bnocera@redhat.com> 2.32.0-1
- Update to 2.32.0

