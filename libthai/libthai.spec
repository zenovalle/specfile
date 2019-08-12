Summary: Thai language support routines
Name: libthai
Version: 0.1.28
Release: 1
License: LGPL
Group: System Environment/Libraries
Source0: ftp://linux.thai.net/pub/ThaiLinux/software/%{name}/%{name}-%{version}.tar.xz
Patch0: libthai-pase.diff
URL: http://linux.thai.net

BuildRequires: libdatrie-devel >= 0.2.4
BuildRequires: pkg-config
#Requires: libdatrie >= 0.2.4

%description
LibThai is a set of Thai language support routines aimed to ease
developers' tasks to incorporate Thai language support in their applications.
It includes important Thai-specific functions e.g. word breaking, input and
output methods as well as basic character and string supports.

%package devel
Summary:  Thai language support routines
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libdatrie-devel >= 0.2.4
Requires: pkg-config

%description devel
The libthai-devel package includes the header files and developer docs 
for the libthai package.

Install libthai-devel if you want to develop programs which will use
libthai.

%prep
%setup -q
%patch0 -p1


%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -fiv .
# all source for struct tms
%configure \
  CPPFLAGS="-D_ALL_SOURCE" \
  LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
  --with-aix-soname=svr4 \
  --enable-shared --disable-static \
  --disable-doxygen-doc

%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc README AUTHORS COPYING ChangeLog
%{_libdir}/libthai.so.0
%{_datadir}/%{name}/*

%files devel
%defattr(-, qsys, *none)
%{_includedir}/*
%{_libdir}/libthai.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Mon Aug 12 2019 Calvin Buckley <calvin@cmpct.info> - 0.1.28-1
- Bump
- PASE

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 0.1.18-1
- update to version 0.1.18

* Tue May 03 2011 Michael Perzl <michael@perzl.org> - 0.1.15-1
- update to version 0.1.15

* Tue Apr 22 2008 Michael Perzl <michael@perzl.org> - 0.1.9-1
- first version for AIX V5.1 and higher
