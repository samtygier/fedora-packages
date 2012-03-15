Name:           mate-calc
Version:        1.2.0
Release:        1%{?dist}
Summary:        A desktop calculator

Group:          Applications/System
License:        GPLv2+
URL:            http://pub.mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

BuildRequires: glib2-devel
BuildRequires: gtk2-devel
BuildRequires: libglade2-devel
BuildRequires: libsoup-devel
BuildRequires: desktop-file-utils
BuildRequires: mate-doc-utils
BuildRequires: gettext
BuildRequires: flex
BuildRequires: bison
BuildRequires: intltool
BuildRequires: mate-common

Requires(post): glib2
Requires(postun): glib2

%description
mate-calc is a powerful graphical calculator with financial, logical and
scientific modes. It uses a multiple precision package to do its arithmetic
to give a high degree of accuracy.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-scrollkeeper 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%find_lang mate-calc --all-name


%postun
glib-compile-schemas %{_datadir}/glib-2.0/schemas ||:

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas ||:


%files -f mate-calc.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/mate-calc
%{_bindir}/mate-calc-cmd
%{_bindir}/mate-calculator
%{_datadir}/applications/mate-calc.desktop
%{_datadir}/glib-2.0/schemas/org.mate.mate-calc.gschema.xml
%{_datadir}/mate-calc
%doc %{_mandir}/man1/mate-calc.1.gz
%{_datadir}/mate/help/mate-calc/*

%changelog
* Wed Mar 14 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to version 1.2.0

* Fri Feb 17 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-calc.spec based on gcalctool-5.32.0-1.fc14 spec

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 5.32.0-1
- Update to 5.32.0

