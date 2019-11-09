%bcond_with reconf

%undefine _disable_source_fetch

Name: R
Version: 3.6.1
Release: 8qsecofr
License: GPL-2.0-only
Summary: R Programming Language
Url: https://www.r-project.org

Source0: https://mirror.las.iastate.edu/CRAN/src/base/R-3/R-%{version}.tar.gz

# Not mentioned (optional): JDK 8.0 64-bit (mandatory LPP in V7R2)
BuildRequires: bzip2-devel
BuildRequires: curl-devel
BuildRequires: lapack-devel
BuildRequires: libffi-devel
BuildRequires: libiconv-devel
BuildRequires: libintl-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
BuildRequires: libutil-devel
BuildRequires: pcre-devel
BuildRequires: readline-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel
BuildRequires: libtiff-devel
BuildRequires: gcc-gfortran
BuildRequires: bison
BuildRequires: coreutils-gnu
BuildRequires: pkg-config
BuildRequires: cairo-devel
BuildRequires: pango-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libXmu-devel
BuildRequires: unzip
# XXX: tcl/tk? ICU? system lapack etc?

# TODO: Why is this required by R?
Requires: coreutils-gnu

%description
R is a programming language and free software environment for statistical
computing and graphics supported by the R Foundation for Statistical Computing.

The R language is widely used among statisticians and data miners for
developing statistical software and data analysis.

%package devel
Requires: %{name} = %{version}-%{release}
Group: Development/Libraries
Summary: Files needed for building R extensions

%description devel
The R-devel package contains the files needed for building R extensions.

%prep
%setup -q

%build

%if ! %{with reconf}
%define _host powerpc-ibm-aix6
%endif

# With this, JNI can be used with R.
# This is set to the 32-bit 7.x JVM, at least by default on V7R2
#     JAVA_HOME        : /QOpenSys/QIBM/ProdData/JavaVM/jdk80/64bit
#     Java library path: $(JAVA_HOME)/jre/lib/ppc64/compressedrefs
#     JNI cpp flags    : -I$(JAVA_HOME)/include -I$(JAVA_HOME)/include/aix
#     JNI linker flags : -L$(JAVA_HOME)/jre/lib/ppc64/compressedrefs -ljvm
#     Updating Java configuration in /QOpenSys/TempBuild/PackageEnv/BUILD/R-3.5.3
#     Done.
# export JAVA_HOME=/QOpenSys/QIBM/ProdData/JavaVM/jdk80/64bit

%configure \
    CFLAGS="-I%{_includedir} -I%{_includedir}/libiconv -pthread -ftls-model=global-dynamic" \
    CPPFLAGS="-I%{_includedir} -I%{_includedir}/libiconv -pthread" \
    CXXPICFLAGS="-I%{_includedir} -I%{_includedir}/libiconv -pthread -ftls-model=global-dynamic -fPIC -fpic -DPIC" \
    LDFLAGS="-pthread -liconv -Wl,-brtl,-liconv,-bbigtoc,-bnoexpall,-blibpath:%{_libdir}:%{_libdir}/R/lib:/QOpenSys/usr/lib" \
    SHLIB_CXX14LDFLAGS="-shared -pthread -Wl,-brtl -Wl,-bnoquiet -lc -lm" \
    SHLIB_CXX17LDFLAGS="-shared -pthread -Wl,-brtl -Wl,-bnoquiet -lc -lm" \
    SHLIB_CXXLDFLAGS="-shared -pthread -Wl,-brtl -Wl,-bnoquiet -lc -lm" \
    SHLIB_FCLDFLAGS="-shared -pthread -Wl,-brtl -Wl,-bnoquiet -lc -lm" \
    SHLIB_LDFLAGS="-shared -pthread -Wl,-brtl,-bnoquiet,-bnoexpall -lc -lm" \
    DYLIB_LDFLAGS="-shared -pthread -Wl,-brtl,-bnoquiet,-bnoexpall -lc -lm" \
    --enable-R-shlib \
    --enable-static=no \
    --disable-static \
    --enable-shared=yes \
    --with-readline \
    --with-blas \
    --with-cairo \
    --with-lapack \
    --with-libpng \
    --with-libtiff \
    --with-jpeglib \
    --enable-java=no \
    --with-x \
    --with-cairo \
    --with-recommended-packages \
    --with-internal-tzcode
    
echo cleaning now 
make clean
echo building now
%make_build

touch doc/NEWS.pdf

%install

%make_install

rm %{buildroot}%{_libdir}/charset.alias || :

%files
%defattr(-, qsys, *none)
%{_bindir}/*
%{_libdir}/R
%{_mandir}/man1/*

%exclude %{_libdir}/R/include
%exclude %{_libdir}/R/SVN-REVISION

%files devel
%defattr(-, qsys, *none)
%{_libdir}/R/include/*
%{_libdir}/pkgconfig/*.pc



%changelog

* Wed Sep 4 2019 Calvin Buckley <calvin@cmpct.info> - 3.6.1-8qsecofr
- Make shared libraries for packages include pthread (unbreaks std::mutex, which some use; a lot of references, but...)

* Wed Aug 7 2019 Calvin Buckley <calvin@cmpct.info> - 3.6.1-7qsecofr
- Just bump it to latest

* Tue Aug 6 2019 Calvin Buckley <calvin@cmpct.info> - 3.5.3-7qsecofr
- Bump
- Unzip is needed for the zoneinfo files
- Try building without Java, it might be a bit hairy on other systems to replicate

* Mon Aug 5 2019 Calvin Buckley <calvin@cmpct.info> - 3.5.1-6
- Add libXmu dependency
- Build with Java (8.0 64-bit, latest PASE will have this). Shouldn't be problematic since Erlang seems to install fine in such a configuration.

* Sun Aug 4 2019 Calvin Buckley <calvin@cmpct.info> - 3.5.1-5
- Build with Cairo
