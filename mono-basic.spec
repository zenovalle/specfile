Name:           mono-basic
BuildRequires:  mono-devel mono-winforms bzip2
License:        LGPL v2.1 only
Group:          Development/Languages/Mono
Summary:        Mono's VB Runtime
Url:            http://go-mono.org/
Version:	4.7
Release:	1
Source0:        http://download.mono-project.com/sources/mono-basic/%{name}-%{version}.tar.bz2
Patch0:         mono-basic-fix-hardcoded.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono's VB runtime.

%files
%defattr(-, qsys, *none)
%_mandir/man1/vbnc.1*
%_prefix/bin/vbnc*
%_prefix/lib/mono/*/Microsoft.VisualBasic.dll
%_prefix/lib/mono/*/Mono.Cecil.VB*.dll
%_prefix/lib/mono/4.5/vbnc*
%_prefix/lib/mono/gac/Microsoft.VisualBasic
%_prefix/lib/mono/gac/Mono.Cecil.VB*

%prep
%setup -q
%patch0 -p1

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_prefix}/lib/mono/2.0/extract-source.exe*
rm -f %{buildroot}%{_prefix}/lib/mono/2.0/rt-console.exe*
rm -f %{buildroot}%{_prefix}/lib/mono/2.0/rt-execute.exe*
rm -f %{buildroot}%{_prefix}/lib/mono/2.0/rt.exe*

%clean
rm -rf %{buildroot}

%changelog
* Tue Apr 2 2019 Calvin Buckley <calvin@cmpct.info> - 4.7-1
- Manual editing of specfile for IBM i conventions
