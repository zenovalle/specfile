Summary: X.Org X11 libXfixes runtime library
Name: libXfixes
Version: 5.0.3
Release: 1
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkg-config
BuildRequires: util-macros, xorgproto, automake, autoconf
BuildRequires: libX11-devel

%description
X.Org X11 libXfixes runtime library

%package devel
Summary: X.Org X11 libXfixes development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
X.Org X11 libXfixes development package

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
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-, qsys, *none)
%{_includedir}/X11/extensions/Xfixes.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/Xfixes.3

%changelog
* Thu Aug 22 2019 Calvin Buckley <calvin@cmpct.info> - 5.0.3-1
- Create

