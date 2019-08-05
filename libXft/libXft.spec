Summary: X.Org X11 libXft runtime library
Name: libXft
Version: 2.3.3
Release: 1
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
Source0: http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: libXrender-devel >= 0.9.5
BuildRequires: libX11-devel >= 1.5
BuildRequires: freetype-devel >= 2.3.5
BuildRequires: fontconfig-devel >= 2.5.0
BuildRequires: pkg-config libxslt xorgproto util-macros
BuildRequires: autoconf automake libtool

#Requires: libXrender >= 0.9.5
#Requires: freetype2 >= 2.3.5
#Requires: fontconfig >= 2.5.0
#Requires: libX11 >= 1.5

Provides: xft

%description
X.Org X11 libXft runtime library

%package devel
Summary: X.Org X11 libXft development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXft development package

%prep
%setup -q

%build

export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -fiv
%configure \
    CPPFLAGS="-pthread" \
    LDFLAGS="-pthread -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static
%make_build

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc AUTHORS COPYING README.md
%{_libdir}/libXft.so.2

%files devel
%defattr(-, qsys, *none)
%{_includedir}/X11/Xft/Xft.h
%{_includedir}/X11/Xft/XftCompat.h
%{_libdir}/libXft.so
%{_libdir}/pkgconfig/xft.pc
%{_mandir}/man3/Xft.3

%changelog
* Sun Aug 04 2019 Calvin Buckley <calvin@cmpct.info> 2.3.3-1
- PASE

* Tue Apr 12 2016 Matthieu Sarter <matthieu.sarter.external@atos.net>  2.3.2-3
- Updated to version 2.3.2
- Fixed libraries references to use /opt/freeware/lib/libXrender.a instead of /usr/lib/libXrender.a

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net>  2.2.0-3
- Initial port on Aix6.1

* Mon Sep 26 2011 Patricia Cugny <patricia.cugny@bull.net> 2.2.0-2
- rebuild for compatibility with new libiconv.a 1.13.1-2
