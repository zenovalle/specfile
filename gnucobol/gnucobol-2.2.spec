Name:       gnucobol
Version:    2.2
Release:    1
Summary:    GnuCOBOL is a free COBOL compiler.
License:    FIXME
URL:        https://open-cobol.sourceforge.io/

Source0:    https://sourceforge.net/projects/open-cobol/files/gnu-cobol/2.2/gnucobol-2.2.tar.gz

Requires:   gmp-devel
Requires:   db
Requires:   ncurses-devel
Requires:   gcc
Requires:   autoconf
Requires:   automake
Requires:   libtool

Group:      Development

%description
GnuCOBOL is a free COBOL compiler.

%prep
%setup -q

%build
%configure --disable-rpath
make clean


make

%install
%make_install

%files
%defattr(-, qsys, *none)
/QOpenSys/pkgs/lib/libcob.la
/QOpenSys/pkgs/lib/libcob.a
/QOpenSys/pkgs/lib/gnucobol/CBL_OC_DUMP.so
/QOpenSys/pkgs/include/libcob/common.h
/QOpenSys/pkgs/include/libcob/cobgetopt.h
/QOpenSys/pkgs/include/libcob/exception.def
/QOpenSys/pkgs/include/libcob.h
/QOpenSys/pkgs/bin/cobc
/QOpenSys/pkgs/bin/cobcrun
/QOpenSys/pkgs/bin/cob-config
/QOpenSys/pkgs/share/man/man1/cobc.1
/QOpenSys/pkgs/share/man/man1/cobcrun.1
/QOpenSys/pkgs/share/gnucobol/config/default.conf
/QOpenSys/pkgs/share/gnucobol/config/cobol85.conf
/QOpenSys/pkgs/share/gnucobol/config/cobol2002.conf
/QOpenSys/pkgs/share/gnucobol/config/cobol2014.conf
/QOpenSys/pkgs/share/gnucobol/config/acu.conf
/QOpenSys/pkgs/share/gnucobol/config/mf.conf
/QOpenSys/pkgs/share/gnucobol/config/ibm.conf
/QOpenSys/pkgs/share/gnucobol/config/mvs.conf
/QOpenSys/pkgs/share/gnucobol/config/bs2000.conf
/QOpenSys/pkgs/share/gnucobol/config/rm.conf
/QOpenSys/pkgs/share/gnucobol/config/acu-strict.conf
/QOpenSys/pkgs/share/gnucobol/config/mf-strict.conf
/QOpenSys/pkgs/share/gnucobol/config/ibm-strict.conf
/QOpenSys/pkgs/share/gnucobol/config/mvs-strict.conf
/QOpenSys/pkgs/share/gnucobol/config/bs2000-strict.conf
/QOpenSys/pkgs/share/gnucobol/config/rm-strict.conf
/QOpenSys/pkgs/share/gnucobol/config/xopen.conf
/QOpenSys/pkgs/share/gnucobol/config/lax.conf-inc
/QOpenSys/pkgs/share/gnucobol/config/cobol85.words
/QOpenSys/pkgs/share/gnucobol/config/cobol2002.words
/QOpenSys/pkgs/share/gnucobol/config/cobol2014.words
/QOpenSys/pkgs/share/gnucobol/config/acu.words
/QOpenSys/pkgs/share/gnucobol/config/mf.words
/QOpenSys/pkgs/share/gnucobol/config/ibm.words
/QOpenSys/pkgs/share/gnucobol/config/mvs.words
/QOpenSys/pkgs/share/gnucobol/config/bs2000.words
/QOpenSys/pkgs/share/gnucobol/config/rm.words
/QOpenSys/pkgs/share/gnucobol/config/runtime.cfg
/QOpenSys/pkgs/share/gnucobol/config/runtime_empty.cfg
/QOpenSys/pkgs/share/gnucobol/copy/screenio.cpy
/QOpenSys/pkgs/share/gnucobol/copy/sqlca.cpy
/QOpenSys/pkgs/share/gnucobol/copy/sqlda.cpy
/QOpenSys/pkgs/share/locale/en@boldquot/LC_MESSAGES/gnucobol.mo
/QOpenSys/pkgs/share/locale/en@quot/LC_MESSAGES/gnucobol.mo
/QOpenSys/pkgs/share/locale/de/LC_MESSAGES/gnucobol.mo
/QOpenSys/pkgs/share/locale/es/LC_MESSAGES/gnucobol.mo
/QOpenSys/pkgs/share/locale/it/LC_MESSAGES/gnucobol.mo
/QOpenSys/pkgs/share/locale/ja/LC_MESSAGES/gnucobol.mo
/QOpenSys/pkgs/share/locale/nl/LC_MESSAGES/gnucobol.mo
/QOpenSys/pkgs/share/locale/pt/LC_MESSAGES/gnucobol.mo
/QOpenSys/pkgs/share/info/gnucobol.info

%changelog
* Sun Sep 1 2019 Yvan Janssens <qsecofr@qseco.fr> - 2.2-1
- Initial port to IBM i
