Name:          imake
# XXX: Build somehow makes ccmakedep in cpp
Version:       1.0.6
Release:       1
Summary:       X.Org imake build tool
Group:         System/X11
URL:           http://x.org
Source:        https://www.x.org/archive/individual/util/imake-%{version}.tar.bz2
License:       MIT
BuildRequires: util-macros, xorgproto, sed-gnu, gcc-aix, make-gnu

%description
X.Org imake build tool.

%prep
%setup -q

# Fix a hardcoded path.
sed -i 's/\/usr\/bin\/perl/\/QOpenSys\/pkgs\/bin\/perl/' mkhtmlindex.pl

%build

%configure \
        CPPFLAGS="$CPPFLAGS -pthread" \
        LDFLAGS="$LDFLAGS -pthread -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}"
%make_build

%install

%make_install

%files
%defattr(-, qsys, *none)
%{_bindir}/ccmakedep
%{_bindir}/cleanlinks
%{_bindir}/imake
%{_bindir}/makeg
%{_bindir}/mergelib
%{_bindir}/mkdirhier
%{_bindir}/mkhtmlindex
%{_bindir}/revpath
%{_bindir}/xmkmf
%{_datadir}/man/man1/ccmakedep.1
%{_datadir}/man/man1/cleanlinks.1
%{_datadir}/man/man1/imake.1
%{_datadir}/man/man1/makeg.1
%{_datadir}/man/man1/mergelib.1
%{_datadir}/man/man1/mkdirhier.1
%{_datadir}/man/man1/mkhtmlindex.1
%{_datadir}/man/man1/revpath.1
%{_datadir}/man/man1/xmkmf.1
%doc COPYING ChangeLog README

%changelog
* Tue Jul 30 2019 Calvin Buckley <calvin@cmpct.info> - 1.0.6-1
- Bump (though not to latest due to build errors)
- PASE

* Tue Jun 18 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.5-1
- Initial port on Aix6.1

