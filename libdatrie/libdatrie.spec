Summary:	Double-array structure for representing trie
Name:		libdatrie
Version:	0.2.11
Release:	1
License:	LGPL
Group:		System/Libraries
URL:		http://linux.thai.net
Source0:	ftp://linux.thai.net/pub/ThaiLinux/software/libthai/%{name}-%{version}.tar.xz
# AIX header dumb, rip out Doxygen until that gets packaged
Patch0:         datrie-pase.diff
BuildRequires:	pkg-config, libiconv-devel, automake, autoconf

%description
This is an implementation of double-array structure for representing trie.

Trie is a kind of digital search tree, an efficient indexing method with
O(1) time complexity for searching. Comparably as efficient as hashing,
trie also provides flexibility on incremental matching and key spelling
manipulation. This makes it ideal for lexical analyzers, as well as spelling
dictionaries.


%package devel
Summary:	Double-array structure for representing trie
Group:		Development/C
Requires:	%{name} = %{version}
Requires:	pkg-config

%description devel
This package includes the header files and developer docs for the libdatrie
package.

Install libdatrie-devel if you want to develop programs which will use
libdatrie.


%prep
%setup -q
%patch0 -p1

%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -fiv .
%configure \
  CPPFLAGS=-I%{_includedir}/libiconv \
  LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
  --with-aix-soname=svr4 \
  --enable-shared --disable-static \
    --disable-doxygen-docs

%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc README AUTHORS COPYING NEWS
%{_bindir}/trietool*
%{_mandir}/man1/*
%{_libdir}/libdatrie.so.1
# huh?
%{_datadir}/doc/libdatrie/README.migration

%files devel
%defattr(-, qsys, *none)
%{_includedir}/*
%{_libdir}/libdatrie.so
%{_libdir}/pkgconfig/datrie-0.2.pc

%changelog
* Mon Aug 12 2019 Calvin Buckley <calvin@cmpct.info> - 0.2.11-1
- Bump
- PASE

* Tue Jul 19 2011 Michael Perzl <michael@perzl.org> - 0.2.4-1
- updated to version 0.2.4-1

* Tue May 03 2011 Michael Perzl <michael@perzl.org> - 0.1.4-1
- updated to version 0.1.4-1

* Tue Apr 22 2008 Michael Perzl <michael@perzl.org> - 0.1.3-1
- first version for AIX V5.1 and higher

