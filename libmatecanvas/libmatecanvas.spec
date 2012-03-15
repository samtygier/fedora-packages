%define gettext_package libmatecanvas-2.0

Summary:        MateCanvas widget
Name:           libmatecanvas
Version:        1.2.0
Release:        1%{?dist}
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
License:        LGPLv2+
Group:          System Environment/Libraries
BuildRequires:  gtk2-devel
BuildRequires:  libart_lgpl-devel
BuildRequires:  libglade2-devel 
BuildRequires:  gail-devel
BuildRequires:  libtool gettext
BuildRequires:  intltool
BuildRequires:  mate-common
BuildRequires:  gtk-doc

%description
The canvas widget allows you to create custom displays using stock items
such as circles, lines, text, and so on. It was originally a port of the
Tk canvas widget but has evolved quite a bit over time.

%package devel
Summary: Libraries and headers for libgnomecanvas
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
# for /usr/share/gtk-doc/html
Requires: gtk-doc

%description devel
The canvas widget allows you to create custom displays using stock items
such as circles, lines, text, and so on. It was originally a port of the
Tk canvas widget but has evolved quite a bit over time.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
# runs on make anyway, let's use the ./autogen.sh hammer for now.
%configure \
	--enable-glade \
	--disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%find_lang libmatecanvas

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libmatecanvas.lang
%defattr(-,root,root)
%doc COPYING.LIB AUTHORS NEWS README
%{_libdir}/lib*.so.*
%{_libdir}/libglade/2.0/libgladematecanvas.so

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gtk-doc/html/libmatecanvas/*

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Sat Dec 24 2011 Wolfgang Ulbrich <info@raveit.de> - libmate-1.1.0.2
- rebuild for enable builds for .i686

* Sat Dec 24 2011 Wolfgang Ulbrich <info@raveit.de> - libmate-1.1.0.1
- libmatecanvas.spec based on libgnomecanvas-2.30.3-3.fc17 spec

* Mon Nov  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.30.3-3
- Rebuild against new libpng
