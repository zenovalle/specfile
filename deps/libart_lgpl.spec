Summary: Library of graphics routines used by libgnomecanvas
Name: libart_lgpl
Version: 2.3.21
Release: 2
URL: http://www.gnome.org/
Source0: http://ftp.gnome.org/pub/gnome/sources/libart_lgpl/2.3/%{name}-%{version}.tar.bz2
Source1: http://ftp.gnome.org/pub/gnome/sources/libart_lgpl/2.3/%{name}-%{version}.sha256sum
License: LGPLv2+
Group: System Environment/Libraries 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: automake, autoconf

%description
Graphics routines used by the GnomeCanvas widget and some other 
applications. libart renders vector paths and the like.

%package devel
Summary: Libraries and headers for libart_lgpl
Group: Development/Libraries
Requires: %name = %{version}-%{release}

%description devel
Graphics routines used by the GnomeCanvas widget and some other 
applications. libart renders vector paths and the like.

%prep
%setup -q


%build

autoreconf -fiv
%configure \
    LDFLAGS="-maix${OBJECT_MODE} -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static
%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc AUTHORS COPYING NEWS README
%{_libdir}/libart_lgpl_2.so.2

%files devel
%defattr(-, qsys, *none)
%{_bindir}/libart2-config
%{_libdir}/libart_lgpl_2.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Tue Mar 26 2019 Calvin Buckley <calvin@cmpct.info> - 2.3.21-2
- De-AIX, Rochester conventions

* Wed May 19 2010 Michael Perzl <michael@perzl.org> - 2.3.21-1
- updated to version 2.3.21

* Sat Apr 05 2008 Michael Perzl <michael@perzl.org> - 2.3.20-1
- first version for AIX V5.1 and higher

