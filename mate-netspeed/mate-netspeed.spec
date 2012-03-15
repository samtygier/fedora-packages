Name:           mate-netspeed   
Version:        1.2.0
Release:        1%{?dist}
Summary:        MATE applet that shows traffic on a network device

Group:          Applications/Internet
License:        GPLv2+
URL:            http://pub.mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig, gettext, scrollkeeper, intltool
BuildRequires:  libgtop2-devel
BuildRequires:  mate-panel-devel >= 1.1.0
BuildRequires:  mate-doc-utils
BuildRequires:  wireless-tools-devel
BuildRequires:  mate-common

Requires:       hicolor-icon-theme

Requires(post): scrollkeeper
Requires(postun): scrollkeeper

Obsoletes: 		mate-netspeed-applet
Provides:  		mate-netspeed


# related to GNOME bz 600579 / Fedora #530920
Patch1: netspeed_applet-0.16-copy-qualpixbufs.patch
# related to GNOME bz 574462 / Fedora #647060
Patch3: netspeed_applet-0.16-details-bytes.patch

%description
netspeed is a little MATE applet that shows the traffic on a
specified network device (for example eth0) in kbytes/s.

%prep
%setup -q -n mate-netspeed-%{version}
%patch1 -p1 -b .copy-qualpixbufs
%patch3 -p1 -b .details-bytes
NOCONFIGURE=1 ./autogen.sh

%build
export 	LDFLAGS="-lm"
%configure \
	--disable-static \
	--disable-scrollkeeper



make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang mate-netspeed


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
scrollkeeper-update -q -o %{_datadir}/omf/mate_netspeed_applet || : 


%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
scrollkeeper-update -q || :


%clean
rm -rf $RPM_BUILD_ROOT


%files -f mate-netspeed.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
# ChangeLog discontinued
%doc %{_datadir}/mate/help/mate_netspeed_applet/*
%{_libexecdir}/*
%{_libdir}/matecomponent/servers/*
%{_datadir}/icons/hicolor/*
%{_datadir}/omf/mate_netspeed_applet/*


%changelog
* Sun Mar 11 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0

* Sun Feb 19 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.1-2
- rebuild for enable builds for .i686
- enable fedora patches

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-applet-netspeed.spec based on gnome-applet-netspeed-0.16-5.fc14 spec

* Wed Nov  3 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 0.16-5
- Fix incorrect labelling in Device Details dialog (#647060),
  ignore "bits instead of bytes" setting for Bytes in/out labels.

