%bcond_with reconf

# zip extension requires libzip: https://libzip.org/
%define zip 1

# With libzip, PEAR is included. However, Fedora's PHP RPMs build PEAR as a separate package.
# Not sure what we want to do, but for now we can use the built-in PEAR. If it becomes
# problematic, we can introduce a seperate package, turn this define off, and set the new
# RPM's Epoch to be higher than this one.
# (There's also other stuff that the php-pear Fedora RPM has, investigate further...)
%define pear 1

# ICU causes problems due to being built with XLC
# PHP calls icu-config --cflags and --ldflags, which
# contain XLC-specific flags like -qmaxmem, -qutf
# We could try hacking these flags *or* build ICU ourselves
# For now, just disable
%bcond_with intl

%define major 7
%define minor 3
%define fix 14

Name: php
Version: %{major}.%{minor}.%{fix}
Release: 0qsecofr
License: PHP-3.01
Summary: PHP programming language
Url: https://www.php.net

Source0: http://us2.php.net/get/php-%{version}.tar.gz/from/this/mirror/#/php-%{version}.tar.gz

Patch0: php-ini.patch
Patch1: php-opcache-flock.patch
Patch2: php-no-sigprof-on-pase.patch
Patch3: php-fpm-allow-non-root.patch

BuildRequires: pkg-config

BuildRequires: bzip2-devel
# We need a version of curl linked with OpenSSL 1.1
BuildRequires: curl-devel >= 7.65.3
BuildRequires: freetype-devel
BuildRequires: libiconv-devel
BuildRequires: libintl-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
BuildRequires: libsodium-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: libzip-devel
BuildRequires: openssl-devel
# We need a version of sqlite built with SQLITE_ENABLE_COLUMN_METADATA
BuildRequires: sqlite3-devel >= 3.19.3-1
BuildRequires: unixODBC-devel
BuildRequires: libwebp-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel

%if %{with reconf}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: m4-gnu
%endif

%description
PHP is a popular general-purpose scripting language that is especially suited to web development.

Fast, flexible and pragmatic, PHP powers everything from your blog to the most popular websites in the world.


%package common
Summary: Common files for PHP

%description common
The php-common package contains files used by both the php
package and the php-cli package.


%package cli
Summary: Command-line interface for PHP
Provides: %{name}-cgi = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, %{_bindir}/php, and the CGI interface.

%package fpm
Summary: PHP FastCGI Process Manager (FPM)
Requires: %{name}-cgi = %{version}-%{release}

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI implementation
with some additional features useful for sites of any size, especially busier
sites.


%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%if %{pear}
%package pear
Summary: PHP Extension and Application Repository framework

%description pear
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

This version is using the bundled PEAR from PHP.
%endif

%package bcmath
Summary: bcmath extension for PHP

%description bcmath
bcmath extension for PHP

%package bz2
Summary: bz2 extension for PHP

%description bz2
bz2 extension for PHP

%package calendar
Summary: calendar extension for PHP

%description calendar
calendar extension for PHP

%package ctype
Summary: ctype extension for PHP

%description ctype
ctype extension for PHP

%package curl
Summary: curl extension for PHP
# We need a version of curl linked with OpenSSL 1.1
Requires: libcurl4 >= 7.65.3

%description curl
curl extension for PHP

%package exif
Summary: exif extension for PHP
Recommends: %{name}-mbstring

%description exif
exif extension for PHP

%package fileinfo
Summary: fileinfo extension for PHP

%description fileinfo
fileinfo extension for PHP

%package ftp
Summary: ftp extension for PHP

%description ftp
ftp extension for PHP

%package gd
Summary: gd extension for PHP

%description gd
gd extension for PHP

%package gettext
Summary: gettext extension for PHP

%description gettext
gettext extension for PHP

%package iconv
Summary: iconv extension for PHP

%description iconv
iconv extension for PHP

%package mbstring
Summary: mbstring extension for PHP

%description mbstring
mbstring extension for PHP

%package mysqlnd
Summary: mysqlnd-related extensions for PHP
Requires: %{name}-pdo

