# Testcase run by default. To disable: rpm(or rpmbuild) -ba --define 'dotests 0' gzip*.spec
#%{!?dotests: %define dotests 1}

%global VERSION  7.0.9
%global Patchlevel  20


Name:           ImageMagick
Version:        %{VERSION}.%{Patchlevel}
Release:        1qsecofr
Summary:        Viewer and Converter for Images
Group:          Applications/Multimedia
License:        https://imagemagick.org/script/license.php
Url:            https://imagemagick.org/
Source0:        https://imagemagick.org/download/%{name}-%{VERSION}-%{Patchlevel}.tar.xz
#Patch0:         ImageMagick-aix-undef_symbol_err.patch
Patch1:         ImageMagick-aix-dlname.patch
Patch2:         ImageMagick-pase-x11-dir.patch

# XXX: Lots of stuff to enable... someday
# (i.e, Perl, Ghostscript, etc)
BuildRequires:  bzip2-devel, freetype-devel, libjpeg-turbo-devel, libpng-devel
BuildRequires:  libtiff-devel, zlib-devel
#BuildRequires:  ghostscript-devel
BuildRequires:  libxml2-devel
BuildRequires:  libwebp-devel
#BuildRequires:  jbigkit-devel
BuildRequires:  libpng-devel
# Realize I'm going to have to rebuild this once OpenJPEG2 gets rebuilt because of any future CMake changes...
BuildRequires:  lcms2-devel, pango-devel, fontconfig-devel, xz-devel, openjpeg2-devel, libtool
BuildRequires:  autoconf automake libtool
BuildRequires:  coreutils-gnu gcc-cplusplus-aix libstdcplusplus-devel
#BuildRequires: libgomp-devel
BuildRequires:  libICE-devel, libXext-devel, libXt-devel, rgb
# XXX: Likely undetermined deps on tcl/tk/X.org

Requires:       %{name}-libs = %{version}-%{release}
#Requires:       libgomp >= 6.3.0
#Requires:       xz-libs >= 5.2.4
#Requires:       libxml2 >= 2.9.7

%description
ImageMagick® is a software suite to create, edit, compose, or convert bitmap images. It can read and write images in a variety of formats (over 200) including PNG, JPEG, JPEG-2000, GIF, TIFF, DPX, EXR, WebP, Postscript, PDF, and SVG. Use ImageMagick to resize, flip, mirror, rotate, distort, shear and transform images, adjust image colors, apply various special effects, or draw text, lines, polygons, ellipses and Bézier curves.

The functionality of ImageMagick is typically utilized from the command-line or you can use the features from programs written in your favorite language. Choose from these interfaces: G2F (Ada), MagickCore (C), MagickWand (C), ChMagick (Ch), ImageMagickObject (COM+), Magick++ (C++), JMagick (Java), L-Magick (Lisp), Lua (LuaJIT), NMagick (Neko/haXe), Magick.NET (.NET), PascalMagick (Pascal), PerlMagick (Perl), MagickWand for PHP (PHP), IMagick (PHP), PythonMagick (Python), RMagick (Ruby), or TclMagick (Tcl/TK). With a language interface, use ImageMagick to modify or create images dynamically and automagically.

ImageMagick utilizes multiple computational threads to increase performance and can read, process, or write mega-, giga-, or tera-pixel image sizes.

ImageMagick is free software delivered as a ready-to-run binary distribution or as source code that you may use, copy, modify, and distribute in both open and proprietary applications. It is distributed under the Apache 2.0 license.

The ImageMagick development process ensures a stable API and ABI. Before each ImageMagick release, we perform a comprehensive security assessment that includes memory error and thread data race detection to prevent security vulnerabilities.

The authoritative ImageMagick web site is https://imagemagick.org. The authoritative source code repository is http://git.imagemagick.org/repos/ImageMagick. We maintain a source code mirror at GitHub.

%package devel
Summary: Library links and header files for ImageMagick application development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
# Requires: ghostscript-devel
Requires: bzip2-devel, freetype-devel, libtiff-devel, libjpeg-turbo-devel
Requires: libwebp-devel, pkg-config
Requires: %{name}-libs = %{version}-%{release}

%description devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.

%package libs
Summary: ImageMagick libraries to link with
Group: Applications/Multimedia

#Requires: libgcc >= 6.3.0
#Requires: libgomp >= 6.3.0
#Requires: xz-libs >= 5.2.4
#Requires: libxml2 >= 2.9.7
#Requires: libtiff >= 3.8.2
#Requires: fontconfig >= 2.11.95-3
#Requires: libpng >= 1.6.27-2
#Requires: glib2 >= 2.56.1-2
#Requires: bzip2 >= 1.0.6-3
#Requires: libjpeg >= 9c
#Requires: freetype2 >= 2.8
#Requires: zlib >= 1.2.11
#Requires: libwebp >= 1.0.2


