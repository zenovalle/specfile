Name:           util-macros
Version:        1.19.2
Release:        1
Summary:        X.org autotools macros

Group:          Development/Libraries
License:        MIT
URL:            http://x.org/
Source0:        https://www.x.org/archive/individual/util/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

# XXX
BuildRequires:  gawk, make-gnu, m4-gnu, libtool, automake, autoconf
Requires:       pkg-config, m4-gnu, automake

%description
This contains some macros (xorg-macros) used by many X.org packages.

%prep
%setup -q

%build

# Not a lot here since it doesn't make objects.

%configure
%make_build

%install

%make_install

%files
%defattr(-, qsys, *none)
%doc COPYING README
%{_datadir}/aclocal/xorg-macros.m4
%{_datadir}/util-macros/INSTALL
%{_datadir}/pkgconfig/xorg-macros.pc

%changelog
* Wed Mar 27 2019 Calvin Buckley <calvin@cmpct.info> - 1.19.2-1
- Create package
