Name: erlang
Version: 22.2
Release: 1qsecofr
Summary: General-purpose programming language and runtime environment
License: Apache-2.0
Group: Development/Languages
URL: http://www.erlang.org

Source: http://www.erlang.org/download/otp_src_%{version}.tar.gz
Source1: http://www.erlang.org/download/otp_doc_html_%{version}.tar.gz
Source2: http://www.erlang.org/download/otp_doc_man_%{version}.tar.gz
Patch1: erlang-aix.patch
Patch2: erlang-getifaddrs.patch
Patch3: erlang-esock.diff
Patch4: erlang-linker.patch
# XXX: Not a complete solution. Unfortunately, LDFLAGS gets passed around for
# both ld and cxxld invocations. This gets some, but not all. This does mean
# some ugly rpath on many binaries for now, unfortunately...
Patch5: erlang-rpath.diff

# BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

# Interestingly, under PASE, Erlang will likely see J9 under the default path.
# This will build the Java modules for Erlang too.
BuildRequires: flex
BuildRequires: m4-gnu
BuildRequires: autoconf, automake, libtool, gcc-aix, bash
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: unixODBC-devel
BuildRequires: zlib-devel
BuildRequires: libxml2-tools
# Not really? Seems to be wx now
#BuildRequires: tcl-devel
#BuildRequires: tk-devel
#Requires: tk

# Added virtual Provides for each erlang module
Provides: erlang-appmon = %{version}-%{release}
Provides: erlang-asn1 = %{version}-%{release}
Provides: erlang-common_test = %{version}-%{release}
Provides: erlang-compiler = %{version}-%{release}
Provides: erlang-cosEvent = %{version}-%{release}
Provides: erlang-cosEventDomain = %{version}-%{release}
Provides: erlang-cosFileTransfer = %{version}-%{release}
Provides: erlang-cosNotification = %{version}-%{release}
Provides: erlang-cosProperty = %{version}-%{release}
Provides: erlang-cosTime = %{version}-%{release}
Provides: erlang-cosTransactions = %{version}-%{release}
Provides: erlang-crypto = %{version}-%{release}
Provides: erlang-debugger = %{version}-%{release}
Provides: erlang-dialyzer = %{version}-%{release}
Provides: erlang-docbuilder = %{version}-%{release}
Provides: erlang-edoc = %{version}-%{release}
Provides: erlang-erts = %{version}-%{release}
Provides: erlang-et = %{version}-%{release}
Provides: erlang-eunit = %{version}-%{release}
Provides: erlang-gs = %{version}-%{release}
Provides: erlang-hipe = %{version}-%{release}
Provides: erlang-ic = %{version}-%{release}
Provides: erlang-inets = %{version}-%{release}
Provides: erlang-inviso = %{version}-%{release}
Provides: erlang-kernel = %{version}-%{release}
Provides: erlang-megaco = %{version}-%{release}
Provides: erlang-mnesia = %{version}-%{release}
Provides: erlang-observer = %{version}-%{release}
Provides: erlang-odbc = %{version}-%{release}
Provides: erlang-orber = %{version}-%{release}
Provides: erlang-os_mon = %{version}-%{release}
Provides: erlang-otp_mibs = %{version}-%{release}
Provides: erlang-parsetools = %{version}-%{release}
Provides: erlang-percept = %{version}-%{release}
Provides: erlang-pman = %{version}-%{release}
Provides: erlang-public_key = %{version}-%{release}
Provides: erlang-runtime_tools = %{version}-%{release}
Provides: erlang-sasl = %{version}-%{release}
Provides: erlang-snmp = %{version}-%{release}
Provides: erlang-ssh = %{version}-%{release}
Provides: erlang-ssl = %{version}-%{release}
Provides: erlang-stdlib = %{version}-%{release}
Provides: erlang-syntax_tools = %{version}-%{release}
Provides: erlang-test_server = %{version}-%{release}
Provides: erlang-toolbar = %{version}-%{release}
Provides: erlang-tools = %{version}-%{release}
Provides: erlang-tv = %{version}-%{release}
Provides: erlang-typer = %{version}-%{release}
Provides: erlang-webtool = %{version}-%{release}
Provides: erlang-xmerl = %{version}-%{release}

