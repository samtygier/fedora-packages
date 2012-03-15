Name:           mate-sensors-applet
Version:        1.2.0
Release:        1%{?dist}
Summary:        MATE panel applet for hardware sensors
Group:          User Interface/Desktops
License:        GPLv2+ and CC-BY-SA
URL:            http://pub.mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
Patch0:			sensors-applet-fixDSO.patch
Patch1:         sensors-applet-2.2.7-libnotify07.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  mate-panel-devel >= 1.1.0
BuildRequires:  libmatenotify-devel >= 1.1.0
BuildRequires:  lm_sensors-devel
BuildRequires:  mate-doc-utils
BuildRequires:  intltool
BuildRequires:  perl-XML-Parser
BuildRequires:  scrollkeeper
BuildRequires:  libmate-devel >= 1.1.0
BuildRequires:  libmateui-devel >= 1.1.0
BuildRequires:  cairo-devel >= 1.0.4
BuildRequires:  gettext
BuildRequires:  libXNVCtrl-devel   
BuildRequires:	libatasmart-devel >= 0.16
BuildRequires:	mate-common
BuildRequires:	gtk2-devel >= 2.14.0
BuildRequires:	glib2-devel >= 2.14.0
BuildRequires:	dbus-glib-devel >= 0.80
BuildRequires:	openssl-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	avahi-glib-devel
BuildRequires:	libselinux-devel
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

%description
MATE Sensors Applet is an applet for the MATE Panel to display readings
from hardware sensors, including CPU and system temperatures, fan speeds
and voltage readings under Linux.
Can interface via the Linux kernel i2c modules, or the i8k kernel module (for
Dell Inspirion 8000 Laptops).
Includes a simple, yet highly customizable display and intuitive 
user-interface.
Alarms can be set for each sensor to notify the user once a certain value
has been reached, and can be configured to execute a given command at given
repeated intervals.
MATE HIG v2.0 compliant.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n mate-sensors-applet-%{version}
NOCONFIGURE=1 ./autogen.sh
%patch0 -p1 -b .fixdso 
#%if 0%{?fedora} > 14
#%patch1 -p1 -b .libnotify07
#%endif

%build

%configure \
	--disable-static \
	--disable-scrollkeeper \
	--enable-libmatenotify \
	--with-nvidia

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name "*.la" -exec rm -rf {} ';'
%find_lang mate-sensors-applet


%post
scrollkeeper-update -q -o %{_datadir}/omf/sensors-applet || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
scrollkeeper-update -q || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files -f mate-sensors-applet.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libexecdir}/mate-sensors-applet
%{_libdir}/libmate-sensors-applet-plugin.so.*
%{_libdir}/mate-sensors-applet/
%{_libdir}/matecomponent/servers/*.server
%{_datadir}/mate-2.0/ui/*.xml
%{_datadir}/mate/help/mate-sensors-applet/
%{_datadir}/pixmaps/mate-sensors-applet/
%{_datadir}/icons/hicolor/*/*/*.png

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmate-sensors-applet-plugin.so
%{_includedir}/mate-sensors-applet/


%changelog
* Sun Mar 11 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0

* Tue Feb 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-2
- rebuild for enable builds for .i686
- enable fedora patches

* Thu Jan 26 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-1
- update to version 1.1.1

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-sensors-applet.spec based on gnome-applet-sensors-2.2.7-4.fc15 spec

* Thu Nov 18 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2.7-4
- patch and rebuild for new libnotify 0.7.0

