%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Last updated for version 2.29.1
# The order here corresponds to that in configure.ac,
# for easier comparison.  Please do not alphabetize.
%define pygtk_version                   2.10.3
%define glib_version                    2.6.0
%define gtk_version                     2.4.0
%define mate_python_version             1.1.0
%define mate_panel_version              1.1.0
%define gtksourceview_version           1.8.5-2
%define libwnck_version                 2.19.3
%define libgtop_version                 2.13.0
%define mate_media_version              1.1.0
%define mate_conf_version               1.1.0
%define marco_version                   1.1.0
%define librsvg2_version                2.13.93
%define mate_keyring_version            1.1.0
%define mate_desktop_version            1.1.0
%define eds_version                     1.4.0

### Abstract ###

Name: 		mate-python2-desktop
Version: 	1.2.0
Release: 	1%{?dist}
License: 	GPLv2+
Group: 		Development/Languages
Summary: 	The sources for additional PyMATE Python extension modules
URL: 		http://pub.mate-desktop.org
Source: 	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

Patch0: 	mate-python-desktop_change-directories.patch
Patch1: 	mate-python2-desktop_evolution_path.patch

### Dependencies ###

Requires: mate-python2-canvas >= %{mate_python_version}

### Build Dependencies ###

BuildRequires: evolution-data-server-devel >= %{eds_version}
BuildRequires: glib2-devel >= %{glib_version}
BuildRequires: mate-conf-devel >= %{mate_conf_version}
BuildRequires: mate-desktop-devel >= %{mate_desktop_version}
BuildRequires: mate-keyring-devel >= %{mate_keyring_version}
BuildRequires: mate-panel-devel >= %{mate_panel_version}
BuildRequires: mate-python2-matecomponent >= %{mate_python_version}
BuildRequires: mate-python2-canvas >= %{mate_python_version}
BuildRequires: mate-python2-devel >= %{mate_python_version}
BuildRequires: mate-python2-mateconf >= %{mate_python_version}
BuildRequires: gtk2-devel >= %{gtk_version}
BuildRequires: libmateui-devel
BuildRequires: libgtop2-devel >= %{libgtop_version}
BuildRequires: librsvg2-devel >= %{librsvg2_version}
BuildRequires: libwnck-devel >= %{libwnck_version}
BuildRequires: marco-devel >= %{marco_version}
BuildRequires: pygtk2-devel >= %{pygtk_version}
BuildRequires: python-devel
BuildRequires: autoconf, automake, libtool
BuildRequires: mate-common
BuildRequires: dbus-glib-devel
BuildRequires: dbus-devel
BuildRequires: openssl-devel
BuildRequires: libgcrypt-devel
BuildRequires: avahi-glib-devel
BuildRequires: libselinux-devel


%description
The mate-python-desktop package contains the source packages for additional 
Python bindings for MATE. It should be used together with mate-python.

%package -n mate-python2-applet
Summary: Python bindings for MATE Panel applets.
License: LGPLv2
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
# applets from GNOME 1.4 are no longer supported - we only have 1 panel
Obsoletes: pymate-applet <= 1.4.2
Requires: mate-python2-matecomponent
Requires: mate-python2-mate

%description -n mate-python2-applet
This module contains a wrapper that allows MATE Panel applets to be
written in Python.

#%package -n mate-python2-brasero
#Summary: Python bindings for interacting with brasero
#License: LGPLv2
#Group: Development/Languages
#Requires: %{name} = %{version}-%{release}
#Requires: brasero-libs >= %{brasero_version}

#%description -n mate-python2-brasero
#This module contains a wrapper that allows the use of brasero via Python.

#%package -n mate-python2-atril
#Summary: Python bindings for interacting with atril
#License: LGPLv2
#Group: Development/Languages
#Requires: %{name} = %{version}-%{release}
#Requires: atril-libs >= %{atril_version}

#%description -n mate-python2-atril
#This module contains a wrapper that allows the use of atril via Python.

%package -n mate-python2-evolution
Summary: Python bindings for interacting with evolution-data-server
License: LGPLv2
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: evolution-data-server >= %{eds_version}
Provides: evolution-python = %{version}-%{release}
Obsoletes: evolution-python <= 0.0.4-3

%description -n mate-python2-evolution
This module contains a wrapper that allows the use of evolution-data-server
via Python.

#%package -n mate-python2-gnomeprint
#Summary: Python bindings for interacting with libgnomeprint
#License: LGPLv2
#Group: Development/Languages
#Requires: %{name} = %{version}-%{release}
#Requires: libgnomeprint22
#Requires: libgnomeprintui22
#Requires: gnome-python2-canvas

#%description -n gnome-python2-gnomeprint
#This module contains a wrapper that allows the use of libgnomeprint via
#Python.

#%package -n mate-python2-gtksourceview
#Summary: Python bindings for interacting with the gtksourceview library 
#License: GPLv2+
#Group: Development/Languages
#Requires: %{name} = %{version}-%{release}
#Requires: gtksourceview >= %{gtksourceview_version}
#Requires: gnome-python2-gnomeprint

#%description -n gnome-python2-gtksourceview
#This module contains a wrapper that allows the use of gtksourceview via
#Python.

%package -n mate-python2-libwnck
Summary: Python bindings for interacting with libwnck
License: LGPLv2
Group: Development/Languages
Requires: libwnck >= %{libwnck_version}

%description -n mate-python2-libwnck
This module contains a wrapper that allows the use of libwnck via
Python.

