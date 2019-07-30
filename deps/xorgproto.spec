Name:          xorgproto
Version:       2019.1
Release:       1
Summary:       The X.org protocol header set.
Group:         Development/Libraries
URL:           http://www.x.org
Source:        https://www.x.org/archive/individual/proto/%{name}-%{version}.tar.gz
License:       MIT
# Old bad decisions from AIX people and myself ahoy
Provides:      xorg-proto
Obsoletes:     xorg-proto
Provides:      renderproto
Obsoletes:     renderproto
Provides:      xproto
Obsoletes:     xproto

# need xmlto and fop for docs
BuildRequires: util-macros, autoconf, automake, gcc-aix, pkg-config, libxslt

BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
This package provides a set of X.org protocol header files.

%prep
%setup -q

%build

autoreconf -fiv
%configure \
    LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static
%make_build

%install

%make_install


%files 
%defattr(-, qsys, *none)
%doc AUTHORS COPYING* README.md
%{_includedir}/*
# X.org is weird
#%{_libdir}/pkgconfig/*.pc
%{_datadir}/pkgconfig/*.pc
# Should be split into own doc package
%{_datadir}/doc/*

%changelog
* Mon Jul 29 2019 Calvin Buckley <calvin@cmpct.info> - 2019.1
- Woosh, it's an omnibus proto set now

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


