Summary: 		Desktop backgrounds packaged with the MATE desktop
Name: 			mate-backgrounds
Version: 		1.2.1
Release: 		1%{?dist}
License: 		GPLv2
Group: 			Applications/Multimedia
URL: 			http://pub.mate-desktop.org
Source0: 		http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
Patch0: 		mate-backgrounds_change_backgrounds_path.patch
BuildArch: 		noarch
BuildRequires: 	intltool
BuildRequires: 	gettext
BuildRequires:  mate-common
BuildRequires:  glib2-devel
Requires: 		desktop-backgrounds-compat
Requires: 		verne-backgrounds-single
Requires: 		verne-backgrounds-gnome

%description
The mate-backgrounds package contains images and tiles
to use for your desktop background which are packaged
with the MATE desktop.

%prep
%setup -q
%patch0 -p1 -b .mate-backgrounds_change
NOCONFIGURE=1 ./autogen.sh

%build

%configure


make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README AUTHORS
%{_datadir}/mate-background-properties
%{_datadir}/backgrounds/mate/*
%{_datadir}/locale/*

%changelog
* Fri Apr 06 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.1-1
- update to 1.2.1
- first mate background is added

* Wed Feb 29 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- rebuild for enable builds for .i686

* Thu Jan 26 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- add dependencies to get fedora 16 default background verne

* Wed Jan 05 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-backgrounds.spec based on gnome-backgrounds-2.32.0-1.fc14 spec

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> 2.32.0-1
- Update to 2.32.0

