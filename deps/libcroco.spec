Name:             libcroco
Summary:          A CSS2 parsing library 
Version:          0.6.12
Release: 	  1
License:          LGPLv2
Group:            System Environment/Libraries
Source0:          http://ftp.gnome.org/pub/gnome/sources/libcroco/0.6/%{name}-%{version}.tar.xz
Source1:          http://ftp.gnome.org/pub/gnome/sources/libcroco/0.6/%{name}-%{version}.sha256sum
#Patch0:           %{name}-%{version}-aix.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:    make-gnu
# XXX: not quite up to date
BuildRequires:    glib2-devel >= 2.8.1-3
BuildRequires:    libxml2-devel >= 2.6.32-3
BuildRequires:    pkg-config >= 0.8
BuildRequires:    xz, autoconf, automake
Requires:         libglib-2_0-0 >= 2.8.1-3
Requires:         libxml2 >= 2.6.32-3

%description
CSS2 parsing and manipulation library for GNOME

%package devel
Summary:          Libraries and include files for developing with libcroco.
Group:            Development/Libraries
Requires:         %{name} = %{version}
Requires:         glib2-devel >= 2.8.1-3
Requires:         libxml2-devel >= 2.6.32-3
Requires:         pkg-config >= 0.8

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with libcroco.

%prep
%setup -q
# %patch0


%build

autoreconf -fiv
%configure \
    LDFLAGS="-maix${OBJECT_MODE} -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static
# XXX: croco fails one or two tests. Most are just FP precision stupdiity, one is a "not quite" Unicode handling issue?
# Might be related to not using Perzl's patch for -fno-common ?
%make_build

%install
%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc AUTHORS COPYING COPYING.LIB NEWS README 
%{_bindir}/csslint-0.6
%{_libdir}/libcroco-0.6.so.3


%files devel
%defattr(-, qsys, *none)
%{_bindir}/croco-0.6-config
%{_includedir}/libcroco-0.6/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcroco-0.6.so
%{_datadir}/gtk-doc/html/libcroco/*

%changelog
* Wed Aug 08 2012 Calvin Buckley <calvin@cmpct.info> - 0.6.12-1
- updated to version 0.6.12
- de-AIX, Rochester conventions, make notes about possible changes

* Wed Aug 08 2012 Michael Perzl <michael@perzl.org> - 0.6.5-1
- updated to version 0.6.5

* Wed Aug 08 2012 Michael Perzl <michael@perzl.org> - 0.6.4-1
- updated to version 0.6.4

* Wed Aug 08 2012 Michael Perzl <michael@perzl.org> - 0.6.3-1
- updated to version 0.6.3

* Thu Oct 07 2010 Michael Perzl <michael@perzl.org> - 0.6.2-1
- updated to version 0.6.2

* Tue Apr 15 2008 Michael Perzl <michael@perzl.org> - 0.6.1-1
- first version for AIX V5.1 and higher
- (NOTE: This originally said Wed, but fixing a bogus date.)
