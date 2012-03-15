%define gettext_package mate-terminal

%define glib2_version 			2.16.0
%define mate_conf_version 		1.1.0
%define vte_version 			0.27
%define desktop_file_utils_version 	0.2.90
%define mateconf_version 		1.1.0
%define gtk2_version	 		2.24
%define glib2_version			1.2.10
%define	vte_version			0.28.2

Summary: 	Terminal emulator for MATE
Name: 		mate-terminal
Version: 	1.2.1
Release: 	1%{?dist}
License: 	GPLv2+ and GFDL
Group: 		User Interface/Desktops
URL: 		http://pub.mate-desktop.org
Source0: 	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

# mateconftool-2
Requires(pre): mate-conf >= %{mateconf_version}
Requires(post): mate-conf >= %{mateconf_version}
Requires(preun): mate-conf >= %{mateconf_version}

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
# for gtk-builder-convert
BuildRequires: gtk2-devel
BuildRequires: mate-conf-devel >= %{mateconf_version}
BuildRequires: vte-devel >= %{vte_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: gettext
BuildRequires: mate-doc-utils
BuildRequires: intltool
BuildRequires: mate-common
BuildRequires: autoconf automake libtool
BuildRequires: libSM-devel
BuildRequires: scrollkeeper

%description
mate-terminal is a terminal emulator for MATE. It supports translucent
backgrounds, opening multiple terminals in a single window (tabs) and
clickable URLs.

%prep
%setup -q

NOCONFIGURE=1 ./autogen.sh

%build
%configure \
	--disable-static \
	--with-gtk=2.0

make %{?_smp_mflags}

%install
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%find_lang %{gettext_package} --all-name

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/mate-terminal.schemas \
	> /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/mate-terminal.schemas \
	> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/mate-terminal.schemas \
	> /dev/null || :
fi

%files -f %{gettext_package}.lang
%defattr(-,root,root,-)

%doc AUTHORS COPYING NEWS README

%{_bindir}/mate-terminal
%{_datadir}/mate-terminal
%{_datadir}/omf/mate-terminal
%{_datadir}/applications/mate-terminal.desktop
%{_sysconfdir}/mateconf/schemas/mate-terminal.schemas
%{_datadir}/mate/help/mate-terminal/*

%changelog
* Wed Mar 14 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
- update to 1.2.1 version

* Thu Mar 08 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- correct %preun scriplet

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-terminal.spec based on gnome-terminal-2.33.5-2.fc15 spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

