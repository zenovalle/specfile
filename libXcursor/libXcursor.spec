Summary: X.Org X11 libXcursor runtime library
Name: libXcursor
Version: 1.2.0
Release: 1
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkg-config
BuildRequires: util-macros, xorgproto, automake, autoconf
BuildRequires: libXrender-devel >= 0.9.5
BuildRequires: libX11-devel, libXfixes-devel

%description
X.Org X11 libXcursor runtime library

%package devel
Summary: X.Org X11 libXcursor development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
X.Org X11 libXcursor development package

%prep
%setup -q


%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -fiv .
%configure \
  CPPFLAGS=-I%{prefix}/libiconv \
  LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
  --with-aix-soname=svr4 \
  --enable-shared --disable-static

%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc AUTHORS COPYING README.md ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-, qsys, *none)
%dir %{_includedir}/X11/Xcursor
%{_includedir}/X11/Xcursor/Xcursor.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/Xcursor*.3*

%changelog
* Thu Aug 22 2019 Calvin Buckley <calvin@cmpct.info> - 1.2.0-1
- Bump
- PASE

* Tue Oct 18 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.1.11-1
- Initial port on Aix5.3

