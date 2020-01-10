Name:          rgb
Version:       1.0.6
Release:       1qsecofr
Summary:       X.Org rgb database
Group:         System/X11
URL:           http://x.org
Source:        https://www.x.org/archive/individual/app/rgb-%{version}.tar.bz2
License:       MIT
BuildRequires: util-macros, xorgproto, sed-gnu, gcc-aix, make-gnu

%description
X.Org RGB database and utility to query it.

%prep
%setup -q

%build

%configure \
        CPPFLAGS="$CPPFLAGS -pthread" \
        LDFLAGS="$LDFLAGS -pthread -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}"
%make_build

%install

%make_install

%files
%defattr(-, qsys, *none)
%{_bindir}/showrgb
%{_datadir}/man/man1/showrgb.1
%{_datadir}/X11/rgb.txt
%doc COPYING ChangeLog README

%changelog
* Tue Dec 31 2019 Calvin Buckley <calvin@cmpct.info> - 1.0.6-1qsecofr
- New package for PASE
