%define glib2_version 2.16.0
%define pango_version 1.8.0
%define libmateui_version 1.1.2
%define libmateprint_version 1.1.0
%define libmateprintui_version 1.1.0
%define desktop_file_utils_version 0.9
%define caja_version 1.1.0
%define mate_doc_utils_version 1.1.0

Summary:        Tool for viewing and creating archives
Name:           engrampa
Version:        1.2.0
Release:        1%{?dist}
License:        GPLv2+
Group:          Applications/Archiving
URL:            https://github.com/mate-desktop/mate-file-archiver
Source:         %{name}-%{version}.tar.gz

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: gtk2-devel
BuildRequires: libglade2-devel
BuildRequires: caja-devel >= %{caja_version}
BuildRequires: libtool
BuildRequires: gettext
BuildRequires: libSM-devel
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: mate-doc-utils >= %{mate_doc_utils_version}
BuildRequires: intltool
BuildRequires: mate-conf-devel
BuildRequires: mate-common

Requires(pre): mate-conf
Requires(post): mate-conf
Requires(preun): mate-conf

%description
engrampa is an application for creating and viewing archives files,
such as tar or zip files.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-scrollkeeper \
	--disable-static \
	--with-gtk=2.0 \
	--enable-caja-actions

export tagname=CC
make LIBTOOL=/usr/bin/libtool

%install
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
export tagname=CC
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

rm -rf $RPM_BUILD_ROOT/var/scrollkeeper
rm -f $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache

%find_lang %{name} --all-name

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/engrampa.schemas \
	> /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/engrampa.schemas \
	> /dev/null || :
fi

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor &> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/mateconf/schemas/engrampa.schemas \
    > /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-, root, root)
%doc README COPYING NEWS AUTHORS
%{_bindir}/engrampa
%{_datadir}/engrampa
%{_datadir}/applications/engrampa.desktop
%{_libdir}/caja/extensions-2.0/libcaja-engrampa.so
%{_libexecdir}/engrampa
%{_datadir}/icons/hicolor/*/apps/engrampa.png
%{_datadir}/icons/hicolor/scalable/apps/engrampa.svg
%{_sysconfdir}/mateconf/schemas/engrampa.schemas
%{_datadir}/mate/help/engrampa/*
%{_datadir}/omf/*


%changelog
* Thu Mar 08 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2

* Tue Feb 14 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- fixed scriplets error
- rebuild for enable builds for .i686

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- engrampa.spec based on file-roller-2.32.0-2.fc14 spec

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> 2.32.0-2
- Fix a typo in %%post. Spotted by Yanko Kaneti
