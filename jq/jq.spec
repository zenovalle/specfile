Summary: Manipulate JSON files
Name: jq
Version: 1.6
Release: 1
License: MIT
Group: Productivity/Text/Utilities
Source0: https://github.com/stedolan/jq/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
URL: https://github.com/stedolan/%{name}/releases
Patch0: %{name}-%{version}-jv.patch
Patch1: %{name}-%{version}-builtin.patch
Patch2: %{name}-%{version}-testcase.patch
Patch3: %{name}-%{version}-aix.patch

BuildRequires: automake, autoconf
BuildRequires: oniguruma-devel >= 6.9.2
Requires: oniguruma >= 6.9.2

%description
A lightweight and flexible command-line JSON processor. jq is like sed for
JSON data - you can use it to slice and filter and map and transform
structured data with the same ease that sed, awk, grep and friends let
you play with text.

%package -n jq-devel
Summary:        Development files for jq
Group:          Development/Languages/C and C++
Requires:       %{name} = %{version}

%description -n jq-devel
Development files (headers and libraries for jq).

%prep
# Don't use -b -- it will lead to poblems when compiling magic file
%setup -q
%patch0
%patch1
%patch2
%patch3

%build

# Powder that makes libtool faster
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
autoreconf -fiv .
# We have to allow the static library to be built for jq to link statically with it.
# Otherwise, you get very weird rpath due to how the makefile invokes libtool.
%configure \
        CPPFLAGS="$CPPFLAGS -pthread" \
        LDFLAGS="$LDFLAGS -pthread -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
        --with-aix-soname=svr4 \
        --enable-shared --enable-static
%make_build

# Need valgrind and Ruby for some tests
# (gmake -k check || true)

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files

%exclude %{_libdir}/libjq.a
%defattr(-, qsys, *none)
%doc AUTHORS COPYING ChangeLog README NEWS README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1
%{_libdir}/libjq.so.1
# really not liking how we have both
%{_datadir}/doc/jq/*

%files -n jq-devel
%defattr(-, qsys, *none)
%{_includedir}/*
%{_libdir}/libjq.so

%changelog
* Tue May 28 2019 Reshma V Kumar <reskumar@in.ibm.com> - 1.6-2
- PASE

* Tue May 28 2019 Reshma V Kumar <reskumar@in.ibm.com> - 1.6-1
- Update to latest version
- Build with oniguruma support

* Wed Sep 26 2018 Reshma V Kumar <reskumar@in.ibm.com>
- Initial port for AIX toolbox


