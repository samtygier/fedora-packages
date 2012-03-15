Name:           caja-python
Version:        1.2.0
Release:        1%{?dist}
Summary:        Python bindings for Caja

Group:          Development/Libraries
License:        GPLv2+
URL:            http://pub.mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

BuildRequires:  python-devel
BuildRequires:  caja-devel
BuildRequires:  pygobject2-devel
BuildRequires:  gtk-doc
BuildRequires:  autoconf automake libtool
BuildRequires: 	mate-common
BuildRequires: 	pygtk2-devel
BuildRequires: 	mate-python2-devel

Requires:       caja >= 1.1.0

%description
Python bindings for Caja


%package devel
Summary:        Python bindings for Caja
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Python bindings for Caja

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions
find $RPM_BUILD_ROOT -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS
%{_libdir}/caja/extensions-2.0/libcaja-python.so
%{_libdir}/caja-python/caja.so
%dir %{_datadir}/%{name}/extensions

%files devel
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/doc/*

%changelog
* Wed Mar 14 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Mon Feb 13 2012 Wolfgang Ulbrich <info@raveit.de> - caja-python-1.1.0-2
- rebuild for enable builds for .i686

* Sat Jan 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- update to version 1.1.0

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 2011.12.01-1
- caja-python.spec based on nautilus-python-1.0-1.fc16 spec

* Tue Sep 27 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 1.0-1
- Update to 1.0
- Remove BuildRoot tag and %%clean section
- Own /usr/share/nautilus-python/extensions instead of the old arch
  dependent locations
