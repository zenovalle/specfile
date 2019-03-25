Summary: A library of functions for manipulating PNG image format files
Name: libpng
Epoch: 2
Version: 1.6.36
Release: 2
License: zlib
Group: System Environment/Libraries
URL: http://www.libpng.org/pub/png/

Source0: https://download.sourceforge.net/libpng/libpng-%{version}.tar.gz

BuildRequires: autoconf, automake, libtool
Requires: zlib
 
%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG
is a bit-mapped graphics format similar to the GIF format.  PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.
 
Libpng should be installed if you need to manipulate PNG format image
files.
 
%package devel
Summary: Development tools for programs to manipulate PNG image format files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: zlib-devel%{?_isa} pkg-config%{?_isa}

 
%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.
 
If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.
 
 
%prep
%setup -q
 
 
%build
# Regenerate the build system so it respects soname
autoreconf -fiv
# XXX: Flags?
%configure --with-aix-soname=svr4

%make_build
 
%install
%make_install
 
# We don't ship .la files.
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
 
 
%files
%doc libpng-manual.txt example.c README TODO CHANGES LICENSE
%{_libdir}/libpng.so*
%{_libdir}/libpng16.so*
%{_mandir}/man5/*
 
%files devel
%{_bindir}/*
%{_includedir}/*
%{_libdir}/libpng.a
%{_libdir}/libpng16.a
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man3/*
 
 
%changelog
