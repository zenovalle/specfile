Name:          libpthread-stubs
Version:       0.4
Release:       2
Summary:       Dummy library for pthread
Group:         System/Libraries
URL:           http://xcb.freedesktop.org
Source:        http://xcb.freedesktop.org/dist/libpthread-stubs-%{version}.tar.gz
License:       MIT
BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
Compatibility stubs for libpthread. (dummy package)

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description devel
pkg-config file for pthread-stubs

%prep
%setup -q

%build

# This package *used* to have objects, but now it just makes a package for linking to pthread.
%configure
%make_build

%install

%make_install

%files
%defattr(-, qsys, *none)
%doc COPYING README

%files devel
%defattr(-, qsys, *none)
%{_libdir}/pkgconfig/*.pc
%doc COPYING README

%changelog
* Wed Mar 27 2019 Calvin Buckley <calvin@cmpct.info> - 0.4-1
- update to 0.4
- de-AIX
- make notes that this is basically a stub now

* Thu Oct 13 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.3-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri Jul 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.3-1
- Initial port on Aix 5.3


