Summary: A GNU archiving program
Name: cpio-gnu
Version: 2.12
Release: 4
License: GPLv3+
Group: Applications/Archiving
URL: http://www.gnu.org/software/cpio/
Source0: ftp://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.bz2.sig

#BuildRequires: info
BuildRequires: gettext-tools, gcc-aix, tar-gnu, bzip2, make-gnu
#Requires: /sbin/install-info, info

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following arch*ive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%prep
# -n is because -gnu
%setup -q -n cpio-%{version}

%build

%configure \
    LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib" \
    --enable-largefile \
    --disable-mt \
    ac_cv_func_openat=no ac_cv_func_openat=no ac_cv_func_utimensat=no ac_cv_func_fstatat=no

%make_build

#if [ "%{dotests}" == 1 ]
#then
    gmake -k check || true
#fi

%install

%make_install

# toolbox strips binary and mungs infodir

%files
%defattr(-, qsys, *none)
%doc AUTHORS ChangeLog NEWS README THANKS TODO COPYING
%{_bindir}/cpio
%{_mandir}/man1/*
%{_infodir}/cpio.info
%{_datadir}/locale/*/LC_MESSAGES/*.mo
# why do you do this to me, gnu
%exclude %{_libdir}/charset.alias

%changelog
* Tue Jul 30 2019 Calvin Buckley <calvin@cmpct.info> - 2.12-4
- avoid using *at functions which PASE doesn't properly implement

* Tue Jul 23 2019 Calvin Buckley <calvin@cmpct.info> - 2.12-3
- convert for PASE

* Mon Nov 21 2016 Jean Girardet <jean.girardet@atos.net> - 2.12-2
- updated to version 2.12 from perzl version 2.11-2

* Thu Jul 01 2010 Michael Perzl <michael@perzl.org> - 2.11-2
- removed dependency on gettext >= 0.17

* Thu Apr 22 2010 Michael Perzl <michael@perzl.org> - 2.11-1
- updated to version 2.11

* Tue Jul 14 2009 Michael Perzl <michael@perzl.org> - 2.10-1
- updated to version 2.10

* Wed Mar 26 2008 Michael Perzl <michael@perzl.org> - 2.9-1
- first version for AIX V5.1 and higher

