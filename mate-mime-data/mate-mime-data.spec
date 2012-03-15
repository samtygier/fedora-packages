Summary: 		MIME type data files for MATE desktop
Name: 			mate-mime-data
Version: 		1.2.0
Release: 		1%{?dist}
URL: 			http://mate-desktop.org
Source0: 		http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
				# No license attribution, just COPYING.
License: 		GPL+
Group: 			System Environment/Libraries
BuildArch: 		noarch
BuildRequires: 	perl(XML::Parser)
BuildRequires: 	gettext
BuildRequires:  mate-common
BuildRequires:  glib2-devel
BuildRequires:  intltool

# Fedora specific patches
Patch0: gnome-mime-data-2.2.0-openoffice.patch
Patch1: gnome-mime-data-2.2.0-rpminstall.patch
Patch3: gnome-mime-data-2.4.1-default-applications.patch

%description
mate-mime-data provides the file type recognition data files for mate-vfs

%prep
%setup -q
%patch0 -p1 -b .openoffice
%patch1 -p1 -b .rpminstall
%patch3 -p1 -b .default-applications

NOCONFIGURE=1 ./autogen.sh

%build

%configure


make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%find_lang %name

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%config %{_sysconfdir}/mate-vfs-mime-magic
%{_datadir}/application-registry
%{_datadir}/mime-info/*.keys
%{_datadir}/mime-info/*.mime
%{_datadir}/pkgconfig/*

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Sun Feb 19 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-2
- rebuild for enable builds for .i686
- enable fedora patches

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-file-manager.spec based on gnome-mime-data-2.18.0-8.fc15 spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