%description mysqlnd
mysqlnd-related extensions for PHP

%package odbc
Summary: odbc extensions for PHP
Requires: %{name}-pdo

%description odbc
odbc extensions for PHP

%package pdo
Summary: pdo extension for PHP

%description pdo
pdo extension for PHP

%package opcache
Summary: opcache extension for PHP

%description opcache
opcache extension for PHP

%package openssl
Summary: openssl extension for PHP

%description openssl
openssl extension for PHP

%package phar
Summary: phar extension for PHP

%description phar
phar extension for PHP

%package process
Summary: process extension for PHP

%description process
process extension for PHP

%package soap
Summary: soap extension for PHP

%description soap
soap extension for PHP

%package sockets
Summary: sockets extension for PHP

%description sockets
sockets extension for PHP

%package sodium
Summary: sodium extension for PHP

%description sodium
sodium extension for PHP

%package sqlite3
Summary: sqlite3 extensions for PHP
Requires: %{name}-pdo
# We need a version of sqlite built with SQLITE_ENABLE_COLUMN_METADATA
Requires: libsqlite3-0 >= 3.19.3-1

%description sqlite3
sqlite3 extensions for PHP

%package tokenizer
Summary: tokenizer extension for PHP

%description tokenizer
tokenizer extension for PHP

%package xml
Summary: xml-related extensions for PHP

%description xml
xml-related extensions for PHP

%if %{zip}
%package zip
Summary: zip extension for PHP

%description zip
zip extension for PHP
%endif


%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# PHP extensions expect to find include files in some_dir/include and
# libraries to be in some_dir/lib so that you can pass --with-ext=some_dir
# This assumption is broken with libiconv though, since it puts its includes
# in a subdirectory: /QOpenSys/pkgs/include/libiconv while the libraries
# are in the normal library path. To work around this, we symlink everything
# in to a common subdirectory here:

