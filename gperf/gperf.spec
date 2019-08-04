Summary: A perfect hash function generator
Name: gperf
Version: 3.1
Release: 2
License: GPLv2+
Source0: ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz.sig
Group: Development/Tools
URL: http://www.gnu.org/software/%{name}/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# XXX: No.
# Requires: /sbin/install-info, info
Requires: libstdcplusplus6
BuildRequires: libstdcplusplus-devel

%description
Gperf is a perfect hash function generator written in C++. Simply
stated, a perfect hash function is a hash function and a data
structure that allows recognition of a key word in a set of words
using exactly one probe into the data structure.


%prep
%setup -q


%build

%configure \
    LDFLAGS="-maix${OBJECT_MODE} -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static
%make_build

%install

%make_install

%files
%defattr(-, qsys, *none)
%doc README NEWS doc/%{name}.html
%{_bindir}/gperf
%{_mandir}/man1/%{name}.1
%{_infodir}/%{name}.info
%{_datadir}/doc/gperf.html

%changelog
* Tue Mar 26 2019 Calvin Buckley <calvin@cmpct.info> 3.1-2
- De-AIX

* Thu Jan 05 2017 Michael Perzl <michael@perzl.org> - 3.1-1
- updated to version 3.1

* Wed Mar 11 2009 Michael Perzl <michael@perzl.org> - 3.0.4-1
- updated to version 3.0.4

* Tue Jun 17 2008 Michael Perzl <michael@perzl.org> - 3.0.3-1
- first version for AIX V5.1 and higher

