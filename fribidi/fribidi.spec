Summary: Library implementing the Unicode Bidirectional Algorithm
Name: fribidi
Version: 1.0.8
Release: 1qsecofr
URL: https://github.com/fribidi/fribidi
Source0: https://github.com/fribidi/fribidi/releases/download/v%{version}/%{name}-%{version}.tar.bz2
License: LGPLv2+
Group: System Environment/Libraries
BuildRequires: pkg-config, automake, autoconf

%description
A library to handle bidirectional scripts (for example Hebrew, Arabic),
so that the display is done in the proper way; while the text data itself
is always written in logical order.

%package devel
Summary: Libraries and include files for FriBidi
Group: System Environment/Libraries
Requires: %name = %{version}-%{release}
Requires: pkg-config

%description devel
Include files and libraries needed for developing applications which use
FriBidi.

%prep
%setup -q

%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -fiv .
# all source for struct tms
%configure \
  CPPFLAGS="-D_ALL_SOURCE" \
  LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
  --with-aix-soname=svr4 \
  --enable-shared --disable-static

%make_build

(gmake check || true)

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc README AUTHORS COPYING ChangeLog THANKS NEWS TODO
%{_bindir}/*
%{_libdir}/libfribidi.so.*

%files devel
%defattr(-, qsys, *none)
%{_includedir}/*
%{_libdir}/libfribidi.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Wed Feb 05 2020 Calvin Buckey <calvin@cmpct.info> - 1.0.8-1qsecofr
- Bump

* Mon Aug 05 2019 Calvin Buckley <calvin@cmpct.info> - 1.0.5-1
- Bump
- PASE

* Thu Mar 27 2014 Michael Perzl <michael@perzl.org> - 0.19.6-1
- updated to version 0.19.6

* Fri May 03 2013 Michael Perzl <michael@perzl.org> - 0.19.5-1
- updated to version 0.19.5

* Mon Nov 16 2009 Michael Perzl <michael@perzl.org> - 0.19.2-1
- first version for AIX V5.1 and higher

