Name:          libXext
Version:       1.3.4
Release:       1
Summary:       X.Org Xext library
Group:         System/Libraries
URL:           http://x.org
Source:        http://ftp.x.org/pub/individual/lib/libXext-%{version}.tar.bz2
License:       MIT
Obsoletes:     libXorg

BuildRequires: libxslt, gcc-aix, autoconf, automake, bzip2
BuildRequires: libX11-devel, libxcb-devel, util-macros, xorgproto

%description
X.Org Xext library.

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
Obsoletes:     libXorg-devel

%description devel
X.Org Xext library.

This package contains static libraries and header files need for development.

%prep
%setup -q

%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -fiv
%configure \
    LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static
%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm
%files
%defattr(-, qsys, *none)
%doc AUTHORS COPYING ChangeLog
%{_libdir}/libXext.so.6

%files devel
%defattr(-, qsys, *none)
%{_includedir}/X11/extensions/*.h
#%{_libdir}/libXext.la
%{_libdir}/libXext.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/man/man3/*
%dir %{_datadir}/doc/libXext
%{_datadir}/doc/libXext/*

%changelog
* Tue Jul 30 2019 Calvin Buckley <calvin@cmpct.info> - 1.3.4-1
- Bump
- PASE

* Thu Apr 11 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.3.1-1
- Initial port on Aix6.1

* Tue May 10 2011 Automatic Build System <autodist@...> 1.3.0-1mamba
- automatic update by autodist

* Fri Dec 10 2010 Automatic Build System <autodist@...> 1.2.0-1mamba
- automatic update by autodist

* Fri Jul 02 2010 Silvan Calarco <silvan.calarco@...> 1.1.2-2mamba
- rebuilt to add pkgconfig provides

* Sat Jun 05 2010 Automatic Build System <autodist@...> 1.1.2-1mamba
- automatic update by autodist

