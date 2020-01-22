# XXX: The hardcoding of PHP version is very ugly, need to figure out how to solve elegantly
%define php_version 7.3
Name:        php-imagick
Version:     3.4.4
Release:     1qsecofr
Summary:     Provides a wrapper to the ImageMagick library.

License:     PHP
URL:         http://pecl.php.net/imagick
Source0:     http://pecl.php.net/get/imagick-%{version}.tgz
Source1:     php-imagick-99-imagick.ini

BuildRequires: ImageMagick-devel

BuildRequires: php-devel >= %{php_version}
# For fix-rpath
BuildRequires: pase-build-tools
# For tests
BuildRequires: php-cli >= %{php_version}
# Misc stuff that it'll throw up without otherwise
BuildRequires: sed-gnu m4-gnu make-gnu

Requires:    php-common >= %{php_version}

%description
Imagick is a native php extension to create and modify images using the ImageMagick API.
This extension requires ImageMagick version 6.5.3-10+ and PHP 5.4.0+.

%prep
%setup -q -n imagick-%{version}

%build

# Pretend to be AIX so shared libraries work (autoreconf doesn't work)
%define _host powerpc-ibm-aix6.1.9.0
%define _host_alias powerpc-ibm-aix6.1
%define _host_os aix6.1.9.0

phpize --clean
phpize
# XXX: Doesn't detect libm
export LDFLAGS="$LDFLAGS -lm"
%configure --with-imagick=/QOpenSys/pkgs
%make_build
# Ugh, there's no aix-soname support, so it'll only generate a shared .a and
# get confused. Let's fix that.
cp ./.libs/imagick.so ./modules/
# fix the rpath on the module since we won't let libtool touch see (see %install)
fix-rpath ./modules/imagick.so "/QOpenSys/pkgs/lib:/QOpenSys/usr/lib"

%install

# make install does NOT respect destdir, we will manually install this ourselves
# XXX: buggy coreutils workaround, update to latest or use 7.1 packages
mkdir -p %{buildroot}%{_libdir}/php-%{php_version}/extensions/
install -m 755 modules/imagick.so %{buildroot}%{_libdir}/php-%{php_version}/extensions/imagick.so
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php/conf.d/99-imagick.ini

%check
gmake test || true

%files
%defattr(-, qsys, *none)
%doc CREDITS LICENSE
%config(noreplace) %{_sysconfdir}/php/conf.d/99-imagick.ini
%{_libdir}/php-%{php_version}/extensions/imagick.so

%changelog
* Thu Jan 9 2020 Calvin Buckley <calvin@cmpct.info> - 3.4.4-1qsecofr
- First version

