Name:          libX11
Version:       1.6.8
Release:       1
Summary:       X.Org X11 library
Group:		System/Libraries
URL:		http://www.x.org
#Old Source:	http://www.x.org/releases/X11R7.6/src/lib/%{name}-%{version}.tar.gz
Source0: 	http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
# XXX: Include from Bull SRPM if necessary
#Patch2: %{name}-%{version}-dont-forward-keycode-0.patch
License:	MIT

BuildRequires: libxslt, gcc-aix, autoconf, automake, bzip2
# Convention adjustment AGAIN
#BuildRequires: xorg-x11-util-macros >= 1.11
BuildRequires: xorgproto
#BuildRequires: xproto-devel >= 7.0.15
#BuildRequires: xtrans-devel >= 1.0.3-4
BuildRequires: xtrans
BuildRequires: libxcb-devel >= 1.2
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel
# XXX: How do I handle Perl?
#BuildRequires: perl(Pod::Usage)
#BuildRequires: inputproto-devel >= 2.0


#BuildRoot:     %{_tmppath}/%{name}-%{version}-root
#BuildRoot:	/var/tmp/%{name}-%{version}-root

%description
X.Org Xext library
Core X11 protocol client library.


%package devel
Summary:	X.Org X11 library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libXau-devel >= 1.0.3
Requires:	libXdmcp-devel >= 1.0.2
Obsoletes:	libXorg-devel


%description devel
X.Org X11 library.

This package contains header files need for development.

%prep
%setup -q

%build

autoreconf -fiv
# XXX: Loadable i18n support?
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
%doc AUTHORS COPYING ChangeLog NEWS README.md
%{_libdir}/libX11.so.6
%{_libdir}/libX11-xcb.so.1
%{_datadir}/X11/XErrorDB
%{_datadir}/X11/locale/*


%files devel
%defattr(-, qsys, *none)
%{_prefix}/share/X11/Xcms.txt
%{_libdir}/libX11*.so

%{_includedir}/X11/*.h

%{_libdir}/pkgconfig/*.pc

%dir %{_docdir}/libX11-%{version}
%{_docdir}/libX11-%{version}/*
%{_datadir}/doc/libX11/*

%{_mandir}/man*/*


%changelog
* Mon Jul 29 2019 Calvin Buckley <calvin@cmpct.info> - 1.6.8-1
- PASE
- Bump
- Change conventions and other munging for PASE

* Tue Apr 12 2016 Tony Reix <tony.reix@bull.net> - 1.6.3-1
- Inital port of version 1.6.3 on AIX 6.1

* Wed Apr 10 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.0-1
- Inital port on AIX 6.1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.4.0
- Inital port on Aix 5.3

