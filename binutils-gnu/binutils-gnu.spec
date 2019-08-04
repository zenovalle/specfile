Summary: The GNU binutils development utilities
Name: binutils-gnu
Version: 2.32
Release: 3
License: GPLv3
Group: Development/Tools
URL: http://www.gnu.org/software/binutils/
Source0: http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2
Source1: http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2.sig
# XXX?
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gettext-tools, libintl-devel, readline-devel
# sigh, no shared libs without
BuildRequires: automake autoconf libtool
BuildRequires: gcc-aix >= 4.5.4-1
BuildRequires: bzip2
BuildRequires: zlib-devel >= 1.2.3-7
# Prereq: info, /sbin/install-info
Requires: libintl9
Requires: libz1 >= 1.2.3-7

%description
GNU binutils package contains utilities useful for development during
compilation.  Utilities such as nm, ar, elfdump, size, and others are included.

This package is specially modified to reduce conflicts with IBM equivalents,
as to preserve build environment compatibility.

%prep
%setup -q -n binutils-%{version}

%build

# XXX: powerpc-ibm-os400 isn't a recognized tuple, we need to pretend to be AIX
%define _host powerpc-ibm-aix
%define _host_alias powerpc-ibm-aix%{nil}
%define _host_os aix6.1

# XXX: May be worth autoreconfing because of the usual GNU/weirdness
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
# XXX: ugh, need to reconf to get shared libs working
autoreconf -fiv .
# XXX: Missing some flags too, i.e for AIX "emulation"?
%configure --with-system-zlib --with-system-readline --without-included-gettext \
    --disable-ld --disable-gold --disable-gas \
    --enable-64-bit-bfd --with-aix-soname=svr4
# XXX: This is ridiculous, but binutils runs configure scripts at make time...
# and it runs all of them in parallel if you let it (!) - seems to work, but
# output buffering gets extremely weird
%make_build

%install

# Incredibly dangerous looking but actually useful
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
%make_install

# Get rid of weird multilib (maybe?) cruft (prefix/powerpc-ibm-aix/...)
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}%{_prefix}/%{_host}

# /usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# GNU info isn't packaged
#mv -f ${RPM_BUILD_ROOT}%{_datadir}/man  ${RPM_BUILD_ROOT}%{_prefix}
#mv -f ${RPM_BUILD_ROOT}%{_datadir}/info ${RPM_BUILD_ROOT}%{_prefix}

#rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
#gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/*

# XXX: We should split binutils into seperate RPMs.
# Mono only really wants objdump for disassembly so the other GNU binutils
# (which are somewhat flaky on AIX) aren't wanted.
# (And those static libraries for BFD too!)

# The "ld" command is renamed to "gld".  For proper linking, please
# use the native AIX ld command, /usr/bin/ld.
# The "strip" command is not functioning correctly in all cases, so
# it has been renamed to "gstrip".  We strongly recommend the use
# of the native AIX strip command, /usr/bin/strip.
# Ditto for ranlib, as, nm, & ar.
# gas and ld are disabled
cd ${RPM_BUILD_ROOT}%{_bindir}
#mv ld gld
mv strip gstrip
mv ranlib granlib
mv ar gar
#mv as gas
mv nm gnm
#chmod 644 gld gstrip granlib gas gar gnm
chmod 644 gstrip granlib gar gnm


#%post
#/sbin/install-info %{_infodir}/as.info.gz        %{_infodir}/dir || :
#/sbin/install-info %{_infodir}/bfd.info.gz       %{_infodir}/dir || :
#/sbin/install-info %{_infodir}/binutils.info.gz  %{_infodir}/dir || :
#/sbin/install-info %{_infodir}/configure.info.gz %{_infodir}/dir || :
#/sbin/install-info %{_infodir}/standards.info.gz %{_infodir}/dir || :
#
#
#%preun
#if [ $1 = 0 ] ; then
# /sbin/install-info --delete %{_infodir}/as.info.gz        %{_infodir}/dir || :
# /sbin/install-info --delete %{_infodir}/bfd.info.gz       %{_infodir}/dir || :
# /sbin/install-info --delete %{_infodir}/binutils.info.gz  %{_infodir}/dir || :
# /sbin/install-info --delete %{_infodir}/configure.info.gz %{_infodir}/dir || :
# /sbin/install-info --delete %{_infodir}/standards.info.gz %{_infodir}/dir || :
#fi

%files
%defattr(-, qsys, *none)
%doc COPYING COPYING.LIB binutils/README binutils/NEWS
%{_bindir}/*
%{_libdir}/*
%{_mandir}/man1/*
%{_datadir}/locale/*
%{_includedir}/*
%{_infodir}/*

%changelog
* Tue Jul 23 2019 Calvin Buckley <calvin@cmpct.info> - 2.32-3
- Rename package to explicitly make it GNU
- Mung autotools

* Sat Apr 06 2019 Calvin Buckley <calvin@cmpct.info> - 2.32-2
- PASE conversion
- Disable tools

* Mon Feb 04 2019 Michael Perzl <michael@perzl.org> - 2.32-1
- updated to version 2.32

* Mon Jul 23 2018 Michael Perzl <michael@perzl.org> - 2.31.1-1
- updated to version 2.31.1

* Mon Jul 16 2018 Michael Perzl <michael@perzl.org> - 2.31-1
- updated to version 2.31

* Mon Jan 29 2018 Michael Perzl <michael@perzl.org> - 2.30-1
- updated to version 2.30

* Tue Sep 26 2017 Michael Perzl <michael@perzl.org> - 2.29.1-1
- updated to version 2.29.1

* Mon Jul 24 2017 Michael Perzl <michael@perzl.org> - 2.29-1
- updated to version 2.29

* Thu Mar 02 2017 Michael Perzl <michael@perzl.org> - 2.28-1
- updated to version 2.28

* Thu Aug 04 2016 Michael Perzl <michael@perzl.org> - 2.27-1
- updated to version 2.27

* Thu Jun 30 2016 Michael Perzl <michael@perzl.org> - 2.26.1-1
- updated to version 2.26.1

* Tue Jan 26 2016 Michael Perzl <michael@perzl.org> - 2.26-1
- updated to version 2.26

* Wed Jul 22 2015 Michael Perzl <michael@perzl.org> - 2.25.1-1
- updated to version 2.25.1

* Wed Jan 21 2015 Michael Perzl <michael@perzl.org> - 2.25-1
- updated to version 2.25

* Mon Dec 02 2013 Michael Perzl <michael@perzl.org> - 2.24-1
- updated to version 2.24

* Wed Mar 27 2013 Michael Perzl <michael@perzl.org> - 2.23.2-1
- updated to version 2.23.2

* Wed Mar 27 2013 Michael Perzl <michael@perzl.org> - 2.22-1
- first version for AIX V5.1 and higher
- based on the original SPEC file from IBM

