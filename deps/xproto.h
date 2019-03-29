Name:          xproto
Version:       7.0.31
Release:       1
Summary:       The X.org xproto header
Group:         Development/Libraries
URL:           http://www.x.org
Source:        https://www.x.org/archive/individual/proto/%{name}-%{version}.tar.gz
License:       MIT
Provides:      xorg-proto
Obsoletes:     xorg-proto

BuildRequires: util-macros, autoconf, automake, gcc-aix, pkg-config

BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
The X.org xproto header

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
%{_includedir}/X11/*.h
%{_libdir}/pkgconfig/*.pc
%dir %{_datadir}/doc/
%{_datadir}/doc/xproto/*


%changelog
* Fri Mar 29 2019 Calvin Buckley <calvin@cmpct.info> - 7.0.31-1
- Update to version 7.0.31
- De-AIX, use other conventions

* Tue Apr 19 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 7.0.28-1
- Update to version 7.0.28

* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.23-1
- Update to version 7.0.23

* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.20-3
- Initial port on Aix6.1

* Mon Oct 03 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.20-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.20
- Inital port on Aix 5.3


