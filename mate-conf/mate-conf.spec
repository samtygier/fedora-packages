%define libxml2_version 2.4.12
%define mate_corba_version 1.1.0
%define glib2_version 2.25.9
%define dbus_version 1.0.1
%define dbus_glib_version 0.74

Summary: 	A process-transparent configuration system
Name: 		mate-conf
Version:	1.2.1
Release: 	1%{?dist}
License:	LGPLv2+
Group: 		System Environment/Base
Source0:	%{name}-%{version}.tar.gz
Source1: 	macros.mateconf
URL: 		https://github.com/mate-desktop/mate-conf

BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: libxslt-devel
BuildRequires: mate-corba-devel >= %{mate_corba_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk-doc >= 0.9
BuildRequires: pkgconfig >= 0.14
BuildRequires: gettext
BuildRequires: openldap-devel
BuildRequires: intltool
BuildRequires: polkit-devel >= 0.92
BuildRequires: dbus-glib-devel >= 0.8
BuildRequires: gobject-introspection-devel >= 0.6.7
BuildRequires: autoconf automake libtool
BuildRequires: mate-common
BuildRequires: gtk2-devel
Requires: dbus
# for patch0
Requires: /usr/bin/killall
Conflicts: mate-conf-dbus

Patch0: GConf-2.18.0.1-reload.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=568845

%description
mate-conf is a process-transparent configuration database API used to
store user preferences. It has pluggable backends and features to
support workgroup administration.

%package devel
Summary: Headers and libraries for mate-conf development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libxml2-devel >= %{libxml2_version}
Requires: mate-conf-devel >= %{mate_corba_version}
Requires: glib2-devel >= %{glib2_version}
# we install a pc file
Requires: pkgconfig
# we install an automake macro
Requires: automake

%description devel
mate-conf development package. Contains files needed for doing
development using mate-conf.

%package gtk
Summary: Graphical mate-conf utilities
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}

%description gtk
The mate-conf-gtk package contains graphical mate-conf utilities
which require GTK+.

%prep
%setup -q -n mate-conf-%{version}
%patch0 -p1 -b .reload
NOCONFIGURE=1 ./autogen.sh

%build
# let's use the ./autogen.sh hammer for now.

%configure \
	--disable-static \
	--with-openldap \
	--enable-defaults-service \
	--enable-gtk \
	--disable-gsettings-backend

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/mateconf/schemas
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/mateconf/mateconf.xml.system
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/rpm-state/mateconf
mkdir -p $RPM_BUILD_ROOT%{_datadir}/MateConf/matesettings

install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/


%find_lang %{name}

%post
/sbin/ldconfig

if [ $1 -gt 1 ]; then
    if ! fgrep -q mateconf.xml.system %{_sysconfdir}/mateconf/2/path; then
        sed -i -e 's@xml:readwrite:$(HOME)/.mateconf@&\n\n# Location for system-wide settings.\nxml:readonly:/etc/mateconf/mateconf.xml.system@' %{_sysconfdir}/mateconf/2/path
    fi
fi

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root)
%doc COPYING NEWS README backends/README.evoldap
%config(noreplace) %{_sysconfdir}/mateconf/2/path
%config(noreplace) %{_sysconfdir}/mateconf/2/evoldap.conf
%dir %{_sysconfdir}/mateconf
%dir %{_sysconfdir}/mateconf/2
%dir %{_sysconfdir}/mateconf/mateconf.xml.defaults
%dir %{_sysconfdir}/mateconf/mateconf.xml.mandatory
%dir %{_sysconfdir}/mateconf/mateconf.xml.system
%dir %{_sysconfdir}/mateconf/schemas
%{_bindir}/mateconf-merge-tree
%{_bindir}/mateconftool-2
%{_libexecdir}/mateconfd-2
%{_libdir}/*.so.*
%{_libdir}/MateConf/2/*.so
%dir %{_datadir}/sgml
%{_datadir}/sgml/mateconf
%{_datadir}/MateConf
%{_mandir}/man1/*
%dir %{_libdir}/MateConf
%dir %{_libdir}/MateConf/2
%{_sysconfdir}/dbus-1/system.d/org.mate.MateConf.Defaults.conf
%{_libexecdir}/mateconf-defaults-mechanism
%{_datadir}/polkit-1/actions/org.mate.mateconf.defaults.policy
%{_datadir}/dbus-1/system-services/org.mate.MateConf.Defaults.service
%{_datadir}/dbus-1/services/org.mate.MateConf.service
%dir %{_localstatedir}/lib/rpm-state/
%{_localstatedir}/lib/rpm-state/mateconf/
%{_libdir}/girepository-1.0
%{_libdir}/MateConf/2/libmateconfbackend-evoldap.la
%{_libdir}/MateConf/2/libmateconfbackend-oldxml.la
%{_libdir}/MateConf/2/libmateconfbackend-xml.la
%{_libdir}/libmateconf-2.la
%{_sysconfdir}/rpm/macros.mateconf


%files gtk
%defattr(-, root, root)
%{_libexecdir}/mateconf-sanity-check-2

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_includedir}/mateconf
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc/html/mateconf
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0

%changelog
* Thu Mar 01 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
-update verion to 1.2

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- rebuild for enable builds for .i686

* Wed Feb 08 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- added patches from fedora GConf2-2.32.4-1.fc16


* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-conf.spec based on GConf2-2.32.4-1.fc16 spec

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.32.4-1
- Update to 2.32.4

