Name:          libICE
Version:       1.0.10
Release:       1
Summary:       X.Org ICE library
Group:         System/Libraries
URL:           http://x.org
Source:        ftp://ftp.x.org/pub/individual/lib/libICE-%{version}.tar.bz2
License:       MIT
BuildRequires: xorgproto, autoconf, automake, xtrans, libxslt, bzip2
BuildRequires: xtrans >= 1.0
Obsoletes:     libXorg

%description
X.Org ICE library.

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
X.Org ICE library.

This package contains static libraries and header files need for development.

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

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%{_libdir}/libICE.so.6
%doc AUTHORS COPYING ChangeLog
%{_datadir}/doc/libICE

%files devel
%defattr(-, qsys, *none)
#%{_libdir}/libICE.la
%{_libdir}/libICE.so
%{_includedir}/X11/ICE/*.h
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun Aug 04 2019 Calvin Buckley <calvin@cmpct.info> - 1.0.10-1
- Bump
- PASE

* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.8-1
- Update to version 1.0.8-1

* Thu Sep 20 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.7-2
- Add shr.o and shr_64.o AIX R7 libICE library to the new libICE.a library

* Fri Jul 20 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.7-1
- Initial port on Aix6.1


