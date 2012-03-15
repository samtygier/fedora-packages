Name:           ffmpegthumbnailer-caja
Version:        1.2.0
Release:        1%{?dist}
Summary:        ffmpegthumbnailer-caja make thumbnails of video files in caja file manager

Group:          Development/Tools
BuildArch:      noarch
License:        GPL
URL: 			http://pub.mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

#change /usr/share/mateconf to /etc/mateconf
Patch1:			ffmpegthumbnailer-caja_mateconf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package install a MateConf schemas to use ffmpegthumbnailer to
make thumbnails of video files in caja file manager.

%prep
%setup -q
%patch1 -p1 -b .ffmpegthumbnailer-caja_mateconf

%build

make %{?_smp_mflags}

cp AUTHORS README

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/ffmpegthumbnailer-caja.schemas \
	> /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/ffmpegthumbnailer-caja.schemas \
	> /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/ffmpegthumbnailer-caja.schemas \
	> /dev/null || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS README
%{_sysconfdir}/mateconf/schemas/ffmpegthumbnailer-caja.schemas

%changelog
* Mon Mar 12 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0

* Thu Feb 11 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- correct %preun error

* Thu Jan 05 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- started building
