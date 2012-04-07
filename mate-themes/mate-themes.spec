Summary: 	Themes for MATE
Name: 		mate-themes
Version: 	1.2.0
Release: 	3%{?dist}
URL: 		https://github.com/mate-desktop/mate-themes
Source: 	%{name}-%{version}.tar.xz
License: 	LGPLv2 and GPLv2
Group: 		User Interface/Desktops
BuildArch: 	noarch
# we need Berlin (Atlanta) marco-theme
Source1:	metacity-theme-1.xml

Requires: 	gtk2-engines
Requires: 	mate-icon-theme

BuildRequires: 	autoconf
BuildRequires: 	automake
BuildRequires: 	intltool
BuildRequires: 	pkgconfig
BuildRequires: 	gtk2-devel
BuildRequires: 	libtool
BuildRequires: 	gettext
BuildRequires: 	gtk2-engines-devel
BuildRequires: 	icon-naming-utils
BuildRequires: 	mate-common

Patch0: 		mate-themes_rename_glider_to_sailplane.patch
Patch1:			mate-themes_change_atlanta_to_berlin.patch

%description
The mate-themes package contains a collection of desktop themes for MATE.
These themes can change the appearance of application widgets, icons, window
borders, cursors, etc.

%package 	legacy
Summary: 	Old names for icons in mate-themes
Group: 		User Interface/Desktops
Requires: 	%{name} = %{version}-%{release}

%description legacy
This package contains symlinks to make the icons in mate-themes
available under old names.

%prep
%setup -q
%patch0 -p1 -b .mate-themes_rename_glider_to_sailplane
%patch1 -p1 -b .mate-themes_change_atlanta_to_berlin
NOCONFIGURE=1 ./autogen.sh

%build
%configure

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# create Berlin dir
mkdir -p $RPM_BUILD_ROOT%{_datadir}/themes/Berlin
mkdir -p $RPM_BUILD_ROOT%{_datadir}/themes/Berlin/metacity-1
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/themes/Berlin/metacity-1/metacity-theme-1.xml

# Clearlooks gtk theme is in gtk2-engines
#rm -rf $RPM_BUILD_ROOT%{_datadir}/themes/Clearlooks/gtk-2.0
#rm -f $RPM_BUILD_ROOT%{_datadir}/themes/ThinIce/README.html
#rm -f $RPM_BUILD_ROOT%{_datadir}/themes/ThinIce/ICON.png
# Remove the test theme
#rm -rf $RPM_BUILD_ROOT%{_datadir}/themes/MateClearlooksTest/


# add legacy symlinks
for size in 16x16 22x22 24x24 32x32 48x48 256x256; do
  for context in actions apps devices places status; do
    (cd $RPM_BUILD_ROOT%{_datadir}/icons/Fog/$size
     icon-name-mapping -c $context)
  done
done

# we want to own the icon caches
for dir in $RPM_BUILD_ROOT%{_datadir}/icons/*; do
  touch $dir/icon-theme.cache
done

(cd $RPM_BUILD_ROOT%{_datadir}
 echo "%%defattr(-,root,root,-)"
 find icons/Fog -type l -and -not -name "gtk-\*" -printf "%%%%{_datadir}/%%p\n"
) > legacy.txt


%find_lang %{name}

%post
for icon_theme in Quid Fog ContrastHighLargePrint ContrastHighLargePrintInverse ContrastHigh-SVG ; do
  touch --no-create %{_datadir}/icons/${icon_theme} &> /dev/null || :
done

%postun
if [ $1 -eq 0 ]; then
for icon_theme in Quid Fog ContrastHighLargePrint ContrastHighLargePrintInverse ContrastHigh-SVG ; do
  touch --no-create %{_datadir}/icons/${icon_theme} &> /dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/${icon_theme} &> /dev/null || :
done
fi

%posttrans
for icon_theme in Quid Fog ContrastHighLargePrint ContrastHighLargePrintInverse ContrastHigh-SVG ; do
  gtk-update-icon-cache %{_datadir}/icons/${icon_theme} &> /dev/null || :
done


%files -f  %{name}.lang
%defattr(-,root,root,-)
%{_datadir}/icons/Quid/
%{_datadir}/icons/Fog/
%{_datadir}/icons/ContrastHigh-SVG/
%{_datadir}/icons/ContrastHighLargePrint/
%{_datadir}/icons/ContrastHigh/
%{_datadir}/icons/ContrastHighInverse/
%{_datadir}/icons/MateLargePrint/
%{_datadir}/icons/ContrastHighLargePrintInverse/
%{_datadir}/icons/mate/icon-theme.cache
%{_datadir}/icons/mate/cursors/
%{_datadir}/themes/ContrastHigh/
%{_datadir}/themes/ContrastHighInverse/
%{_datadir}/themes/ContrastHighLargePrint/
%{_datadir}/themes/ContrastHighLargePrintInverse/
%{_datadir}/themes/Reverse/
%{_datadir}/themes/ContrastLow/
%{_datadir}/themes/ContrastLowLargePrint/
%{_datadir}/themes/PrintLarge/
%{_datadir}/themes/Aldabra/
%{_datadir}/themes/Inverted/


# themes where the gtk theme is shipped with the engine
%{_datadir}/themes/TraditionalOk/*
%{_datadir}/themes/Quid/*
%{_datadir}/themes/Fog/*

# others
%{_datadir}/themes/Sailplane
%{_datadir}/themes/Shiny
%{_datadir}/themes/TraditionalOkClassic
%{_datadir}/themes/Simply
%{_datadir}/themes/Berlin/metacity-1/metacity-theme-1.xml

%doc AUTHORS COPYING NEWS README

%files legacy -f legacy.txt

%changelog
* Sat Mar 24 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-3
- update to latest git version
- themes are renamed
- add Berlin (Atlanta) marco theme for contrasthigh

* Thu Mar 01 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-2
- test build

* Thu Mar 01 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update version to 1.2

* Sun Feb 12 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-3
- using a patch for further actions

* Sun Feb 12 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- move directories to avoid conflicts with gnome-themes

* Wed Jan 04 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-themes.spec based on gnome-themes-2.32.0-7.fc16 spec

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-7
- Rebuilt for glibc bug#747377

