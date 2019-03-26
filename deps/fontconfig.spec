# XXX: Holding off on fc 2.13.1 until >= ft 2.8 RPMs appear
%define freetype_version 2.7-1

Summary: Font configuration and customization library
Name: fontconfig
Version: 2.12.6
Release: 3
License: MIT
Group: System Environment/Libraries
Source0: http://fontconfig.org/release/%{name}-%{version}.tar.bz2
URL: http://fontconfig.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gawk, make-gnu, sed-gnu, grep-gnu, gperf, bash, bzip2, automake, autoconf, libtool
#BuildRequires: gcc >= 4.5.4-1
# XXX: Lowered this check from 2.2.4-1
BuildRequires: expat-devel >= 2.2
BuildRequires: freetype-devel >= %{freetype_version}

Requires: libexpat1 >= 2.2
Requires: libfreetype6 >= %{freetype_version}
#Requires: libgcc >= 4.5.4-1

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.

%package devel
Summary: Font configuration and customization library
Group: Development/Libraries
Requires: fontconfig = %{version}-%{release}
Requires: expat-devel >= 2.2
Requires: freetype-devel >= %{freetype_version}
Requires: pkg-config

%description devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.

%prep
%setup -q

%build

export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

# we don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

# Needed for struct random_data in stdlib.h
export CPPFLAGS="-D_ALL_SOURCE -pthread"

autoreconf -fiv

%configure \
    LDFLAGS="-maix${OBJECT_MODE} -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static \
    --with-add-fonts=/QOpenSys/usr/lib/X11/fonts/TrueType,/QOpenSys/usr/lib/X11/fonts/Type1

%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%post

umask 0022
mkdir -p %{_localstatedir}/cache/fontconfig
# Remove stale caches
rm -f %{_localstatedir}/cache/fontconfig/????????????????????????????????*.cache-?
rm -f %{_localstatedir}/cache/fontconfig/stamp
# Regenerate font cache
# XXX: Remove Perzl-ism?
# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x /QOpenSys/pkgs/bin/fc-cache ] && /QOpenSys/pkgs/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
  HOME=/ /QOpenSys/pkgs/bin/fc-cache -f
fi


%files
%defattr(-, qsys, *none)
%doc README AUTHORS COPYING 
%doc doc/fontconfig-user.txt doc/fontconfig-user.html
%doc doc/fontconfig-user.pdf
%{_bindir}/fc-*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/conf.avail
%config %{_datadir}/%{name}/conf.avail/*.conf
%dir %{_sysconfdir}/fonts
%config %{_sysconfdir}/fonts/fonts.conf
# XXX: Include /QOpenSys/etc/fonts/fonts.conf.bak ?
%dir %{_sysconfdir}/fonts/conf.d
%config(noreplace) %{_sysconfdir}/fonts/conf.d/*.conf
%{_datadir}/xml/fontconfig/fonts.dtd
%{_libdir}/libfontconfig.so.1
%doc %{_sysconfdir}/fonts/conf.d/README
%dir %{_localstatedir}/cache/fontconfig
%{_mandir}/man1/*
%{_mandir}/man5/*
# XXX: More redundant docs...
%{_datadir}/doc/fontconfig/fontconfig-user.*

%files devel
%defattr(-, qsys, *none)
%doc doc/fontconfig-devel.txt doc/fontconfig-devel
%doc doc/fontconfig-devel.pdf
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/fontconfig.pc
%{_includedir}/fontconfig/*
%{_mandir}/man3/*
%{_datadir}/doc/fontconfig/fontconfig-devel.*
%{_datadir}/doc/fontconfig/fontconfig-devel/*

%changelog
* Tue Mar 26 2019 Calvin Buckley <calvin@cmpct.info> - 2.12.6-3
- Conversion for PASE

* Thu Nov 09 2017 Michael Perzl <michael@perzl.org> - 2.12.6-2
- changes to the shipped libtool *.la files

* Fri Sep 22 2017 Michael Perzl <michael@perzl.org> - 2.12.6-1
- updated to version 2.12.6

* Fri Sep 22 2017 Michael Perzl <michael@perzl.org> - 2.12.5-1
- updated to version 2.12.5

* Wed Jul 05 2017 Michael Perzl <michael@perzl.org> - 2.12.4-1
- updated to version 2.12.4

* Wed Jul 05 2017 Michael Perzl <michael@perzl.org> - 2.12.3-1
- updated to version 2.12.3

* Wed Jul 05 2017 Michael Perzl <michael@perzl.org> - 2.12.2-1
- updated to version 2.12.2

* Thu Nov 17 2016 Michael Perzl <michael@perzl.org> - 2.12.1-1
- updated to version 2.12.1

* Mon Jul 04 2016 Michael Perzl <michael@perzl.org> - 2.12.0-1
- updated to version 2.12.0

* Tue May 24 2016 Michael Perzl <michael@perzl.org> - 2.11.1-1
- updated to version 2.11.1

* Tue May 24 2016 Michael Perzl <michael@perzl.org> - 2.11.0-1
- updated to version 2.11.0

* Mon Jan 07 2013 Michael Perzl <michael@perzl.org> - 2.10.2-1
- updated to version 2.10.2

* Wed Aug 29 2012 Michael Perzl <michael@perzl.org> - 2.10.1-1
- updated to version 2.10.1

* Thu Apr 19 2012 Michael Perzl <michael@perzl.org> - 2.9.0-1
- updated to version 2.9.0

* Mon Jul 04 2011 Michael Perzl <michael@perzl.org> - 2.8.0-2
- added missing 64-bit pkg-config file and RTL-style shared libraries

* Thu Nov 19 2009 Michael Perzl <michael@perzl.org> - 2.8.0-1
- updated to version 2.8.0

* Thu Nov 19 2009 Michael Perzl <michael@perzl.org> - 2.7.3-1
- updated to version 2.7.3

* Wed Sep 02 2009 Michael Perzl <michael@perzl.org> - 2.7.2-1
- updated to version 2.7.2

* Mon Jul 06 2009 Michael Perzl <michael@perzl.org> - 2.7.0-1
- updated to version 2.7.0

* Tue Jul 08 2008 Michael Perzl <michael@perzl.org> - 2.6.0-1
- updated to version 2.6.0

* Wed Apr 23 2008 Michael Perzl <michael@perzl.org> - 2.5.0-2
- some minor spec file fixes

* Tue Apr 01 2008 Michael Perzl <michael@perzl.org> - 2.5.0-1
- first version for AIX V5.1 and higher