%description
Erlang is a general-purpose programming language and runtime
environment. Erlang has built-in support for concurrency, distribution
and fault tolerance. Erlang is used in several large telecommunication
systems from Ericsson.

%package doc
Summary: Erlang documentation
Group: Development/Languages

%description doc
Documentation for Erlang.

%prep

%setup -q -n otp_src_%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1



%build
#
# WARNING : pcre-devel must be desinstalled to properly compile erlang
#
# XXX: Really?

export CFLAGS=$RPM_OPT_FLAGS
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
# XXX: ???
export erl_xcomp_poll=no
# We use the AIX nm with the -B option to display the symbols in the BSD format
# XXX: ???
# export NM="/usr/bin/nm -X32_64 -B"

# Regen build system
./otp_build autoconf
# XXX: Erlang uses both ld raw and ccld in LDFLAGS, too risky to use anything with -Wl
%configure  \
    LDFLAGS="-L/QOpenSys/pkgs/lib" \
    --with-odbc=/QOpenSys/pkgs --with-ssl=/QOpenSys/pkgs \
    --with-aix-soname=svr4 --enable-shared --disable-static

%make_build

%install

%make_install

# clean up
find ${RPM_BUILD_ROOT}%{_libdir}/erlang -perm 0775 | xargs chmod 755
find ${RPM_BUILD_ROOT}%{_libdir}/erlang -name Makefile | xargs chmod 644
find ${RPM_BUILD_ROOT}%{_libdir}/erlang -name \*.o | xargs chmod 644

# doc
cd ${RPM_BUILD_DIR}/otp_src_%{version}
mkdir -p erlang_doc

tar -C erlang_doc -zxf %{SOURCE1}
tar -C ${RPM_BUILD_ROOT}%{_libdir}/erlang -zxf %{SOURCE2}

