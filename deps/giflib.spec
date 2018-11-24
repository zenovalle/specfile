# Modified by Yvan Janssens <qsecofr@qseco.fr> to work on IBM i.
#
# spec file for package giflib
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           giflib
%define lname	libgif6
Version:        5.1.4
Release:        0
Summary:        A Library for Working with GIF Images
License:        MIT
Group:          Development/Libraries/C and C++
Url:            http://giflib.sf.net/

#Git-Clone:	git://git.code.sf.net/p/giflib/code
#Freecode-URL:	http://freecode.com/projects/giflib
Source:         http://downloads.sf.net/giflib/%name-%version.tar.bz2

%description
This Library allows manipulating GIF Image files. Since the LZW patents
have expired, giflib can again be used instead of libungif.

%package -n %lname
Summary:        A Library for Working with GIF Images
Group:          System/Libraries

%description -n %lname
This Library allows manipulating GIF Image files. Since the LZW patents
have expired, giflib can again be used instead of libungif.

%package progs
Summary:        Tools for Working with the GIF Library
Group:          Productivity/Graphics/Convertors
Provides:       ungif
Obsoletes:      ungif

%description progs
A tool for converting GIFs to various formats.

%package devel
Summary:        Library for Working with GIF Images - Files Mandatory for Development
Group:          Development/Libraries/C and C++
Requires:       %lname = %version
#

%description devel
This Library allows manipulating GIF Image files. Since the LZW patents
have expired, giflib can again be used instead of libungif.

%prep
%setup -q

%build

mkdir -p m4; autoreconf -fiv
./configure --disable-static --with-pic --x-libraries=%{_libdir} --prefix=/QOpenSys/pkgs
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files -n %lname
%defattr(-,root,root)
%doc COPYING
%{_libdir}/lib*.a

%files devel
%defattr(-,root,root)
%_includedir/gif_lib.h
%{_libdir}/lib*

%files progs
%defattr(-,root,root)
%doc COPYING NEWS README doc
%_bindir/*

%changelog

