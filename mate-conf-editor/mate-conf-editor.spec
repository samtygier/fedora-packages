%define mate-conf_version 1.1.0

Summary: 	Editor/admin tool for MateConf
Name: 		mate-conf-editor
Version: 	1.2.0
Release: 	1%{?dist}
URL: 		http://pub.mate-desktop.org
Source0: 	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
License: 	GPLv2+ and GFDL
Group: 		Applications/System

Requires(pre): mate-conf >= %{mate-conf_version}
Requires(post): mate-conf >= %{mate-conf_version}
Requires(preun): mate-conf >= %{mate-conf_version}

BuildRequires: mate-conf-devel
BuildRequires: gtk2-devel
BuildRequires: dbus-glib-devel
BuildRequires: desktop-file-utils
BuildRequires: scrollkeeper
BuildRequires: gettext
BuildRequires: mate-doc-utils
BuildRequires: intltool
BuildRequires: mate-common
BuildRequires: autoconf automake libtool

%description
mate-conf-editor allows you to browse and modify MateConf configuration
sources.

%prep
%setup -q
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

# stuff we don't want
rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

%find_lang mateconf-editor --all-name

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
mateconftool-2 --makefile-install-rule %{_sysconfdir}/mateconf/schemas/mateconf-editor.schemas > /dev/null || :

touch --no-create %{_datadir}/icons/hicolor >& /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule %{_sysconfdir}/mateconf/schemas/mateconf-editor.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule %{_sysconfdir}/mateconf/schemas/mateconf-editor.schemas > /dev/null || :
fi

%postun
if [ $1 -eq 0 ]; then
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files -f mateconf-editor.lang
%defattr(-,root,root)
%doc AUTHORS NEWS README COPYING
%{_bindir}/mateconf-editor
%{_datadir}/icons/hicolor/*/apps/mateconf-editor.png
%{_datadir}/mateconf-editor
%{_datadir}/applications/mateconf-editor.desktop
%{_mandir}/man1/mateconf-editor.1.gz
%{_sysconfdir}/mateconf/schemas/mateconf-editor.schemas
%dir %{_datadir}/omf/mateconf-editor
%{_datadir}/mate/help/mateconf-editor/*
%{_datadir}/omf/mateconf-editor/*

%changelog
* Mon Mar 12 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-conf-editor.spec based on gconf-editor-2.32.0-2.fc15 spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

