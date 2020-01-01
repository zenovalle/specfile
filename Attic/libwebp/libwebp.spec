Name:		libwebp
Version:	1.0.3
Release:	1
Group:		Development/Libraries
URL:		http://webmproject.org/
Summary:	Library and tools for the WebP graphics format
# Additional IPR is licensed as well. See PATENTS file for details
License:	BSD
Source0:	https://storage.googleapis.com/downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz

BuildRequires:	libjpeg-turbo-devel, automake, autoconf
BuildRequires:	libpng-devel >= 1.2.46
BuildRequires:	libtiff-devel >= 3.9.4-2
BuildRequires:  giflib-devel

%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%package tools
Group:		Development/Tools
Summary:	The WebP command line tools
#Requires:	libjpeg >= 6b-7
#Requires:	libpng >= 1.2.46
#Requires:	libtiff >= 3.9.4-2

%description tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%package devel
Group:		Development/Libraries
Summary:	Development files for libwebp, a library for the WebP format
Requires:	%{name} = %{version}-%{release}

%description devel
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.


%prep
%setup -q

%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -fiv .
# all source for struct tms
%configure \
    LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static \
    --enable-libwebpmux \
    --enable-libwebpdemux \
    --enable-libwebpdecoder \
    --enable-libwebpextras

%make_build

%install
%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc README PATENTS COPYING NEWS AUTHORS
%{_libdir}/*.so.*

%files devel
%defattr(-, qsys, *none)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files tools
%defattr(-, qsys, *none)
%{_bindir}/*
%{_mandir}/man?/*


%changelog
* Mon Aug 12 2019 Calvin Buckley <calvin@cmpct.info> - 1.0.3-1
- Bump
- PASE

* Wed Jan 29 2014 Michael Perzl <michael@perzl.org> - 0.4.0-1
- updated to version 0.4.0

* Wed Jun 26 2013 Michael Perzl <michael@perzl.org> - 0.3.0-1
- updated to version 0.3.0

* Fri May 03 2013 Michael Perzl <michael@perzl.org> - 0.2.1-1
- updated to version 0.2.1

* Mon Jul 09 2012 Michael Perzl <michael@perzl.org> - 0.1.3-1
- first version for AIX V5.1 and higher

