Name:          libXt
Version:       1.2.0
Release:       1
Summary:       X Toolkit Intrinsics library
Group:         System/Libraries
URL:           http://xorg.freedesktop.org
Source:        http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2
License:       MIT
BuildRequires: automake, autoconf
BuildRequires: glib2-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libX11-devel
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel
#BuildRequires: libuuid-devel
BuildRequires: libxcb-devel
BuildRequires: xorgproto
## AUTOBUILDREQ-END
Obsoletes:     libXorg
%description
X.Org Xt library.

%package devel
Summary:       Development files for the X Toolkit Intrinsics library
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
#Requires:       %lname = %version
Obsoletes:     libXorg-devel

%description devel
X.Org Xt library.

This package contains static libraries and header files need for development.

%prep
%setup -q

%build
#export DED_LD="ld -G -bnoentry -bexpall -b64"

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
%{_libdir}/libXt.so.6
#%{_bindir}/makestrs
%doc COPYING ChangeLog

%files devel
%defattr(-, qsys, *none)
#%{_libdir}/libXt.la
%{_libdir}/libXt.so
%{_includedir}/X11/*.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
# XXX
%{_datadir}/doc/libXt/*.xml

%changelog
* Sun Aug 04 2019 Calvin Buckley <calvin@cmpct.info> - 1.2.0-1
- Bump
- PASE

* Wed Apr 10 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.1.3-1
- Initial port on Aix6.1

* Mon May 02 2011 Silvan Calarco <silvan.calarco@mambasoft.it> 1.1.1-1mamba
- update to 1.1.1

