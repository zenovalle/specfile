# XXX: The hardcoding of PHP version is very ugly, need to figure out how to solve elegantly
%define php_version 7.3
Name:        php-pdo_ibm
Version:     1.3.6
Release:     0zenovalle
Summary:     PDO driver for IBM databases

License:     Apache-2.0
URL:         https://pecl.php.net/package/PDO_IBM
Source0:     https://pecl.php.net/get/PDO_IBM-%{version}.tgz
Source1:     php-pdo_ibm-99-pdo_ibm.ini
Patch0:      php-pdo_ibm-ibm_driver.diff
Patch1:      php-pdo_ibm-ibm_statement.diff
Patch2:      php-pdo_ibm-config.diff

BuildRequires: php-devel >= %{php_version}
# For fix-rpath
BuildRequires: pase-build-tools
# For tests
BuildRequires: php-cli >= %{php_version}
# Misc stuff that it'll throw up without otherwise
BuildRequires: sed-gnu m4-gnu make-gnu
# SQL CLI headers
BuildRequires: sqlcli-devel

Requires:    php-common >= %{php_version}

%description
This extension provides an IBM database driver for PDO. This driver supports IBM DB2
Universal Database, IBM Cloudscape, Apache Derby databases and IDS (Informix Data Server).

%prep
%setup -q -n pdo_ibm-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Copy the SQL/CLI headers, because PASE doesn't have one out of the box
# Sometimes this can be installed globally, but not always. We won't
# assume such a thing. These are EBCDIC source PFs, so convert.
# XXX: May be a good idea to turn Cairns' libdb400 replacement into
# an RPM.
mkdir include
# We have to use CPY instead of reading with Rfile because of CCSIDs.
system -v "CPY OBJ('/QIBM/include/sqlca.h') TODIR('./include') TOCCSID(*STDASCII) DTAFMT(*TEXT) REPLACE(*YES)"

%build

# Pretend to be AIX so shared libraries work (autoreconf doesn't work)
%define _host powerpc-ibm-aix6.1.9.0
%define _host_alias powerpc-ibm-aix6.1
%define _host_os aix6.1.9.0

phpize --clean
phpize
%configure CFLAGS="$CFLAGS -DPASE" PHP_PDO_IBM_LIB="/QOpenSys/pkgs" --with-pdo-ibm=/QOpenSys/usr
%make_build
# for some reason, libtool gets confused and forgets to copy this
cp ./.libs/pdo_ibm.so ./modules/
# fix the rpath on the module since we won't let libtool touch see (see %install)
fix-rpath ./modules/pdo_ibm.so "/QOpenSys/pkgs/lib:/QOpenSys/usr/lib"

%install

# make install does NOT respect destdir, we will manually install this ourselves
# XXX: have to run mkdir -p and install without -D; i 7.2 specific?
mkdir -p %{buildroot}%{_libdir}/php-%{php_version}/extensions/
install -m 755 modules/pdo_ibm.so %{buildroot}%{_libdir}/php-%{php_version}/extensions/pdo_ibm.so
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php/conf.d/99-pdo_ibm.ini

# test suite is incredibly fragile
#%check
# gmake test

%files
%defattr(-, qsys, *none)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/php/conf.d/99-pdo_ibm.ini
%{_libdir}/php-%{php_version}/extensions/pdo_ibm.so

%changelog
* Wed Mar 04 2020 Roberto Bizzozero <zenovalle@gmail.com> - 1.3.6-0zenovalle
- New specfile for open source PHP RPM

