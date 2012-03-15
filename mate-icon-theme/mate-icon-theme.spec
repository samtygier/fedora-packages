Summary: 		MATE icon theme
Name: 			mate-icon-theme
Version: 		1.2.0
Release: 		1%{?dist}
URL: 	 		http://mate-desktop.org
Source0: 		http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
License: 		GPL+
BuildArch: 		noarch
Group: 			User Interface/Desktops
BuildRequires: 	icon-naming-utils
BuildRequires: 	gettext
BuildRequires: 	intltool
BuildRequires:  mate-common
Requires: 		hicolor-icon-theme

%description
This package contains the default icon theme used by the MATE desktop.

%package legacy
Summary: Old names for icons in mate-icon-theme
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}

%description legacy
This package contains symlinks to make the icons in mate-icon-theme
available under old names.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static \
	--enable-icon-mapping

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Add scalable directories for symbolic icons
(cd $RPM_BUILD_ROOT%{_datadir}/icons/mate

mkdir -p scalable/actions
mkdir -p scalable/apps
mkdir -p scalable/devices
mkdir -p scalable/emblems
mkdir -p scalable/mimetypes
mkdir -p scalable/places
mkdir -p scalable/status
)

(cd $RPM_BUILD_ROOT%{_datadir}
 echo "%%defattr(-,root,root,-)"
 find icons/mate \( -name gtk-* -or -type f \) -printf "%%%%{_datadir}/%%p\n"
 find icons/mate -type d -printf "%%%%dir %%%%{_datadir}/%%p\n"
) > files.txt

(cd $RPM_BUILD_ROOT%{_datadir}
 echo "%%defattr(-,root,root,-)"
 find icons/mate \( -type l -and -not -name gtk-* \) -printf "%%%%{_datadir}/%%p\n"
) > legacy.txt

%post
touch --no-create %{_datadir}/icons/mate &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/mate &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/mate &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/mate &>/dev/null || :

%post legacy
touch --no-create %{_datadir}/icons/mate &>/dev/null || :

%postun legacy
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/mate &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/mate &>/dev/null || :
fi

%posttrans legacy
gtk-update-icon-cache %{_datadir}/icons/mate &>/dev/null || :


%files -f files.txt
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%{_datadir}/pkgconfig/mate-icon-theme.pc

%files legacy -f legacy.txt
%defattr(-,root,root,-)

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Thu Jan 26 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-2
- fix %postun error

* Thu Jan 26 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-1
- update to version 1.1.1

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-file-manager.spec based on gnome-icon-theme-2.31.0-2.fc15 spec

* Wed Sep 29 2010 Parag Nemade <paragn AT fedoraproject.org> 2.31.0-2
- Merge-review cleanup (#225818)