%package -n mate-python2-libgtop2
Summary: Python bindings for interacting with libgtop
License: GPLv2+
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libgtop2 >= %{libgtop_version}

%description -n mate-python2-libgtop2
This module contains a wrapper that allows the use of libgtop via
Python.

%package -n mate-python2-marco
Summary: Python bindings for interacting with marco
License: GPLv2
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: marco >= %{marco_version}

%description -n mate-python2-marco
This module contains a wrapper that allows the use of marco
via Python.

#%package -n gnome-python2-totem
#Summary: Python bindings for interacting with totem
#License: LGPLv2
#Group: Development/Languages
#Requires: %{name} = %{version}-%{release}
#Requires: totem-pl-parser >= %{totem_version}
#Requires: gnome-python2-gconf

#%description -n gnome-python2-totem
#This module contains a wrapper that allows the use of totem
#via Python.

%package -n mate-python2-rsvg
Summary: Python bindings for interacting with librsvg
License: LGPLv2
Group: Development/Languages
Requires: librsvg2 >= %{librsvg2_version}

%description -n mate-python2-rsvg
This module contains a wrapper that allows the use of librsvg
via Python.

%package -n mate-python2-matedesktop
Summary: Python bindings for interacting with mate-desktop
License: LGPLv2
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: mate-desktop >= %{mate_desktop_version}

%description -n mate-python2-matedesktop
This module contains a wrapper that allows the use of mate-desktop
via Python.

%package -n mate-python2-matekeyring
Summary: Python bindings for interacting with mate-keyring
License: LGPLv2
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: mate-keyring >= %{mate_keyring_version}

%description -n mate-python2-matekeyring
This module contains a wrapper that allows the use of mate-keyring
via Python.

%prep
%setup -q -n mate-python2-desktop-%{version}
%patch0 -p1 -b .mate-python-desktop_change-directories
%patch1 -p1 -b .mate-python2-desktop_evolution_path
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
	--disable-static\
	--enable-marco \
	--enable-applet \
	--enable-cajaburn \
	--enable-matekeyring \
 	--enable-matedesktop \
	--enable-mateprint \
	--enable-mateprintui \
	--enable-marco \
	--enable-evolution \
	--enable-evolution_ecal

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \;

rm -rf $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/gtk-2.0/gksu
rm -rf $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/gtk-2.0/bugbuddy.*

%files
%defattr(-,root,root,-)
%doc AUTHORS NEWS README COPYING COPYING.GPL COPYING.LGPL
%{_libdir}/pkgconfig/mate-python-desktop-2.0.pc
%{_datadir}/pygtk

%files -n mate-python2-applet
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/mate/applet.*
%{python_sitearch}/gtk-2.0/mateapplet.so
%{python_sitearch}/gtk-2.0/mateapplet.la

#%files -n mate-python2-brasero
#%defattr(-,root,root,-)
#%{python_sitearch}/gtk-2.0/braseroburn.so
#%{python_sitearch}/gtk-2.0/braseromedia.so

#%files -n mate-python2-atril
#%defattr(-,root,root,-)
#%{python_sitearch}/gtk-2.0/atril.so

%files -n mate-python2-evolution
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/mate-evolution/

#%files -n gnome-python2-gnomeprint
#%defattr(-,root,root,-)
#%{python_sitearch}/gtk-2.0/gnomeprint/
#%{_datadir}/gtk-doc/html/pygnomeprint
#%{_datadir}/gtk-doc/html/pygnomeprintui
#%defattr(644,root,root,755)
#%doc ../gnome-python-desktop-%{version}/examples/gnomeprint/*

#%files -n gnome-python2-gtksourceview
#%defattr(-,root,root,-)
#%{python_sitearch}/gtk-2.0/gtksourceview.so
#%{_datadir}/gtk-doc/html/pygtksourceview
#%defattr(644,root,root,755)
#%doc ../gnome-python-desktop-%{version}/examples/gtksourceview/*

%files -n mate-python2-libwnck
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/mate/wnck.so
%{python_sitearch}/gtk-2.0/mate/wnck.la

%files -n mate-python2-libgtop2
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/mate/gtop.so
%{python_sitearch}/gtk-2.0/mate/gtop.la

%files -n mate-python2-marco
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/marco.so
%{python_sitearch}/gtk-2.0/marco.la

#%files -n gnome-python2-totem
#%defattr(-,root,root,-)
#%ifnarch s390 s390x
#%{python_sitearch}/gtk-2.0/mediaprofiles.so
#%endif
#%{python_sitearch}/gtk-2.0/totem

%files -n mate-python2-rsvg
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/mate/rsvg.so
%{python_sitearch}/gtk-2.0/mate/rsvg.la

%files -n mate-python2-matedesktop
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/matedesktop

%files -n mate-python2-matekeyring
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/matekeyring.so
%{python_sitearch}/gtk-2.0/matekeyring.la

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0

* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-5
- test build

* Mon Feb 20 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-4
- rebuild for enable builds for .i686
- move some directories to avoid conflicts with gnome-python2-desktop
- change %{_datadir} back

* Tue Feb 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- rebuild for pymatecorba-1.1.0-2

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- change %{_datadir} from /usr/share to /usr/share/mate-defs to avoid conflicts
- with gnome-python2-desktop

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-python2-desktop.spec based on ggnome-python2-desktop-2.32.0-3.fc14 spec

* Tue Feb  7 2011 Daniel Drake <dsd@laptop.org> - 2.32.0-3
- Fix applying of patch from 2.6.32.0-2

