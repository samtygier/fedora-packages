%define glib2_version 2.22.0
%define desktop_file_utils_version 0.9
%define gtksourceview_version 2.9.7
%define pygtk_version 2.12.0
%define pygobject_version 2.15.4
%define pygtksourceview_version 2.9.2
%define mate_python_desktop_version 1.1.0
%define mate_doc_utils_version 1.1.0
%define mateconf_version 1.1.0
%define enchant_version 1.2.0
%define isocodes_version 0.35

Summary:	Text editor for the MATE desktop
Name:		pluma
Version: 	1.2.0
Release: 	1%{?dist}
License:	GPLv2+ and GFDL
Group:		Applications/Editors
URL:		http://pub.mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

Requires(post):			mate-conf >= %{mateconf_version}
Requires(pre):			mate-conf >= %{mateconf_version}
Requires(preun):		mate-conf >= %{mateconf_version}
Requires(post):         desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun):       desktop-file-utils >= %{desktop_file_utils_version}

# http://bugzilla.gnome.org/show_bug.cgi?id=587053
Patch3: print-to-file.patch


BuildRequires: mate-common
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel
BuildRequires: mate-conf-devel >= 1.1.0
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: enchant-devel >= %{enchant_version}
BuildRequires: iso-codes-devel >= %{isocodes_version}
BuildRequires: gtksourceview2-devel >= %{gtksourceview_version}
BuildRequires: scrollkeeper gettext
BuildRequires: pygtk2-devel >= %{pygtk_version}
BuildRequires: pygobject2-devel >= %{pygobject_version}
BuildRequires: pygtksourceview-devel >= %{pygtksourceview_version}
BuildRequires: python-devel
BuildRequires: mate-doc-utils >= %{mate_doc_utils_version}
BuildRequires: autoconf, automake, libtool
BuildRequires: intltool
BuildRequires: libxml-devel
BuildRequires: gtk+-devel >= 2.16.0
BuildRequires: mate-common
BuildRequires: gtk-doc

Requires: pygtk2 >= %{pygtk_version}
Requires: pygobject2 >= %{pygtk_version}
Requires: pygtksourceview >= %{pygtksourceview_version}
#Requires: mate-python2-desktop >= %{mate_python_desktop_version}
# the run-command plugin uses  mate-dialogs
Requires: mate-dialogs


%description
pluma is a small, but powerful text editor designed specifically for
the MATE desktop. It has most standard text editor functions and fully
supports international text in Unicode. Advanced features include syntax
highlighting and automatic indentation of source code, printing and editing
of multiple documents in one window.

pluma is extensible through a plugin system, which currently includes
support for spell checking, comparing files, viewing CVS ChangeLogs, and
adjusting indentation levels. Further plugins can be found in the
gedit-plugins package.

%package devel
Summary: Support for developing plugins for the pluma text editor
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtksourceview2-devel >= %{gtksourceview_version}
Requires: pygtk2-devel >= %{pygtk_version}
Requires: pkgconfig
Requires: gtk-doc

%description devel
pluma is a small, but powerful text editor for the MATE desktop.
This package allows you to develop plugins that add new functionality
to gedit.

Install pluma-devel if you want to write plugins for pluma.

%prep
%setup -n pluma-%{version} -q
NOCONFIGURE=1 ./autogen.sh

%patch3 -p1 -b .print-to-file

autoreconf -f -i
intltoolize -f

%build
%configure\
	--disable-static \
	--disable-scrollkeeper \
	--enable-python


make %{_smp_mflags}

# strip unneeded translations from .mo files
# ideally intltool (ha!) would do that for us
# http://bugzilla.gnome.org/show_bug.cgi?id=474987
cd po
grep -v ".*[.]desktop[.]in.*\|.*[.]server[.]in[.]in$" POTFILES.in > POTFILES.keep
mv POTFILES.keep POTFILES.in
intltool-update --pot
for p in *.po; do
  msgmerge $p %{name}.pot > $p.out
  msgfmt -o `basename $p .po`.gmo $p.out
done
cd ..

%install
rm -rf $RPM_BUILD_ROOT
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL


## clean up all the static libs for plugins (workaround for no -module)
/bin/rm -f `find $RPM_BUILD_ROOT%{_libdir} -name "*.a"`
/bin/rm -f `find $RPM_BUILD_ROOT%{_libdir} -name "*.la"`

/bin/rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

# save space by linking identical images in translated docs
helpdir=$RPM_BUILD_ROOT%{_datadir}/mate/help/%{name}
for f in $helpdir/C/figures/*.png; do
  b="$(basename $f)"
  for d in $helpdir/*; do
    if [ -d "$d" -a "$d" != "$helpdir/C" ]; then
      g="$d/figures/$b"
      if [ -f "$g" ]; then
        if cmp -s $f $g; then
          rm "$g"; ln -s "../../C/figures/$b" "$g"
        fi
      fi
    fi
  done
done

%find_lang %{name} --all-name

%pre
if [ "$1" -gt 1 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  	mateconftool-2 --makefile-uninstall-rule \
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/pluma-file-browser.schemas \
	%{_sysconfdir}/mateconf/schemas/pluma.schemas \
	> /dev/null || :
fi

%post
export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
	mateconftool-2 --makefile-install-rule \
	%{_sysconfdir}/mateconf/schemas/pluma-file-browser.schemas \
	%{_sysconfdir}/mateconf/schemas/pluma.schemas \
	> /dev/null || :
update-desktop-database -q
touch --no-create %{_datadir}/pluma/icons >&/dev/null || :

%preun
if [ "$1" -eq 0 ]; then
  export MATECONF_CONFIG_SOURCE=`mateconftool-2 --get-default-source`
  mateconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/mateconf/schemas/pluma-file-browser.schemas \
	%{_sysconfdir}/mateconf/schemas/pluma.schemas \
	> /dev/null || :
fi

%postun
update-desktop-database -q
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/pluma/icons >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/pluma/icons >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/pluma/icons >&/dev/null || :

%files -f %{name}.lang
%defattr(-, root, root)
%doc README COPYING AUTHORS
%{_datadir}/pluma
%{_datadir}/applications/pluma.desktop
%{_mandir}/man1/*
%{_libdir}/pluma
%{_libexecdir}/pluma
%{_bindir}/*
%{_sysconfdir}/mateconf/schemas/pluma-file-browser.schemas
%{_sysconfdir}/mateconf/schemas/pluma.schemas
%{_datadir}/mate/help/pluma
%{_datadir}/omf/pluma/*



%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/pluma.pc
%{_includedir}/pluma/pluma/*


%changelog
* Wed Mar 14 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Tue Feb 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686
- enable fedora patches

* Sat Jan 21 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- pluma.spec based on gedit-2.31.5-1.fc14 spec

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-1
- Update to 2.31.5

