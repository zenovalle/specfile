Name:		libpaper
Version:	1.1.28
Release:	1
Summary:	Library and tools for handling papersize
Group:		System Environment/Libraries
License:	GPLv2
URL:		http://packages.qa.debian.org/libp/libpaper.html
Source0:	http://ftp.debian.org/debian/pool/main/libp/%{name}/%{name}_%{version}.tar.gz

BuildRequires:	autoconf, automake, gawk

%description
The paper library and accompanying files are intended to provide a 
simple way for applications to take actions based on a system- or 
user-specified paper size. This release is quite minimal, its purpose 
being to provide really basic functions (obtaining the system paper name 
and getting the height and width of a given kind of paper) that 
applications can immediately integrate.

%package devel
Summary:	Headers/Libraries for developing programs that use libpaper
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains headers and libraries that programmers will need 
to develop applications which use libpaper.

%prep
%setup -q

%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -fiv .
# all source for struct tms
%configure \
  CPPFLAGS="-D_ALL_SOURCE" \
  LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
  --with-aix-soname=svr4 \
  --enable-shared --disable-static

%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
echo '# Simply write the paper name. See papersize(5) for possible values' > ${RPM_BUILD_ROOT}%{_sysconfdir}/papersize
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/libpaper.d

%files
%defattr(-, qsys, *none)
%doc COPYING ChangeLog README
%config(noreplace) %{_sysconfdir}/papersize
%dir %{_sysconfdir}/libpaper.d
%{_bindir}/paperconf
%{_sbindir}/paperconfig
%{_libdir}/libpaper.so.1
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*


%files devel
%defattr(-, qsys, *none)
%{_includedir}/*
%{_libdir}/libpaper.so
%{_mandir}/man3/*


%changelog
* Fri Aug 09 2019 Calvin Buckley <calvin@cmpct.info> - 1.1.28-1
- Bump
- PASE

* Tue Jan 25 2011 Michael Perzl <michael@perzl.org> - 1.1.24-1 
- updated to version 1.1.24

* Fri Oct 23 2009 Michael Perzl <michael@perzl.org> - 1.1.23-3 
- adapted the paper.h include file for AIX

* Tue Sep 15 2009 Michael Perzl <michael@perzl.org> - 1.1.23-2 
- fixed some minor SPEC file issues

* Tue Jul 28 2009 Michael Perzl <michael@perzl.org> - 1.1.23-1
- first version for AIX5L v5.1 and higher
