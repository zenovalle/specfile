Name:           libxcb
Version:        1.13.1
Release:        2
Summary:        A C binding to the X11 protocol

Group:          System Environment/Libraries
License:        MIT
URL:            http://xcb.freedesktop.org/
Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  libXdmcp-devel, xorgproto
BuildRequires:  libxslt
BuildRequires:  make-gnu, bzip2, tar-gnu, libXau-devel
BuildRequires:  pkg-config, util-macros, libpthread-stubs
BuildRequires:	python2-devel, gcc-aix
BuildRequires:  xcb-proto >= 1.6

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring a
small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config, libpthread-stubs, libXau-devel
BuildRequires:  xcb-proto >= 1.6

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

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

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc COPYING NEWS README
%{_libdir}/libxcb*.so.*

%files devel
%defattr(-, qsys, *none)
%doc COPYING NEWS README
%{_includedir}/xcb
%{_libdir}/libxcb*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_datadir}/doc/libxcb/tutorial/*

%changelog
* Mon Jul 29 2019 Calvin Buckley <calvin@cmpct.info> - 1.13.1-2
- Switch to X.org, clean up deps

* Thu Mar 28 2019 Calvin Buckley <calvin@cmpct.info> - 1.13.1-1
- Update to version 1.13.1
- Add dependencies undeclared by RPM
- Add dependencies not included with system X11 on PASE
- Add dependencies undeclared by AIX packages
- De-AIX package and switch to Rochester conventions

* Wed Nov 10 2010 Michael Perzl <michael@perzl.org> - 1.7-1
- first version for AIX V5.1 and higher

