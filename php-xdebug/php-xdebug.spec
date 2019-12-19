# XXX: The hardcoding of PHP version is very ugly, need to figure out how to solve elegantly
%define php_version 7.3
Name:        php-xdebug
Version:     2.9.0
Release:     1qsecofr
Summary:     Provides functions for function traces and profiling

License:     Xdebug
URL:         https://xdebug.org/
Source0:     https://xdebug.org/files/xdebug-%{version}.tgz
Source1:     php-xdebug-99-xdebug.ini

BuildRequires: php-devel >= %{php_version}
# For fix-rpath
BuildRequires: pase-build-tools
# For tests
BuildRequires: php-cli >= %{php_version}
# Misc stuff that it'll throw up without otherwise
BuildRequires: sed-gnu m4-gnu make-gnu

Requires:    php-common >= %{php_version}

%description
The Xdebug extension helps you debugging your script by providing a lot of
valuable debug information. The debug information that Xdebug can provide
includes the following:

* stack and function traces in error messages with:
o full parameter display for user defined functions
o function name, file name and line indications
o support for member functions
* memory allocation
* protection for infinite recursions

Xdebug also provides:

* profiling information for PHP scripts
* code coverage analysis
* capabilities to debug your scripts interactively with a debug client

%prep
%setup -q -n xdebug-%{version}

%build

# Pretend to be AIX so shared libraries work (autoreconf doesn't work)
%define _host powerpc-ibm-aix6.1.9.0
%define _host_alias powerpc-ibm-aix6.1
%define _host_os aix6.1.9.0

phpize --clean
phpize
%configure --enable-xdebug
%make_build
# Ugh, there's no aix-soname support, so it'll only generate a shared .a and
# get confused. Let's fix that.
cp ./.libs/xdebug.so ./modules/
# fix the rpath on the module since we won't let libtool touch see (see %install)
fix-rpath ./modules/xdebug.so "/QOpenSys/pkgs/lib:/QOpenSys/usr/lib"

%install

# make install does NOT respect destdir, we will manually install this ourselves
# XXX: buggy coreutils workaround, update to latest or use 7.1 packages
mkdir -p %{buildroot}%{_libdir}/php-%{php_version}/extensions/
install -m 755 modules/xdebug.so %{buildroot}%{_libdir}/php-%{php_version}/extensions/xdebug.so
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php/conf.d/99-xdebug.ini

%check
# Some tests might fail if php.ini isn't set right or something's using port 9000
gmake test || true

%files
%defattr(-, qsys, *none)
%doc CREDITS README.rst LICENSE
%config(noreplace) %{_sysconfdir}/php/conf.d/99-xdebug.ini
%{_libdir}/php-%{php_version}/extensions/xdebug.so

%changelog
* Thu Dec 19 2019 Calvin Buckley <calvin@cmpct.info> - 2.9.0-1qsecofr
- First version

