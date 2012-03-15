Name:           caja-sendto
Version:        1.2.0
Release:        1%{?dist}
Summary:        Caja context menu for sending files

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://pub.mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

BuildRequires:  gtk2-devel
BuildRequires:  caja-devel >= 1.1.2
BuildRequires:  gettext
BuildRequires:  perl-XML-Parser intltool
BuildRequires:  dbus-glib-devel >= 0.70
BuildRequires:  gupnp-devel >= 0.13
BuildRequires: 	mate-common
BuildRequires: 	gtk-doc

Requires(pre): mate-conf
Requires(post): mate-conf
Requires(preun): mate-conf

%description
The caja-sendto package provides a Caja context menu for
sending files via other desktop applications.  These functions are
implemented as plugins, so caja-sendto can be extended with
additional features.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the libraries amd header files that are needed
for writing plugins for caja-sendto.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure
make %{?_smp_mflags}


%install
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find $RPM_BUILD_ROOT \( -name '*.a' -o -name '*.la' \) -exec rm -f {} \;

#rm -f $RPM_BUILD_ROOT/%{_libdir}/caja-sendto/plugins/libnstbluetooth.so

%find_lang %{name}

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas || :

%postun
glib-compile-schemas %{_datadir}/glib-2.0/schemas || :

%pre
%mateconf_schema_prepare nst

%preun
%mateconf_schema_remove nst

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS
%{_libdir}/caja/extensions-2.0/libcaja-sendto.so
%dir %{_libdir}/caja-sendto
%dir %{_libdir}/caja-sendto/plugins
%{_libdir}/caja-sendto/plugins/*.so
%{_datadir}/caja-sendto
%{_bindir}/caja-sendto
%{_mandir}/man1/caja-sendto.1.gz
%{_datadir}/glib-2.0/schemas/org.mate.Caja.Sendto.gschema.xml
%{_datadir}/MateConf/gsettings/caja-sendto-convert

%files devel
%defattr(-,root,root,-)
%{_datadir}/gtk-doc
%{_libdir}/pkgconfig/caja-sendto.pc
%dir %{_includedir}/caja-sendto
%{_includedir}/caja-sendto/caja-sendto-plugin.h

%changelog
* Thu Mar 15 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0

* Fri Feb 25 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- correct scriplet error

* Tue Jan 31 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- switch to github version

* Tue Jan 31 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- caja-sendto.spec based on nautilus-sendto-2.32.0-1.fc14 spec

* Tue Sep 28 2010 Bastien Nocera <bnocera@redhat.com> 2.32.0-1
- Update to 2.32.0