mkdir -p libiconv/include libiconv/lib
ln -s %{_includedir}/libiconv/* libiconv/include
ln -s %{_libdir}/libiconv.so* libiconv/lib

%build

%if %{with reconf}
autoreconf -fi
%else
%define _host powerpc64-ibm-aix6
%endif

%define sysconfdir_php    %{_sysconfdir}/php
%define extension_dir     %{_libdir}/php-%{major}.%{minor}/extensions

export EXTENSION_DIR=%{extension_dir}

LDFLAGS="-Wl,-brtl -pthread -Wl,-bbigtoc -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib"

### NOTES on shared vs static ###
# Here's the list of static extensions on Fedora
#    hash, session, pcre, pcntl, readline, openssl, zlib
#
# Here's the list of static extensions on openSUSE:
#   simplexml, session, pcre, filter
#
# We set the following to build static:
# hash, filter, session, libxml, zlib
#
# Additionally, we are building these static for the time being:
# pdo, sqlite3, pdo_sqlite

%configure \
    -C \
    php_sapi_module=shared \
    ax_cv_check_cflags___fvisibility_hidden=no \
    ac_cv_func_flock=no \
    CPPFLAGS="$CPPFLAGS -pthread"  \
    CFLAGS="$CFLAGS -pthread" \
    PHP_AIX_LDFLAGS="$LDFLAGS" \
    LDFLAGS="$LDFLAGS" \
    --sysconfdir=%{sysconfdir_php} \
    --with-config-file-path=%{sysconfdir_php} \
    --with-config-file-scan-dir=%{sysconfdir_php}/conf.d \
    --disable-phpdbg \
    --disable-rpath \
    --enable-fpm \
    --enable-shared=yes \
    --enable-bcmath=shared \
    --enable-calendar=shared \
    --enable-ctype=shared \
    --enable-dom=shared \
    --enable-exif=shared \
    --enable-filter \
    --enable-fileinfo=shared \
    --enable-ftp=shared \
    --enable-hash \
    --enable-libxml \
    --enable-mbstring=shared \
    --enable-mysqlnd=shared \
    --enable-pcntl=yes \
    --enable-pdo=shared \
%if %{pear}
    --with-pear \
%else
    --without-pear \
%endif
    --enable-phar=shared \
    --enable-posix=shared \
    --enable-session \
    --enable-soap=shared \
    --enable-shmop=shared \
    --enable-simplexml=shared \
    --enable-sockets=shared \
    --enable-sysvmsg=shared \
    --enable-sysvsem=shared \
    --enable-sysvshm=shared \
    --enable-tokenizer=shared \
    --enable-xml=shared \
    --enable-xmlreader=shared \
    --enable-xmlwriter=shared \
%if %{zip}
    --enable-zip=shared \
    --with-libzip=%{_prefix} \
%else
    --disable-zip \
%endif
%if %{with intl}
    --enable-intl=shared \
%else
    --disable-intl \
%endif
    --with-bz2=shared,%{_prefix} \
    --with-curl=shared,%{_prefix} \
    --with-gd=shared \
    --with-gettext=shared,%{_prefix} \
    --with-iconv=shared,$PWD/libiconv \
    --with-openssl=shared,%{_prefix} \
    --with-sodium=shared,%{_prefix} \
    --with-xsl=shared,%{_prefix} \
    --with-mysqli=shared \
    --with-pdo-mysql=shared \
%if 0
    --with-mysql-sock=/tmp/mysql.sock \
%endif
    --with-unixODBC=shared,%{_prefix} \
    --with-pdo-odbc=shared,unixODBC,%{_prefix} \
    --with-sqlite3=shared,%{_prefix} \
    --with-pdo-sqlite=shared,%{_prefix} \
    --with-webp-dir=%{_prefix} \
    --with-jpeg-dir=%{_prefix} \
    --with-png-dir=%{_prefix} \
    --with-freetype-dir=%{_prefix} \
    --with-xpm-dir=/QOpenSys/usr/lib \
    --with-zlib=yes \
    --with-zlib-dir=%{_prefix} \
    # end

# The following extensions need additional linking:
# exif, opcache, soap need to link to libm
# mysqlnd needs to link to libm, libcrypto, and libssl
# gd needs to link to libm and libiconv
#
# PHP extensions have automatic foo_SHARED_LIBADD variables referenced by the
# Makefile that we can add to. For exif, opcache, and mysqlnd the configure
# script sets them empty, so we can simply pass them on the command line to make.
# For gd and soap, however, we need to append to the existing line in the
# Makefile using perl.

perl -p -i -e 's/(SOAP_SHARED_LIBADD = .*)/$1 -lm/' Makefile
perl -p -i -e 's/(GD_SHARED_LIBADD = .*)/$1 -liconv -lm/' Makefile


%make_build \
    LDFLAGS="$LDFLAGS" \
    OPCACHE_SHARED_LIBADD=-lm \
    EXIF_SHARED_LIBADD=-lm \
    MYSQLND_SHARED_LIBADD='-lm -lcrypto -lssl'

%install

%make_install INSTALL_ROOT=%{buildroot}

mkdir -p %{buildroot}%{sysconfdir_php}/conf.d

for f in modules/*.so
do
    ext=`basename $f .so`

    case $ext in
    pdo_*|mysqli|xmlreader|xsl)
        # pdo extensions depend on the pdo extension
        LEVEL=30
        ;;

    mysqli)
        # mysqli depends on the mysqlnd extension
        LEVEL=30
        ;;

    xmlreader|xsl)
        # these extensions depend on the dom extension
        LEVEL=30
        ;;

    opcache)
        # opcache is special, so it goes first
        LEVEL=10
        ;;

    *)
        LEVEL=20
        ;;
    esac

    if [ "$ext" = "opcache" ]
    then
    cat <<EOF > %{buildroot}%{sysconfdir_php}/conf.d/$LEVEL-$ext.ini
; enable Zend OPcache extension module
zend_extension=$ext
EOF
    else
    cat <<EOF > %{buildroot}%{sysconfdir_php}/conf.d/$LEVEL-$ext.ini
; enable $ext extension module
extension=$ext
EOF

    fi
done

sed 's|@EXTENSION_DIR@|%{extension_dir}|; s|@SYSCONF_DIR@|%{sysconfdir_php}|' \
    php.ini-production > %{buildroot}%{_sysconfdir}/php.ini

mv %{buildroot}%{sysconfdir_php}/php-fpm.conf.default %{buildroot}%{sysconfdir_php}/php-fpm.conf

sed 's|user = nobody|user = qtmhhttp|; s|group = nobody|;group = nobody|' \
    %{buildroot}%{sysconfdir_php}/php-fpm.d/www.conf.default > %{buildroot}%{sysconfdir_php}/php-fpm.d/www.conf

rm %{buildroot}%{sysconfdir_php}/php-fpm.d/www.conf.default

# rm -r %{buildroot}/.channels
# rm -r %{buildroot}/.depdb
# rm -r %{buildroot}/.depdblock
# rm -r %{buildroot}/.filemap
# rm -r %{buildroot}/.lock


# %files
# %defattr(-, qsys, *none)

%files common
%defattr(-, qsys, *none)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
#%doc Zend/ZEND_*
#%dir /etc/php.d
#%dir %{_libdir}/php
#%{_libdir}/build/*
#%dir {_libdir}/php/modules
#%dir /var/lib/php
#%dir {_libdir}/php/PEAR

%config(noreplace) %{_sysconfdir}/php.ini

%dir %{sysconfdir_php}
%dir %{sysconfdir_php}/conf.d

%{_libdir}/*
%exclude %{extension_dir}/*

%files fpm
%defattr(-, qsys, *none)
%{_sbindir}/php-fpm

%dir %{sysconfdir_php}/php-fpm.d

%config(noreplace) %{sysconfdir_php}/php-fpm.conf
%config(noreplace) %{sysconfdir_php}/php-fpm.d/www.conf

%{_datadir}/fpm/status.html

%{_mandir}/man8/php-fpm.8


%files cli
%defattr(-, qsys, *none)
%{_bindir}/php
%{_bindir}/php-cgi

%{_mandir}/man1/php.1
%{_mandir}/man1/php-cgi.1

%{_bindir}/phar
%{_bindir}/phar.phar
# %{_bindir}/phpdbg

%{_mandir}/man1/phar.1
%{_mandir}/man1/phar.phar.1
# %{_mandir}/man1/phpdbg.1

%if %{pear}
%files pear
%defattr(-, qsys, *none)

%config(noreplace) %{sysconfdir_php}/pear.conf

%{_bindir}/pear
%{_bindir}/peardev
%{_bindir}/pecl

# blah, it leaves some droppings in .
%exclude /.*
%endif

%files devel
%defattr(-, qsys, *none)
%{_bindir}/php-config
%{_bindir}/phpize

%{_includedir}/php

%{_mandir}/man1/php-config.1
%{_mandir}/man1/phpize.1

%files bcmath
%defattr(-, qsys, *none)
%{extension_dir}/bcmath.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-bcmath.ini

%files bz2
%defattr(-, qsys, *none)
%{extension_dir}/bz2.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-bz2.ini

%files calendar
%defattr(-, qsys, *none)
%{extension_dir}/calendar.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-calendar.ini

%files ctype
%defattr(-, qsys, *none)
%{extension_dir}/ctype.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-ctype.ini

%files curl
%defattr(-, qsys, *none)
%{extension_dir}/curl.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-curl.ini

%files exif
%defattr(-, qsys, *none)
%{extension_dir}/exif.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-exif.ini

%files fileinfo
%defattr(-, qsys, *none)
%{extension_dir}/fileinfo.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-fileinfo.ini

%files ftp
%defattr(-, qsys, *none)
%{extension_dir}/ftp.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-ftp.ini

%files gd
%defattr(-, qsys, *none)
%{extension_dir}/gd.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-gd.ini

%files gettext
%defattr(-, qsys, *none)
%{extension_dir}/gettext.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-gettext.ini

%files iconv
%defattr(-, qsys, *none)
%{extension_dir}/iconv.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-iconv.ini

%files mbstring
%defattr(-, qsys, *none)
%{extension_dir}/mbstring.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-mbstring.ini

%files mysqlnd
%defattr(-, qsys, *none)
%{extension_dir}/mysqlnd.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-mysqlnd.ini

%{extension_dir}/mysqli.so
%config(noreplace) %{sysconfdir_php}/conf.d/30-mysqli.ini

%{extension_dir}/pdo_mysql.so
%config(noreplace) %{sysconfdir_php}/conf.d/30-pdo_mysql.ini

%files odbc
%defattr(-, qsys, *none)
%{extension_dir}/odbc.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-odbc.ini

%{extension_dir}/pdo_odbc.so
%config(noreplace) %{sysconfdir_php}/conf.d/30-pdo_odbc.ini

%files pdo
%defattr(-, qsys, *none)
%{extension_dir}/pdo.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-pdo.ini

%files opcache
%defattr(-, qsys, *none)
%{extension_dir}/opcache.so
%config(noreplace) %{sysconfdir_php}/conf.d/10-opcache.ini

%files openssl
%defattr(-, qsys, *none)
%{extension_dir}/openssl.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-openssl.ini

%files phar
%defattr(-, qsys, *none)
%{extension_dir}/phar.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-phar.ini

%files process
%defattr(-, qsys, *none)
%{extension_dir}/posix.so
%{sysconfdir_php}/conf.d/20-posix.ini

%{extension_dir}/shmop.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-shmop.ini

%{extension_dir}/sysvmsg.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-sysvmsg.ini

%{extension_dir}/sysvsem.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-sysvsem.ini

%{extension_dir}/sysvshm.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-sysvshm.ini

%files soap
%defattr(-, qsys, *none)
%{extension_dir}/soap.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-soap.ini

%files sockets
%defattr(-, qsys, *none)
%{extension_dir}/sockets.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-sockets.ini

%files sodium
%defattr(-, qsys, *none)
%{extension_dir}/sodium.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-sodium.ini

%files sqlite3
%defattr(-, qsys, *none)
%{extension_dir}/sqlite3.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-sqlite3.ini

%{extension_dir}/pdo_sqlite.so
%config(noreplace) %{sysconfdir_php}/conf.d/30-pdo_sqlite.ini

%files tokenizer
%defattr(-, qsys, *none)
%{extension_dir}/tokenizer.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-tokenizer.ini

%files xml
%defattr(-, qsys, *none)
%{extension_dir}/dom.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-dom.ini

%{extension_dir}/simplexml.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-simplexml.ini

%{extension_dir}/xml.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-xml.ini

%{extension_dir}/xmlreader.so
%config(noreplace) %{sysconfdir_php}/conf.d/30-xmlreader.ini

%{extension_dir}/xmlwriter.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-xmlwriter.ini

%{extension_dir}/xsl.so
%config(noreplace) %{sysconfdir_php}/conf.d/30-xsl.ini

%if %{zip}
%files zip
%defattr(-, qsys, *none)
%{extension_dir}/zip.so
%config(noreplace) %{sysconfdir_php}/conf.d/20-zip.ini
%endif

%changelog
* Fri Jan 24 2020 Calvin Buckley <calvin@cmpct.info> - 7.3.14-0qsecofr
- Bump
- Enable libzip (will need rebuild on sonaming tho)
- Enable built-in PEAR and some comments if this will be a good idea or not

* Tue Oct 1 2019 Kevin Adler <kadler@us.ibm.com> - 7.3.6
- Always build with CURL built w/ OpenSSL 1.1
- Build sqlite extension shared & fix ownership
- Build with libwebp support

* Wed Jul 17 2019 Kevin Adler <kadler@us.ibm.com> - 7.3.6
- Bump to 7.3.6 and drop unneeded patches
- Add patch to fix set_timeout not working due to SIGPROF usage
- Don't link to libbsd due to issues; use php_flock wrapper for opcache
- Add BuildRequires for extensions and build them shared
