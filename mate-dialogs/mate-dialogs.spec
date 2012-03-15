Name:		mate-dialogs
Version:	1.2.0
Release:	1%{?dist}
Summary:	Display dialog boxes from shell scripts
Group:		Applications/System
License:	LGPLv2+
URL:		http://mate-desktop.or
Source:		http://pub.mate-desktop.org/releases/1.2/%{name}-%{version}.tar.xz

BuildRequires: mate-doc-utils >= 1.0.0
BuildRequires: glib2-devel >= 2.7.3
BuildRequires: gtk2-devel
BuildRequires: libmatenotify-devel >= 1.1.0
BuildRequires: scrollkeeper
BuildRequires: which
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: mate-common

%description
mate-dialogs lets you display Gtk+ dialog boxes from the command line and through
shell scripts. It is similar to gdialog, but is intended to be saner. It comes
from the same family as dialog, Xdialog, and cdialog.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build

%configure \
	--disable-static \
	--enable-libmatenotify

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# we don't want a perl dependency just for this
rm $RPM_BUILD_ROOT%{_bindir}/gdialog

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

%find_lang mate-dialogs


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS NEWS THANKS README
%{_bindir}/matedialog
%{_datadir}/matedialog
%{_mandir}/man1/matedialog.1.gz
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/mate/help/matedialog/*/figures/*.png
%{_datadir}/mate/help/matedialog/*/*.xml
%{_datadir}/omf/matedialog/*.omf


%changelog
* Fri Mar 09 2012 Wolfgang Ulbrich <info@raveit.de> - 1.2.0-1
- update to 1.2.0 version

* Sat Feb 18 2012 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-2
- rebuild for enable builds for .i686

* Sun Dec 25 2011 Wolfgang Ulbrich <info@raveit.de> - 1.1.0-1
- mate-dialogs.spec based on zenity-2.32.0-1.fc14 spec

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

