Name:           libmateweather
Version:        1.2.0
Release:        1%{?dist}
Summary:        A library for weather information

Group:          System Environment/Libraries
License:        GPLv2+
URL: 			http://mate-desktop.org
Source0:         http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

# Patch from Ubuntu...
Patch0: gettext-not-xml.patch

BuildRequires:  mate-conf-devel >= 1.1.0
BuildRequires:  dbus-devel
BuildRequires:  gtk2-devel >= 2.11.0
BuildRequires:  libsoup-devel >= 2.4
BuildRequires:  libxml2-devel >= 2.6
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  gtk-doc
BuildRequires:  autoconf automake libtool
BuildRequires:  mate-common

# for directories
Requires: mate-icon-theme

%description
libmateweather is a library to access weather information from online
services for numerous locations.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
# libgweather used to be part of mate-applets, and
# mate-applets-devel only had the libmateweather-devel parts in it
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       gtk-doc

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh
%patch0 -p1 -b .gettext
gtkdocize
autoreconf -i -f

%build

%configure \
	--disable-static \
	--disable-gtk-doc

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{name} --all-name

%post
/sbin/ldconfig
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
mateconftool-2 --makefile-install-rule %{_sysconfdir}/mateconf/schemas/mateweather.schemas > /dev/null || :
touch --no-create %{_datadir}/icons/mate &>/dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule %{_sysconfdir}/mateconf/schemas/mateweather.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule %{_sysconfdir}/mateconf/schemas/mateweather.schemas > /dev/null || :
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/mate &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/mate &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -q %{_datadir}/icons/mate &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_sysconfdir}/mateconf/schemas/mateweather.schemas
%{_libdir}/libmateweather.so.*
%dir %{_datadir}/libmateweather
%{_datadir}/libmateweather/*
%{_datadir}/icons/mate/*/status/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libmateweather
%{_libdir}/libmateweather.so
%{_libdir}/pkgconfig/mateweather.pc
%{_datadir}/gtk-doc/html/libmateweather

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686
- enable fedora patch

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- libmateweather.spec based on libgweather-2.30.3-1.fc14 spec

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.3-1
- Update to 2.30.3

