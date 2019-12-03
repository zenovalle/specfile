# XXX: The hardcoding of PHP version is very ugly, need to figure out how to solve elegantly
%define php_version 7.3
Name:        php-ibm_db2
Version:     2.0.8
Release:     7qsecofr
Summary:     Extension for IBM DB2 Universal Database, IBM Cloudscape, and Apache Derby

License:     Apache-2.0
URL:         https://pecl.php.net/package/ibm_db2
Source0:     https://pecl.php.net/get/ibm_db2-%{version}.tgz
Source1:     php-ibm_db2-99-ibm_db2.ini
# Ugly hacks so we don't need to install global includes
Source2:     php-ibm_db2-sqlcli1.h
Patch0:      php-ibm_db2-no-global-header.diff

BuildRequires: php-devel >= %{php_version}
# For fix-rpath
BuildRequires: pase-build-tools
# For tests
BuildRequires: php-cli >= %{php_version}
# Misc stuff that it'll throw up without otherwise
BuildRequires: sed-gnu m4-gnu make-gnu

Requires:    php-common >= %{php_version}

%description
This extension supports IBM DB2 Universal Database, IBM
Cloudscape, and Apache Derby databases.

%prep
%setup -q -n ibm_db2-%{version}
%patch0 -p1

# Copy the SQL/CLI headers, because PASE doesn't have one out of the box
# Sometimes this can be installed globally, but not always. We won't
# assume such a thing. These are EBCDIC source PFs, so convert.
# XXX: May be a good idea to turn Cairns' libdb400 replacement into
# an RPM.
mkdir include
# We have to use CPY instead of reading with Rfile because of CCSIDs.
for header in $(ls /QIBM/include/sql*.h)
do
	system -v "CPY OBJ('$header') TODIR('./include') TOCCSID(*STDASCII) DTAFMT(*TEXT) REPLACE(*YES)"
done
cp %{SOURCE2} ./include/sqlcli1.h

%build

# Pretend to be AIX so shared libraries work (autoreconf doesn't work)
%define _host powerpc-ibm-aix6.1.9.0
%define _host_alias powerpc-ibm-aix6.1
%define _host_os aix6.1.9.0

phpize --clean
phpize
%configure --with-IBM_DB2=/QOpenSys/usr
%make_build
# for some reason, libtool gets confused and forgets to copy this
cp ./.libs/ibm_db2.so ./modules/
# fix the rpath on the module since we won't let libtool touch see (see %install)
fix-rpath ./modules/ibm_db2.so "/QOpenSys/pkgs/lib:/QOpenSys/usr/lib"

%install

# make install does NOT respect destdir, we will manually install this ourselves
# XXX: have to run mkdir -p and install without -D; i 7.2 specific?
mkdir -p %{buildroot}%{_libdir}/php-%{php_version}/extensions/
install -m 755 modules/ibm_db2.so %{buildroot}%{_libdir}/php-%{php_version}/extensions/ibm_db2.so
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php/conf.d/99-ibm_db2.ini

# test suite is incredibly fragile
#%check
# gmake test

%files
%defattr(-, qsys, *none)
%doc README LICENSE
%config(noreplace) %{_sysconfdir}/php/conf.d/99-ibm_db2.ini
%{_libdir}/php-%{php_version}/extensions/ibm_db2.so

%changelog
* Tue Dec 3 2019 Calvin Buckley <calvin@cmpct.info> - 2.0.9-7qsecofr
- Use CPY instead of Rfile, as Massimo points out

* Mon Dec 2 2019 Calvin Buckley <calvin@cmpct.info - 2.0.8-6qsecofr
- Fix on environments without SQL/CLI headers installed globally
- Polish dependencies further

* Mon Nov 25 2019 Calvin Buckley <calvin@cmpct.info - 2.0.8-5qsecofr
- New specfile for open source PHP RPM

