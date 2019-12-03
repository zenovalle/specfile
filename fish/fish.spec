Summary:                Friendly interactive shell
Name:                   fish

Version:                3.0.2
Release:                1qsecofr

License:                GPL-2.0
Group:                  System/Shells
URL:                    https://fishshell.com/

Source0:                https://github.com/fish-shell/fish-shell/releases/download/3.0.2/fish-3.0.2.tar.gz
BuildRequires:          ncurses-devel gettext-runtime libintl-devel gettext-tools
BuildRequires:          libstdcplusplus-devel readline-devel
BuildRequires:          zlib-devel bzip2-devel pcre-devel
BuildRequires:          cmake make-gnu gcc-cplusplus libutil-devel

Patch0: fish-3.0.2.diff

#BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Needs coreutils for [
Requires:               coreutils-gnu
#Requires:		bc
#Requires:		python
#Requires:		man

%description

fish is a shell geared towards interactive use. Its features are
focused on user friendliness and discoverability. The language syntax
is simple but incompatible with other shell languages.

%prep
%setup -q -n %{name}-3.0.2
%patch0 -p1

%build
#EXTRA_CMAKE_FLAGS="-DCURSES_EXTRA_LIBRARY=tinfo"
# CMake macros define -DBUILD_SHARED_LIBS:BOOL=ON, which breaks the
# bundled PCRE2 static library.
#EXTRA_CMAKE_FLAGS="$EXTRA_CMAKE_FLAGS -DBUILD_SHARED_LIBS:BOOL=OFF"

#%cmake -DZLIB_ROOT=/QOpenSys/pkgs -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} $EXTRA_CMAKE_FLAGS
# XXX: We need cmake rpm macros
mkdir build
cd build
cmake -DZLIB_ROOT=/QOpenSys/pkgs -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} $EXTRA_CMAKE_FLAGS ..
%make_build

%install

cd build
%make_install

%files
%defattr(-, qsys, *none)

# Language files
%{_datadir}/locale/*/LC_MESSAGES/fish.mo

# The documentation directory
%docdir %{_datadir}/doc/fish/
%{_datadir}/doc/fish/

# man files
%{_mandir}/man1/*
%docdir %{_datadir}/fish/man/man1/
%{_datadir}/fish/man/man1/

# The program binaries
%attr(0755, qsys, *none) %{_bindir}/*

# Configuration files
%dir %{_sysconfdir}/fish/
%config(noreplace) %{_sysconfdir}/fish/config.fish

# Support files
%{_datadir}/fish/

# pkgconfig
%{_datadir}/pkgconfig/fish.pc