%description libs
This packages contains a shared libraries to use within other applications.


%package doc
Summary: ImageMagick HTML documentation
Group: Documentation

%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in HTML format.
Note this documentation can also be found on the ImageMagick website:
https://imagemagick.org/.


%package c++
Summary: ImageMagick Magick++ library (C++ bindings)
Group: System Environment/Libraries

Requires: %{name}-libs = %{version}-%{release}
#Requires: libgcc >= 6.3.0
#Requires: libgomp >= 6.3.0
#Requires: libstdc++ >= 6.3.0
#Requires: xz-libs >= 5.2.4
#Requires: libxml2 >= 2.9.7

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.


%package c++-devel
Summary: C++ bindings for the ImageMagick library
Group: Development/Libraries
Requires: %{name}-c++ = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.

You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.


%prep
%setup -q -n %{name}-%{VERSION}-%{Patchlevel}
#%patch0 -p1
%patch1 -p1
%patch2 -p0

# for %%doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples

%build

# ImageMagick internally adds "-pthread" compile flag so add the gcc pthread specific libpath in blibpath 
#export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -L/usr/lib -Wl,-blibpath:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

autoreconf -fiv .
# openmp hangs reported, don't do it
# https://github.com/Imagick/imagick#openmp
%configure \
        --enable-shared \
        --disable-static \
        --with-modules \
        --with-x \
        --with-threads \
        --with-magick_plus_plus \
        --with-xml \
        --without-gcc-arch \
        --with-lzma=yes \
        --with-lcms=yes \
        --with-pango=yes \
        --with-fontconfig=yes \
        --with-openjp2=yes \
        --disable-openmp \
        --with-aix-soname=svr4

#        --with-jbig

# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
# XXX: Is this still true?
gmake

#if [ "%{dotests}" == 1 ]
#then
    ( gmake -k check || true )
#fi

%install

#make install DESTDIR=%{buildroot} INSTALL="install -p"
%make_install
cp -a www/source %{buildroot}%{_datadir}/doc/%{name}-%{VERSION}
rm %{buildroot}%{_libdir}/*.la
/usr/bin/strip %{buildroot}%{_bindir}/magick

%files
%defattr(-, qsys, *none)
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt ChangeLog Platforms.txt
%{_bindir}/[a-z]*
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*

%files libs
%defattr(-, qsys, *none)
%doc LICENSE NOTICE AUTHORS.txt QuickStart.txt
%{_libdir}/libMagickCore-7.Q16HDRI.so.*
%{_libdir}/libMagickWand-7.Q16HDRI.so.*
%{_libdir}/%{name}-%{VERSION}
%{_datadir}/%{name}-7
%dir %{_sysconfdir}/%{name}-7
%config(noreplace) %{_sysconfdir}/%{name}-7/*.xml

%files devel
%defattr(-, qsys, *none)
%{_bindir}/MagickCore-config
%{_bindir}/MagickWand-config
%{_libdir}/libMagickCore-7.Q16HDRI.so
%{_libdir}/libMagickWand-7.Q16HDRI.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/MagickCore-7.Q16HDRI.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-7.Q16HDRI.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/MagickWand-7.Q16HDRI.pc
%dir %{_includedir}/%{name}-7
%{_includedir}/%{name}-7/MagickCore
%{_includedir}/%{name}-7/MagickWand
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/MagickWand-config.*

%files doc
%defattr(-, qsys, *none)
%doc %{_datadir}/doc/%{name}-7
%doc %{_datadir}/doc/%{name}-%{VERSION}
%doc LICENSE

%files -n ImageMagick-c++
%defattr(-, qsys, *none)
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++-7.Q16HDRI.so.*

%files c++-devel
%defattr(-, qsys, *none)
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/%{name}-7/Magick++
%{_includedir}/%{name}-7/Magick++.h
%{_libdir}/libMagick++-7.Q16HDRI.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/Magick++-7.Q16HDRI.pc
%{_mandir}/man1/Magick++-config.*

%changelog
* Thu Jan 30 2020 Calvin Buckley <calvin@cmpct.info> - 7.0.9.20-1qsecofr
- Bump
- Disable OpenMP

* Thu Jan 1 2020 Calvin Buckley <calvin@cmpct.info> - 7.0.9.13-2qsecofr
- Enable some desirable stuff

* Tue Dec 31 2019 Calvin Buckley <calvin@cmpct.info> - 7.0.9.13-1qsecofr
- Port to IBM i

* Tue Sep 24 2019 Ayappan P <ayappap2@in.ibm.com> - 7.0.8.61-2
- Add proper dependency on freetype2-devel
- Enable libwebp support

* Tue Aug 20 2019 Ayappan P <ayappap2@in.ibm.com> - 7.0.8.61-1
- Port to AIX Toolbox