%files
%defattr(-, qsys, *none)
%doc AUTHORS LICENSE.txt README.md
%{_bindir}/*
%{_libdir}/erlang

%files doc
%defattr(-, qsys, *none)
%doc erlang_doc*

# XXX: Is this really needed?
#%post
#%{_libdir}/erlang/Install -minimal %{_libdir}/erlang &>/dev/null

%changelog
* Tue Jan 21 2020 Calvin Buckley <calvin@cmpct.info> 22.2-1qsecofr
- Update to OTP 22.2

* Sat Mar 30 2019 Calvin Buckley <calvin@cmpct.info> 22.0-rc1
- Update to OTP 21.3
- De-AIX

* Wed Feb 6 2013 Bernard Cahen <bernard.cahen@bull.net> - R15B02-1
- Version for AIX 6.1

* Thu Mar 31 2011 Steve Huff <shuff@vecna.org> - R14B02-1
- Updated to version R14B02.
- HiPE and the halfword emulator cannot currently coexist.
- We can use a more modern Java on el6.
- Captured WxWidgets dependency.

* Thu Sep 02 2010 Steve Huff <shuff@vecna.org> - R14A-1
- Updated to version R14A.

* Fri Jul 02 2010 Steve Huff <shuff@vecna.org> - R12B-5.12
- Argh, Erlang uses standard man page format, but its man pages really are
  not supposed to be installed in man's search path. Huh.

* Thu Jul 01 2010 Steve Huff <shuff@vecna.org> -
- A few man pages conflict with distro files; renamed them.

* Fri Jun 25 2010 Steve Huff <shuff@vecna.org> - R12B-5.11
- Ported from EPEL.
- Turned on some additional compile-time options.
- Moved man pages into standard $MANPATH.

* Mon Jun 7 2010 Peter Lemenkov <lemenkov@gmail.com> - R12B-5.10
- Added missing virtual provides erlang-erts

* Tue May 25 2010 Peter Lemenkov <lemenkov@gmail.com> - R12B-5.9
- Use java-1.4.2 only for EL-[45]
- Added virtual provides for each erlang module
- Small typo fix

* Mon Apr 19 2010 Peter Lemenkov <lemenkov@gmail.com> - R12B-5.8
- Patches rebased
- Added patches 6,7 from trunk
- Use %%configure

* Tue Apr 21 2009 Debarshi Ray <rishi@fedoraproject.org> R12B-5.7
- Updated rpath patch.
- Fixed configure to respect $RPM_OPT_FLAGS.

* Sun Mar 1 2009 Gerard Milmeister <gemi@bluewin.ch> - R12B-5.6
- new release R12B-5
- link escript and dialyzer to %{_bindir}

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - R12B-5.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Dennis Gilmore <dennis@ausil.us> - R12B-4.5
- fix sparc arches to compile

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - R12B-4.4
- rebuild with new openssl

* Sat Oct 25 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-4.1
- new release R12B-4

* Fri Sep 5 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-3.3
- fixed sslrpath patch

* Thu Jul 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> - R12B-3.2
- fix license tag

* Sun Jul 6 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-3.1
- new release R12B-3

* Thu Mar 27 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-1.1
- new release R12B-1

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-0.3
- disable strict aliasing optimization

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - R12B-0.2
- Autorebuild for GCC 4.3

* Sat Dec 8 2007 Gerard Milmeister <gemi@bluewin.ch> - R12B-0.1
- new release R12B-0

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - R11B-6
 - Rebuild for deps

* Sun Aug 19 2007 Gerard Milmeister <gemi@bluewin.ch> - R11B-5.3
- fix some permissions

* Sat Aug 18 2007 Gerard Milmeister <gemi@bluewin.ch> - R11B-5.2
- enable dynamic linking for ssl

* Sat Aug 18 2007 Gerard Milmeister <gemi@bluewin.ch> - R11B-5.1
- new release R11B-5

* Sat Mar 24 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - R11B-2.4
- Require java-1.5.0-gcj-devel for build.

* Sun Dec 31 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-2.3
- remove buildroot from installed files

* Sat Dec 30 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-2.2
- added patch for compiling with glibc 2.5

* Sat Dec 30 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-2.1
- new version R11B-2

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-0.3
- Rebuild for FE6

* Wed Jul 5 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-0.2
- add BR m4

* Thu May 18 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-0.1
- new version R11B-0

* Wed May 3 2006 Gerard Milmeister <gemi@bluewin.ch> - R10B-10.3
- added patch for run_erl by Knut-Håvard Aksnes

* Mon Mar 13 2006 Gerard Milmeister <gemi@bluewin.ch> - R10B-10.1
- new version R10B-10

* Thu Dec 29 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-9.1
- New Version R10B-9

* Sat Oct 29 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-8.2
- updated rpath patch

* Sat Oct 29 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-8.1
- New Version R10B-8

* Sat Oct 1 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.4
- Added tk-devel and tcl-devel to buildreq
- Added tk to req

* Tue Sep 6 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.3
- Remove perl BuildRequires

* Tue Aug 30 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.2
- change /usr/lib to %%{_libdir}
- redirect output in %%post to /dev/null
- add unixODBC-devel to BuildRequires
- split doc off to erlang-doc package

* Sat Jun 25 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.1
- New Version R10B-6

* Sun Feb 13 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-3.1
- New Version R10B-3

* Mon Dec 27 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:R10B-2-0.fdr.1
- New Version R10B-2

* Wed Oct 6 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:R10B-0.fdr.1
- New Version R10B

* Thu Oct 16 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:R9B-1.fdr.1
- First Fedora release


