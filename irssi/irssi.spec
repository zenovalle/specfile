# XXX: sitearch isn't ideal, but vendorarch isn't configured and not sure of practice otherwise
%define perl_sitearch %(eval "`perl -V:installsitearch`"; echo $installsitearch)
%define perl_archlibexp %(eval "`perl -V:archlibexp`"; echo $archlibexp)
%define perl_version %(eval "`perl -V:version`"; echo $version)

Summary: Modular text mode IRC client with Perl scripting
Name: irssi
Version: 1.2.2
Release: 1qsecofr
License: GPLv2+
Source0: https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
URL: http://irssi.org

# Hard dependency because we install into site, which has a fixed version...
Requires: perl = %{perl_version}

# XXX: OTR support, UTF8Proc
BuildRequires: glib2-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: perl = %{perl_version}
BuildRequires: automake, autoconf, libtool

%package devel
Summary: Development package for irssi
Requires: %{name} = %{version}-%{release}

%description
Irssi is a modular IRC client with Perl scripting.

%description devel
This package contains headers needed to develop irssi plugins.

%prep
%setup -q

%build

autoreconf -fiv .
%configure \
    CPPFLAGS="-pthread" \
    LDFLAGS="-maix${OBJECT_MODE} -pthread -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static \
    --enable-true-color \
    --with-proxy --with-textui \
    --with-bot \
    --with-perl=yes \
    --with-perl-lib=site

%make_build

%install

%make_install

# cleanup droppings

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/modules/lib*.*a
rm -Rf $RPM_BUILD_ROOT/%{_docdir}/%{name}
find $RPM_BUILD_ROOT%{perl_vendorarch} -type f -a -name '*.bs' -a -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{perl_vendorarch} -type f -a -name .packlist -exec rm {} ';'

%files
%defattr(-, qsys, *none)
%doc docs/*.txt docs/*.html AUTHORS COPYING NEWS README.md TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/botti
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/%{name}.1*
%{perl_sitearch}/Irssi*
%{perl_sitearch}/auto/Irssi
%exclude %{perl_archlibexp}/perllocal.pod

%files devel
%defattr(-, qsys, *none)
%{_includedir}/irssi/

%changelog
* Sun Feb 9 2020 Calvin Buckley <calvin@cmpct.info> 1.2.2-1qsecofr
- New package
