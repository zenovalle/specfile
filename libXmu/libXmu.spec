Name:          libXmu
Version:       1.1.3
Release:       1
Summary:       X Toolkit Intrinsics library
Group:         System/Libraries
URL:           http://xorg.freedesktop.org
Source:        http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2
License:       MIT
BuildRequires: automake, autoconf, util-macros
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXt-devel
BuildRequires: xorgproto
## AUTOBUILDREQ-END
Obsoletes:     libXorg
%description
X.Org Xmu library.

%package devel
Summary:       Development files for the X Toolkit Intrinsics library
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
#Requires:       %lname = %version
Obsoletes:     libXorg-devel

%description devel
X.Org Xmu library.

This package contains libraries and header files need for development.

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
%{_libdir}/libXmu.so.6
%{_libdir}/libXmuu.so.1
%doc COPYING ChangeLog

%files devel
%defattr(-, qsys, *none)
%{_libdir}/libXmu.so
%{_libdir}/libXmuu.so
%{_includedir}/X11/Xmu/*.h
%{_libdir}/pkgconfig/*.pc
#%{_mandir}/man3/*
# XXX
%{_datadir}/doc/libXmu/*

%changelog
* Mon Aug 05 2019 Calvin Buckley <calvin@cmpct.info> - 1.1.3-1
- Create

