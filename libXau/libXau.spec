# rpm -ba --define 'dotests 0' libXau-1.0.8-1.spec
#%{!?dotests:%define DO_TESTS 1}
#%{?dotests:%define DO_TESTS 0}

Name:          libXau
Version:       1.0.9
Release:       2
Summary:       X.Org Xau library
Group:		System/Libraries
URL:		http://www.x.org
Source:		https://www.x.org/archive/individual/lib/%{name}-%{version}.tar.gz
License:	MIT
BuildRoot:	/var/tmp/%{name}-%{version}-root

BuildRequires: util-macros, xorgproto, autoconf, automake, libtool
# Obsoletes:     libXorg

%description
X.Org Xau library (X Authentication)

%package devel
Summary:       X.Org Xau library
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Obsoletes:     libXorg-devel

%description devel
Development files for X.Org Xau library.

%prep

%setup -q

%build

# This should automatically pick up util-macros.
autoreconf -fiv
%configure \
    LDFLAGS="-maix${OBJECT_MODE} -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
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
%{_libdir}/libXau.so.6
%doc AUTHORS COPYING ChangeLog README

%files devel
%defattr(-, qsys, *none)
%{_includedir}/X11/*.h
%{_libdir}/libXau.so
%{_libdir}/pkgconfig/xau.pc
%{_mandir}/man3/*

%changelog
* Mon Jul 29 2019 Calvin Buckley <calvin@cmpct.info> - 1.0.9-2
- Build with X.org protos

* Wed Mar 27 2019 Calvin Buckley <calvin@cmpct.info> - 1.0.9-1
- Update to version 1.0.9-1
- Add the undeclared dependencies and de-AIX

* Wed Jul 27 2016 Ravi Hirekurabar <rhirekur@in.ibm.com> - 1.0.8-1
- Update to version 1.0.8-1

* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.7-1
- Update to version 1.0.7-1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.6-1
- Inital port on Aix 5.3


