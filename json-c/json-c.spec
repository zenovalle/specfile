%define dotests  0

Name:		json-c
Version:	0.13.1
Release:	2
Summary:	A JSON implementation in C
Group:		Development/Libraries
License:	MIT
URL:		https://github.com/json-c/json-c/wiki
Source0:	https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Patch0: json-c-pase.diff

# Added autoreconf to help it with AIX sonames
BuildRequires:	patch-gnu make-gnu autoconf automake libtool
Requires: gcc-aix >= 6.3.0


%description
JSON-C implements a reference counting object model that allows you to easily
construct JSON objects in C, output them as JSON formatted strings and parse
JSON formatted strings back into the C representation of JSON objects.


%package devel
Summary:	Development headers and library for json-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkg-config

%description devel
This package contains the development headers and library for json-c.


%package doc
Summary:	Reference manual for json-c
Group:		Documentation

%description doc
This package contains the reference manual for json-c.


%prep
%setup -q
%patch0 -p1

%build

autoreconf -fiv
%configure \
	CPPFLAGS="$CPPFLAGS -pthread" \
	LDFLAGS="$LDFLAGS -pthread -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
	--with-aix-soname=svr4 --enable-threading \
	--enable-shared --disable-static
%make_build

#if [ "%{dotests}" == 1 ] then
#	( gmake -k check || true )
#	/usr/sbin/slibclean
#fi

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

# The AIX RPM did a bunch of crap for merging libs, of course

%files
%defattr(-, qsys, *none)
%doc AUTHORS ChangeLog COPYING NEWS
%doc README README.html
%{_libdir}/libjson-c.so.4

%files devel
%defattr(-, qsys, *none)
%{_includedir}/json-c/*
%{_libdir}/libjson-c.so
%{_libdir}/pkgconfig/json-c.pc

%files doc
%defattr(-, qsys, *none)
%doc doc/html/*


%changelog
* Sun Jul 21 2019 Calvin Buckley <calvin@cmpct.info>
- Port to IBM i

* Mon Apr 30 2018 Ravi Hirekurabar <rhirekur@in.ibm.com>
- Initial port to AIX

