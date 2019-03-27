Summary: X.Org X11 libXrender runtime library
Name: libXrender
Version: 0.9.10
Release: 3
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: bash, pkg-config, tar-gnu, xorg-compat-aix >= 1.2, util-macros
BuildRequires: tar-gnu, automake, autoconf, m4-gnu, gcc-aix
BuildRequires: renderproto >= 0.11.1-2

Provides: xrender

%description
X.Org X11 libXrender runtime library

%package devel
Summary: X.Org X11 libXrender development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config
Requires: renderproto >= 0.11.1-2

%description devel
X.Org X11 libXrender development package

%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q

%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

# Shared libraries don't like to work right in svr4 sonames without autoreconf,
# but we also don't have xorg-macros - that's what we patched out.
autoreconf -fiv
%configure \
    LDFLAGS="-maix${OBJECT_MODE} -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static
%make_build

# We shouldn't need the crazy steps with merging member objects like what Perzl
# does, because we build an `.so` instead of an `.a`.

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc AUTHORS COPYING ChangeLog
%{_libdir}/libXrender.so.1

%files devel
%defattr(-, qsys, *none)
%{_includedir}/X11/extensions/Xrender.h
%{_libdir}/pkgconfig/xrender.pc
%{_libdir}/libXrender.so
%{_datadir}/doc/libXrender/libXrender.txt

%changelog
* Wed Mar 27 2019 Calvin Buckley <calvin@cmpct.info> - 0.9.10-3
- Use xorg-macros instead of patching them out

* Wed Mar 27 2019 Calvin Buckley <calvin@cmpct.info> - 0.9.10-2
- De-AIX, Rochester conventions

* Fri Nov 18 2016 Michael Perzl <michael@perzl.org> - 0.9.10-1
- updated to version 0.9.10

* Sat Dec 26 2015 Michael Perzl <michael@perzl.org> - 0.9.9-1
- updated to version 0.9.9

* Thu Aug 22 2013 Michael Perzl <michael@perzl.org> - 0.9.8-1
- updated to version 0.9.8

* Mon Aug 13 2012 Michael Perzl <michael@perzl.org> - 0.9.7-2
- added compatibility shared members for AIX >= 6.1 as starting with AIX 6.1
  AIX has a system version of libXrender

* Sun Jun 03 2012 Michael Perzl <michael@perzl.org> - 0.9.7-1
- updated to version 0.9.7

* Wed Nov 03 2010 Michael Perzl <michael@perzl.org> - 0.9.6-1
- updated to version 0.9.6

* Mon Nov 09 2009 Michael Perzl <michael@perzl.org> - 0.9.5-1
- updated to version 0.9.5
- fixed a AIX V6.1 compatibility issue and built a separate AIX V6.1 version

* Fri Nov 06 2009 Michael Perzl <michael@perzl.org> - 0.9.4-2
- fixed a compatibility issue with the original AIX Toolbox xrender package

* Sat Apr 05 2008 Michael Perzl <michael@perzl.org> - 0.9.4-1
- first version for AIX V5.1 and higher

