%define libxml2_version 2.5
%define mate_corba_version 1.1.0
%define libmatecomponent_version 1.1.0
%define libmatecanvas_version 1.1.0
%define libmate_version 1.1.2
%define libart_lgpl_version 2.3.8
%define gtk2_version 2.6.0
%define libglade2_version 2.0.0
%define glib2_version 2.6.0

%define po_package libmatecomponentui

Summary: libmatecomponent user interface components
Name:    libmatecomponentui
Version: 1.2.0
Release: 1%{?dist}
URL:     https://github.com/Perberos/Mate-Desktop-Environment
Source0: http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
License: LGPLv2+
Group:   System Environment/Libraries

Requires: mate-corba >= %{mate_corba_version}

BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: mate-corba-devel >= %{mate_corba_version}
BuildRequires: libmatecomponent-devel >= %{libmatecomponent_version}
BuildRequires: libmatecanvas-devel >= %{libmatecanvas_version}
BuildRequires: libmate-devel >= %{libgnome_version}
BuildRequires: libart_lgpl-devel >= %{libart_lgpl_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libglade2-devel >= %{libglade2_version}
BuildRequires: intltool >= 0.14-1
BuildRequires: libtool >= 1.4.2-12
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gettext
BuildRequires: mate-common


%description

libmatecomponentui is a component system based on CORBA, used by the MATE
desktop. libmatecomponentui contains the user interface related components
that come with libmatecomponent.

%package devel
Summary: Libraries and headers for libmatecomponentui
Group: Development/Libraries
License: GPLv2+ and LGPLv2+
Requires: %name = %{version}-%{release}
Requires: libxml2-devel >= %{libxml2_version}
Requires: mate-corba-devel >= %{mate_corba_version}
Requires: libmatecomponent-devel >= %{libmatecomponent_version}
Requires: libmatecanvas-devel >= %{libgnomecanvas_version}
Requires: libmate-devel >= %{libgnome_version}
Requires: libart_lgpl-devel >= %{libart_lgpl_version}
Requires: gtk2-devel >= %{gtk2_version}
Requires: libglade2-devel >= %{libglade2_version}
Requires: glib2-devel >= %{glib2_version}
Requires: pkgconfig

%description devel

libmatecomponentui is a component system based on CORBA, used by the MATE desktop.
libmatecomponentui contains GUI components that come with libmatecomponent.

This package contains header files used to compile programs that
use libmatecomponentui.

%prep
%setup -q -n %{name}-%{version}
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.la
#rm -f $RPM_BUILD_ROOT%{_datadir}/applications/matecomponent-browser.desktop

for serverfile in $RPM_BUILD_ROOT%{_libdir}/matecomponent/servers/*.server; do
    sed -i -e 's|location *= *"/usr/lib\(64\)*/|location="/usr/$LIB/|' $serverfile
done


%find_lang %{po_package}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-,root,root)
%doc COPYING.LIB NEWS README
%{_libdir}/lib*.so.*
%{_libdir}/libglade/2.0/*.so
%{_libdir}/matecomponent/servers/*
%{_datadir}/applications/matecomponent-browser.desktop
%{_datadir}/mate-2.0/ui/*

%files devel
%defattr(-,root,root)
%doc COPYING COPYING.LIB
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/*
%{_libdir}/matecomponent-2.0
%{_datadir}/gtk-doc/html/libmatecomponentui/*

%changelog
* Thu Mar 01 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update version to 1.2

* Thu Feb 16 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-2
- rebuild for enable builds for .i686

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-1
- libmatecomponentui.spec based on libbonoboui-2.32.1-1.fc16 spec

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.24.5-2
- Rebuild for new libpng
