%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

### Abstract ###

Name: 		pymatecorba
Version: 	1.2.0
Release: 	1%{?dist}
License: 	LGPLv2+
Group: 		Development/Languages
Summary: 	Python bindings for Corba.
BuildRoot: 	%{_tmppath}/%{name}-root
URL: 		https://github.com/Perberos/Mate-Desktop-Environment
Source0: 	%{name}-%{version}.tar.gz

### Dependencies ###

Requires: mate-corba >= 1.0.0
Requires: glib2 >= 2.4.0
Requires: libIDL >= 0.8.0
Requires: python2 >= 2.3

### Build Dependencies ###

BuildRequires: mate-corba-devel >= 1.0.0
BuildRequires: autoconf
BuildRequires: automake >= 1.6.3-5
BuildRequires: glib2-devel >= 2.4.0
BuildRequires: libIDL-devel >= 0.8.0
BuildRequires: libtool
BuildRequires: pygtk2 >= 2.4.0
BuildRequires: python2-devel >= 2.3
BuildRequires: mate-common

%description
pymatecorba is an extension module for python that gives you access
to the ORBit2 CORBA ORB.

%package devel
Summary: Files needed to build wrappers for mate-corba addon libraries.
Group: Development/Languages
Requires: %{name} = %{version}

%description devel
This package contains files required to build wrappers for mate-corba addon
libraries so that they interoperate with pymatecorba

%prep
%setup -q -n %{name}-%{version}

NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS NEWS README ChangeLog

%defattr(755, root, root, 755)
%{python_sitearch}/*.so
%defattr(644, root, root, 755)
%{python_sitearch}/*.py*
%{python_sitearch}/MateCORBA.la

%files devel
%defattr(644, root, root, 755)
%{_includedir}/pymatecorba-2
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- removed upstreamed pymatecorba_rename.patch
- update to version 1.2

* Mon Feb 20 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-4
- rebuild for enable builds for .i686
- rename results are now in a patch

* Thu Feb 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- renamed again

* Thu Feb 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- try rename

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- pymatecorba.spec based on pyorbit-2.24.0-6.fc14 spec

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.24.0-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

