Name:          xtrans
Version:       1.4.0
Release:       1
Summary:       X protocol translation tools for X.Org
Group:         Development/Libraries
URL:           http://www.x.org
Source:        https://www.x.org/archive/individual/lib/%{name}-%{version}.tar.bz2
License:       MIT
Provides:      xorg-xtrans
Obsoletes:     xorg-xtrans
BuildRoot:     /var/tmp/%{name}-%{version}-root

BuildRequires: util-macros, gcc-aix, autoconf, automake

%description
X protocol translation tools for X.Org

%prep
%setup -q

%build

autoreconf -fiv
%configure
%make_build

%install

%make_install

%files 	
%defattr(-, qsys, *none)
%dir %{_includedir}/X11/Xtrans
%{_includedir}/X11/Xtrans/*.c
%{_includedir}/X11/Xtrans/*.h
%{_datadir}/pkgconfig/xtrans.pc
%{_datadir}/aclocal/xtrans.m4
%dir %{_datadir}/doc/xtrans
%{_datadir}/doc/xtrans/xtrans.*
%doc AUTHORS COPYING ChangeLog README.md


%changelog
* Fri Mar 29 2019 Calvin Buckley <calvin@cmpct.info> - 1.4.0-1
- PASE, update version, change conventions

* Fri Apr 26 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.7-1
- Initial port on Aix6.1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.6
- Inital port on Aix 5.3


