%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           mozo
Version:        1.2.0
Release:        1%{?dist}
Summary:        Menu editor for the MATE desktop

Group:          Applications/System
License:        LGPLv2+
URL:            http://pub.mate-desktop.org
Source0:        %{name}-%{version}.tar.xz

Patch1:         mate-menu-editor-move-and_rename_directorys.patch

BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  pygtk2-devel
BuildRequires:  pkgconfig
BuildRequires:  mate-menus-devel >= 1.1.1
BuildRequires:  intltool
BuildRequires:  mate-common
Requires:       pygtk2, mate-python2-mateconf
Requires:       mate-menus >= 1.1.1

Obsoletes:		mate-menu-editor
Provides:		mozo

%description
mozo is a graphical menu editor that lets you edit, add, and delete
menu entries. It follows the freedesktop.org menu specification and
should work with any desktop environment that uses this specification.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%find_lang mozo

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f mozo.lang
%defattr(-,root,root,-)
%{python_sitelib}/Mozo
%{_bindir}/mozo
%{_datadir}/applications/mozo.desktop
%{_datadir}/mozo/mozo.ui
%{_datadir}/icons/hicolor/16x16/apps/mozo.png
%{_datadir}/icons/hicolor/22x22/apps/mozo.png
%{_datadir}/icons/hicolor/24x24/apps/mozo.png
%{_datadir}/icons/hicolor/32x32/apps/mozo.png
%{_datadir}/icons/hicolor/48x48/apps/mozo.png
%{_datadir}/icons/hicolor/256x256/apps/mozo.png

%changelog
* Wed Mar 14 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2.0

* Mon Mar 05 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-alacarte called now mozo

* Sat Mar 03 2012 Wolfgang Ulbrich <info@raveit.de> - 2011.12.01-3
- rename is now complete
- bin file called now matealacarte

* Sun Feb 19 2012 Wolfgang Ulbrich <info@raveit.de> - 2011.12.01-2
- move some directories to avoid conflicts with alacarte, but unfortunately
- not %{python_sitelib}/Alacarte

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 2011.12.01-1
- mate-menu-editor.spec based on alacarte-0.13.2-3.fc16 spec

* Mon Mar 14 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.13.2-3
- Require gnome-panel (#684927)
- Compile with %%{?_smp_mflags}
- Update icon-cache scriptlets

