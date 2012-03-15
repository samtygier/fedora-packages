Name:				caja-share
Version:			0.7.3
Release:			2%{?dist}
Summary:			Easy sharing folder via Samba (CIFS protocol)
Group:				Applications/File
License:			GPLv2+
URL:				https://github.com/mate-desktop/mate-file-manager-share
Source0:			%{name}-%{version}.tar.gz
Source1:			caja-share-setup-instructions
Source2:			caja-share-smb.conf.example
BuildRoot:			%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:		libdaemon-devel
BuildRequires:		caja-devel
BuildRequires:		gettext
BuildRequires:		perl(XML::Parser)
BuildRequires:		gtk+-devel
BuildRequires:		libglade2-devel
BuildRequires: 	    mate-common
BuildRequires:		intltool
Requires:			samba >= 3.6.1

%description
Caja extension designed for easier folders 
sharing via Samba (CIFS protocol) in *NIX systems.

%prep
%setup -q
cp %{SOURCE1} SETUP
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
rm $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0/lib%{name}.la
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/samba/
cp %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/samba/
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO SETUP
%{_libdir}/caja/extensions-2.0/*
%{_datadir}/caja-share/
%{_sysconfdir}/samba/%{name}-smb.conf.example


%changelog
* Mon Feb 13 2012 Wolfgang Ulbrich <info@raveit.de> - caja-share-1.1.0-2
- rebuild for enable builds for .i686

* Thu Jan 19 2012 Wolfgang Ulbrich <info@raveit.de> - 0.7.3-1
- caja-share.spec based on nautilus-share-0.7.2-13.fc10 spec

* Wed Nov 12 2008 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 0.7.2-13
- set icon to "folder-remote"
- don't use extensions-1.0 directory (fixes #447072)

