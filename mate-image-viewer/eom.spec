%define gtk2_version 2.13.1
%define glib2_version 2.15.3
%define libmateui_version 1.1.2
%define libglade_version 2.3.6
%define libart_version 2.3.16
%define mate_desktop_version 1.1.0
%define mate_icon_theme_version 1.1.0
%define desktop_file_utils_version 0.9
%define gail_version 1.2.0
%define libexif_version 0.6.12

Summary: 	Eye of MATE image viewer
Name:    	eom
Version: 	1.2.0
Release: 	1%{?dist}
URL: 		https://github.com/mate-desktop/mate-image-viewer
Source: 	%{name}-%{version}.tar.gz
		# The GFDL has an "or later version" clause embedded inside the license.
		# There is no need to add the + here.
License: 	GPLv2+ and GFDL
Group: 		User Interface/Desktops
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libglade2-devel >= %{libglade_version}
BuildRequires: gail-devel >= %{gail_version}
BuildRequires: libexif-devel >= %{libexif_version}
BuildRequires: exempi-devel
BuildRequires: lcms-devel
BuildRequires: libart_lgpl-devel >= %{libart_version}
BuildRequires: intltool
BuildRequires: libjpeg-devel
BuildRequires: scrollkeeper
BuildRequires: gettext
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: mate-doc-utils
BuildRequires: mate-desktop-devel >= %{gnome_desktop_version}
BuildRequires: mate-icon-theme >= %{gnome_icon_theme_version}
BuildRequires: libXt-devel
BuildRequires: libxml2-devel
BuildRequires: librsvg2-devel
BuildRequires: pygtk2-devel
BuildRequires: pygobject2-devel
BuildRequires: dbus-glib-devel


BuildRequires: mate-common
BuildRequires: gtk-doc
BuildRequires: mate-conf-devel

Requires(post): desktop-file-utils >= %{desktop_file_utils_version}
Requires(post): mate-conf
Requires(pre):  mate-conf
Requires(preun): mate-conf
Requires(postun): desktop-file-utils >= %{desktop_file_utils_version}

Patch1: eog-statusbar-date-race.patch

%description
The Eye of MATE image viewer (eog) is the official image viewer for the
MATE desktop. It can view single image files in a variety of formats, as
well as large image collections.

eom is extensible through a plugin system.

%package devel
Summary: Support for developing plugins for the eom image viewer
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtk2-devel
Requires: libglade2-devel
Requires: mate-conf-devel

%description devel
The Eye of MATE image viewer (eom) is the official image viewer for the
MATE desktop. This package allows you to develop plugins that add new
functionality to eom.

%prep
%setup -q
%patch1 -p1 -b .statusbar-date-race
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
	--disable-static \
	--disable-scrollkeeper

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%find_lang %{name} --all-name

# grr, --disable-scrollkeeper seems broken
rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

rm -rf $RPM_BUILD_ROOT%{_libdir}/eom/plugins/*.la

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


%post
update-desktop-database -q
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/eom.schemas \
	> /dev/null || :

touch %{_datadir}/icons/hicolor >&/dev/null || :


%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/eom.schemas \
	> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/eom.schemas \
	> /dev/null || :
fi

%postun
update-desktop-database -q
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%{_datadir}/eom
%{_datadir}/applications/*
%{_datadir}/omf/*
%{_datadir}/icons/hicolor/*/apps/*
%{_bindir}/*
%{_sysconfdir}/mateconf/schemas/*.schemas
%{_libdir}/eom
%{_datadir}/mate/help/eom/*

%files devel
%defattr(-,root,root)
%{_includedir}/eom-2.20
%{_libdir}/pkgconfig/eom.pc

%changelog
* Thu Mar 08 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2

* Fri Mar 02 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-4
- fix mock build error

* Sat Feb 11 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- rebuild for enable builds for .i686
- enable fedora patches

* Sat Feb 11 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- correct %preun error

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- eom.spec based on eog-2.32.0-3.fc14 spec

* Tue Dec  7 2010 Siddhesh Poyarekar <siddhesh@redhat.com> 2.32.0-3
- Workaround concurrency issue with statusbar-date plugin
  (bz #602412, gnome bz #622161)

