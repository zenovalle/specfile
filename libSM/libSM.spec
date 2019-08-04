Name:          libSM
Version:       1.2.3
Release:       1
Summary:       X.Org SM library
Group:         System/Libraries
URL:           http://x.org
Source:        http://ftp.x.org/pub/individual/lib/libSM-%{version}.tar.gz
License:       MIT
BuildRequires: xorgproto, automake, autoconf, libxslt
BuildRequires: xtrans >= 1.0
BuildRequires: libICE-devel >= 1.0.1
Obsoletes:     libXorg

%description
X.Org SM library.

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
X.Org SM library.

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
%{_libdir}/%{name}.so.6
%doc AUTHORS COPYING ChangeLog

%files devel
%defattr(-, qsys, *none)
#%{_libdir}/%{name}.la
%{_libdir}/%{name}.so
%{_includedir}/X11/SM/*.h
%{_libdir}/pkgconfig/*.pc
# XXX?
%{_datadir}/doc/libSM/*.xml

%changelog
* Sun Aug 04 2019 Calvin Buckley <calvin@cmpct.info> - 1.2.3-1
- Bump
- PASE

* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.1-1
- Update to version 1.2.1-1

* Thu Sep 20 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.2-2
- Add shr.o and shr_64.o AIX R7 libSM library to the new libSM.a library

* Fri Jul 20 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.2-1
- Initial port on Aix6.1

