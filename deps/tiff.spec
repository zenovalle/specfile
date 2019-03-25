Summary: Library of functions for manipulating TIFF format image files
Name: libtiff
Version: 4.0.10
Release: 2

License: libtiff
Group: System Environment/Libraries
URL: http://simplesystems.org/libtiff/

BuildRequires: sed-gnu, automake, autoconf, libtool, libjpeg-turbo-devel, zlib-devel, libstdcplusplus-devel
Requires: libjpeg8, libz1, libstdcplusplus6
Source: http://download.osgeo.org/libtiff/tiff-%{version}.tar.gz


%global LIBVER %(echo %{version} | cut -f 1-2 -d .)

%description
The libtiff package contains a library of functions for manipulating
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

%package devel
Summary: Development tools for programs which will use the libtiff library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and documentation necessary for
developing programs which will manipulate TIFF format image files
using the libtiff library.

If you need to develop programs which will manipulate TIFF format
image files, you should install this package.  You'll also need to
install the libtiff package.


%package tools
Summary: Command-line utility programs for manipulating TIFF files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description tools
This package contains command-line programs for manipulating TIFF format
image files using the libtiff library.

%prep
%setup -q -n tiff-%{version}

# XXX: How much of this is necessary?
# Use build system's libtool.m4, not the one in the package.
rm -f libtool.m4

libtoolize --force  --copy
aclocal -I . -I m4
automake --add-missing --copy
autoconf
autoheader

%build
# XXX: Flags more consistent?
export CFLAGS="%{optflags} -fno-strict-aliasing"
%configure LDFLAGS="-maix${OBJECT_MODE} -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" --with-aix-soname=svr4 --disable-static
%make_build


%install
#rm -rf $RPM_BUILD_ROOT

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%clean
rm -rf $RPM_BUILD_ROOT

# XXX: should use i naming for perms

%files
%defattr(-, qsys, *none)
%doc COPYRIGHT
%{_libdir}/libtiff.so.5
%{_libdir}/libtiffxx.so.5
%{_datadir}/doc/tiff-4.0.10/*

%files devel
%defattr(-, qsys, *none)
%doc TODO ChangeLog html
%{_includedir}/*
%{_libdir}/libtiff.so
%{_libdir}/libtiffxx.so
%{_mandir}/man3/*
%{_libdir}/pkgconfig/libtiff-4.pc


%files tools
%defattr(-, qsys, *none)
%{_bindir}/*
%{_mandir}/man1/*
