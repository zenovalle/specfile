Name:          libXdmcp
Version:       1.1.3
Release:       1
Summary:       X.Org Xdmcp library
Group:		System/Libraries
URL:		http://www.x.org
Source:		https://www.x.org/archive/individual/lib/%{name}-%{version}.tar.gz
License:	MIT
BuildRequires: util-macros, xorgproto, autoconf, automake, libtool, libxslt
#Obsoletes:     libXorg

%description
X.Org Xdmcp library


%package devel
Summary:       X.Org Xdmcp library
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
#Obsoletes:     libXorg-devel

%description devel
X.Org Xdmcp library.

This package contains static libraries and header files need for development.


%prep
%setup -q

%build

autoreconf -fiv
%configure \
    LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static \
    --disable-selective-werror \
    --disable-silent-rules

%make_build

#if [ "%{DO_TESTS}" == 1 ]
#then
#        (gmake -k check || true)
#        /usr/sbin/slibclean
#fi

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc AUTHORS COPYING ChangeLog README.md
%{_libdir}/libXdmcp.so.6

%files devel
%defattr(-, qsys, *none)
#%{_libdir}/libXdmcp.la
%{_libdir}/libXdmcp.so
%{_includedir}/X11/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/doc/libXdmcp

%changelog
* Mon Jul 29 2019 Calvin Buckley <calvin@cmpct.info> - 1.1.3-1devel
- Version bump
- PASE

* Tue May 03 2016 Tony Reix <tony.reix@bull.net> - 1.1.2-1
- Inital port on AIX 6.1

* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.1.1-1
- Inital port on Aix6.1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.1.0
- Inital port on Aix 5.3

