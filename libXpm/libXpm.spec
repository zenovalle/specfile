Summary: X.Org X11 libXpm runtime library
Name: libXpm
Version: 3.5.13
Release: 1qsecofr
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkg-config
BuildRequires: util-macros, xorgproto, automake, autoconf
BuildRequires: libX11-devel, libXt-devel, libXext-devel, libintl-devel, libxslt

%description
X.Org X11 libXpm runtime library

%package devel
Summary: X.Org X11 libXpm development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
X.Org X11 libXpm development package

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
%doc COPYING README.md ChangeLog
%{_libdir}/*.so.*
%{_bindir}/cxpm
%{_bindir}/sxpm

%files devel
%defattr(-, qsys, *none)
%{_includedir}/X11/xpm.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
# no man3?
%{_mandir}/man1/*.1*

%changelog
* Thu Aug 22 2019 Calvin Buckley <calvin@cmpct.info> - 3.5.13-1qsecofr
- Init

