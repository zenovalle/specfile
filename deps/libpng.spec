Summary: A library of functions for manipulating PNG image format files
Name: libpng
Epoch: 2
Version: 1.6.35
Release: 1
License: zlib
Group: System Environment/Libraries
URL: http://www.libpng.org/pub/png/
 
Source0: ftp://ftp.simplesystems.org/pub/png/src/libpng-%{version}.tar.gz
 
 
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
Requires: zlib-devel%{?_isa} pkgconfig%{?_isa}
 
%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.
 
If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.
 
 
%prep
%setup -q
 
 
%build
%configure --prefix=/QOpenSys/pkgs

make %{?_smp_mflags} 
 
%install
make DESTDIR=$RPM_BUILD_ROOT install
 
# We don't ship .la files.
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
 
 
%files
%doc libpng-manual.txt example.c README TODO CHANGES LICENSE
%{_libdir}/libpng*
%{_mandir}/man5/*
 
%files devel
%{_bindir}/*
%{_includedir}/*
%{_libdir}/libpng*
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man3/*
 
 
%changelog
