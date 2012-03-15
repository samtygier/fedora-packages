# Last updated for 1.1.0
# The order here corresponds to that in configure.ac,
# for easier comparison.  Please do not alphabetize.
%define pygtk_version                   2.10.3
%define pymatecorba_version             1.1.0
%define glib_version                    2.6.0
%define gtk_version                     2.6.0
%define libmate_version                 1.1.2
%define libmateui_version               1.1.2
%define libmatecanvas_version           1.1.0
%define mate_vfs_version                1.1.0
%define mate_conf_version               1.1.0
%define libmatecomponent_activation_version       1.1.0
%define libmatecomponent_version        1.1.0
%define libmatecomponentui_version      1.1.0
%define python_version                  2.3.0
%define pygobject_version               2.17.0

### Abstract ###

Name:		mate-python2
Version:	1.2.0
Release:	1%{?dist}
License:	LGPLv2+
Group:		Development/Languages
Summary:	The sources for the PyMATE Python extension module.
URL:		https://github.com/mate-desktop/python-mate
Source:		%{name}-%{version}.tar.gz

### Dependencies ###

Requires: pygtk2 >= %{pygtk_version}

### Build Dependencies ###

BuildRequires: pygtk2-devel >= %{pygtk_version}
BuildRequires: python2-devel >= %{python_version}
BuildRequires: pymatecorba-devel >= %{pymatecorba_version}
BuildRequires: libmate-devel >= %{libmate_version}
BuildRequires: libmateui-devel >= %{libmateui_version}
BuildRequires: libmatecomponent-devel >= %{libmatecomponent_version}
BuildRequires: libmatecomponentui-devel >= %{libmatecomponentui_version}
BuildRequires: avahi-glib-devel
BuildRequires: mate-common
BuildRequires: dbus-glib-devel
BuildRequires: dbus-devel
BuildRequires: openssl-devel
BuildRequires: libgcrypt-devel
BuildRequires: libselinux-devel


%description
The mate-python package contains the source packages for the Python
bindings for MATE called PyMATE.

PyMATE is an extension module for Python that provides access to the
base MATE libraries, so you have access to more widgets, a simple
configuration interface, and metadata support.

%package mate
Summary: Python bindings for libmate
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: %{name}-matevfs = %{version}-%{release}
Requires: libmate >= %{libmate_version}
Requires: libmateui >= %{libmateui_version}

%description mate
This module contains a wrapper that makes libmate functionality available
from Python.

%package capplet
Summary: Python bindings for MATE Panel applets.
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description capplet
This module contains a wrapper that allows MATE Control Center
capplets to be in Python.

%package canvas
Summary: Python bindings for the MATE Canvas.
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: gtk2 >= %{gtk_version}
Requires: libmatecanvas >= %{libmatecanvas_version}
Requires: pygtk2 >= %{pygtk_version}

%description canvas
This module contains a wrapper that allows use of the MATE Canvas
in Python.


%package matecomponent
Summary: Python bindings for interacting with matecomponent.
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libmatecomponent-activation >= %{libmatecomponent_activation_version}
Requires: libmatecomponent >= %{libmatecomponent_version}
Requires: libmatecomponentui >= %{libmatecomponentui_version}
Requires: pymatecorba >= %{pymatecorba_version}

%description matecomponent
This module contains a wrapper that allows the creation of matecomponent
components and the embedding of matecomponent components in Python.

%package mateconf
Summary: Python bindings for interacting with MateConf
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: mate-conf >= %{mate_conf_version}

%description mateconf
This module contains a wrapper that allows the use of MateConf via Python.

%package matevfs
Summary: Python bindings for interacting with mate-vfs
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: mate-vfs >= %{mate_vfs_version}
Requires: libmatecomponent >= %{libmatecomponent_version}

%description matevfs
This module contains a wrapper that allows the use of gnome-vfs via python.

%package devel
Summary: Development files for building add-on libraries
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: mate-vfs-devel >= %{mate_vfs_version}
Requires: pkgconfig
Requires: python-devel >= %{python_version}

%description devel
This package contains files required to build wrappers for MATE add-on
libraries so that they interoperate with mate-python2.

%prep
%setup -q -n mate-python2-%{version}

NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \;



%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS
%dir %{python_sitearch}/gtk-2.0/mate/
%dir %{_datadir}/pygtk/2.0/defs
%dir %{_datadir}/pygtk/2.0/argtypes
%{_libdir}/mate-vfs-2.0/modules/libpythonmethod.la
%{_libdir}/python2.7/site-packages/gtk-2.0/mate/_mate.la
%{_libdir}/python2.7/site-packages/gtk-2.0/mate/ui.la
%{_libdir}/python2.7/site-packages/gtk-2.0/matecanvas.la
%{_libdir}/python2.7/site-packages/gtk-2.0/matecomponent/_matecomponent.la
%{_libdir}/python2.7/site-packages/gtk-2.0/matecomponent/activation.la
%{_libdir}/python2.7/site-packages/gtk-2.0/matecomponent/ui.la
%{_libdir}/python2.7/site-packages/gtk-2.0/mateconf.la




%files mate
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/mate/__init__.*
%{python_sitearch}/gtk-2.0/mate/_mate.so
%{python_sitearch}/gtk-2.0/mate/ui.so
%{_datadir}/pygtk/2.0/defs/mate/mate.defs
%{_datadir}/pygtk/2.0/defs/mate/mate-types.defs
%{_datadir}/pygtk/2.0/defs/mate/ui.defs

%files canvas
%defattr(-,root,root,-)
%dir %{python_sitearch}/gtk-2.0/mate/
%{python_sitearch}/gtk-2.0/mate/__init__.*
%{python_sitearch}/gtk-2.0/mate/canvas.*
%{python_sitearch}/gtk-2.0/matecanvas.so
%{_datadir}/pygtk/2.0/defs/mate/canvas.defs
%defattr(644,root,root,755)
%doc examples/canvas/*

%files matecomponent
%defattr(-,root,root,-)
%dir %{python_sitearch}/gtk-2.0/matecomponent/
%{python_sitearch}/gtk-2.0/matecomponent/__init__.*
%{python_sitearch}/gtk-2.0/matecomponent/*.so
%{_datadir}/pygtk/2.0/defs/matecomponent*.defs
%{_datadir}/pygtk/2.0/argtypes/matecomponent*
%defattr(644,root,root,755)
%doc examples/matecomponent/*


%files mateconf
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/mateconf.so
%{_datadir}/pygtk/2.0/defs/mateconf.defs
%{_datadir}/pygtk/2.0/argtypes/mateconf*
%defattr(644,root,root,755)
%doc examples/mateconf/*

%files matevfs
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/matevfs
%{python_sitearch}/gtk-2.0/mate/vfs*
%{_libdir}/mate-vfs-2.0/modules/libpythonmethod.so
%doc %{_datadir}/gtk-doc/html/pymatevfs
%defattr(644,root,root,755)
%doc examples/vfs/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/mate-python-2.0
%{_libdir}/pkgconfig/mate-python-2.0.pc

%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- removed upstreamed mate-python_change-directories.patch
- update to version 1.2

* Mon Feb 20 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-5
- rebuild for enable builds for .i686
- hopefully last directories change
- change %{_datadir} back

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-4
- rebuild for pymatecorba-1.1.0-2
 
* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- change %{_datadir} from /usr/share to /usr/share/mate-defs to avoid conflicts
- with gnome-python2-canvas and gnome-python2-gnome

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- correct some file path in the spec file

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-python2.spec based on gnome-python2-2.28.1-3.fc14.src spec

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.28.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

