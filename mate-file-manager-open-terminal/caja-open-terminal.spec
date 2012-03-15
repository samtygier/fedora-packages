Name:           caja-open-terminal
Version:        1.1.0
Release:        2%{?dist}
Summary:        Caja extension for an open terminal shortcut

Group:          User Interface/Desktops
License:        GPLv2+
URL:            https://github.com/Perberos/Mate-Desktop-Environment
Source0:	%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	intltool
# need extensions
BuildRequires:	caja-devel
BuildRequires:  autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	mate-conf-devel
BuildRequires: 	mate-common
BuildRequires: 	mate-desktop-devel
Requires(pre): 	mate-conf
Requires(post): mate-conf
Requires(preun): mate-conf

%description
The caja-open-terminal extension provides a right-click "Open
Terminal" option for caja users who prefer that option.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/caja/extensions-2.0/*.{l,}a

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
              %{_sysconfdir}/mateconf/schemas/%{name}.schemas > /dev/null || :
fi

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
mateconftool-2 \
	    --makefile-install-rule \
	    %{_sysconfdir}/mateconf/schemas/%{name}.schemas >/dev/null || :

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
              %{_sysconfdir}/mateconf/schemas/%{name}.schemas > /dev/null || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS TODO
%config(noreplace) %{_sysconfdir}/mateconf/schemas/*
%{_libdir}/caja/extensions-2.0/*.so*

%changelog
* Mon Feb 13 2012 Wolfgang Ulbrich <info@raveit.de> - caja-open-terminal-1.1.0-2
- rebuild for enable builds for .i686

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- caja-open-terminal.spec based on nautilus-open-terminal-0.19-1.fc15 spec

* Tue Feb 22 2011 Cosimo Cecchi <cosimoc@redhat.com> - 0.19-1
- Update to 0.19

