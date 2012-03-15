%global enable_debugging 0

Summary:  		A menu system for the MATE project
Name: 			mate-menus
Version: 		1.2.0
Release: 		1%{?dist}
License: 		LGPLv2+
Group: 			System Environment/Libraries
URL: 			https://github.com/mate-desktop/mate-menus
Source0: 		%{name}-%{version}.tar.gz
				# Keep release notes from showing up in Applications>Other
Patch0: 		other-docs.patch

Requires:  		redhat-menus 
BuildRequires: 	gamin-devel
BuildRequires: 	gawk
BuildRequires: 	gettext
BuildRequires: 	glib2-devel
BuildRequires: 	pkgconfig
BuildRequires: 	python2-devel
 
BuildRequires: 	intltool
BuildRequires: 	mate-common
BuildRequires:  gobject-introspection-devel

%description
mate-menus is an implementation of the draft "Desktop
Menu Specification" from freedesktop.org. This package
also contains the MATE menu layout configuration files,
.directory files and assorted menu related utility programs,
Python bindings, and a simple menu editor.

%package devel
Summary: Libraries and include files for the MATE menu system
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package provides the necessary development libraries for
writing applications that use the MATE menu system.

%prep
%setup -q
%patch0 -p1 -b .other-docs

NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static \
	--enable-python \
	--enable-introspection=yes \
	%if %{enable_debugging}
	--enable-debug=yes
	%else
	--enable-debug=no
	%endif

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS NEWS COPYING.LIB
%{_libdir}/libmate-menu.so.*
%{python_sitearch}/matemenu.so
%{_datadir}/mate/desktop-directories/*.directory
%{_sysconfdir}/xdg/menus/*.menu
%{_datadir}/mate-menus/examples/mate-menus-ls.*
%{_libdir}/girepository-1.0/MateMenu-2.0.typelib

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/mate-menus
%{_datadir}/gir-1.0/MateMenu-2.0.gir


%changelog
* Wed Feb 29 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- enable mock builds
- update to version 1.2

* Thu Feb 23 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-3
- fixed build error for i686

* Sun Feb 19 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-2
- rebuild for enable builds for .i686
- enable fedora patch

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-1
- mate-file-manager.spec based on gnome-menus-2.30.4-6.fc15 spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

