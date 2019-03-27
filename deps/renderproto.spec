Summary:	X Render Extension
Name:		renderproto
Version:	0.11.1
Release:	4
License:	MIT
Group:		X11/Development/Libraries
Source0:	https://www.x.org/archive/individual/proto/%{name}-%{version}.tar.gz
URL:		http://fontconfig.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	autoconf, automake, libtool, m4-gnu, grep-gnu, tar-gnu, gzip
BuildRequires:	pkg-config, util-macros

%description
This package contains header files and documentation for the X render
extension.  Library and server implementations are separate.


%prep
%setup -q


%build

autoreconf -fiv
# There are no binary objects built, so tweaks are minimal.
%configure
%make_build

%install

%make_install

%files
%defattr(-, qsys, *none)
%doc renderproto.txt
%{_includedir}/X11/extensions/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/doc/renderproto/renderproto.txt
# Not needed for modern AIX and PASE
#%ifos aix5.1 || %ifos aix5.2 || %ifos aix5.3
#/usr/include/X11/extensions/*
#%endif


%changelog
* Tue Mar 26 2019 Calvin Buckley <calvin@cmpct.info> - 0.11.1-4
- Use xorg-macros package and fix up deps for implied

* Tue Mar 26 2019 Calvin Buckley <calvin@cmpct.info> - 0.11.1-3
- Convert for PASE

* Wed Nov 23 2016 Michael Perzl <michael@perzl.org> - 0.11.1-2
- account for system include files provided since AIX 6.1

* Thu Aug 22 2013 Michael Perzl <michael@perzl.org> - 0.11.1-1
- updated to version 0.11.1

* Thu Aug 22 2013 Michael Perzl <michael@perzl.org> - 0.11-1
- updated to version 0.11

* Wed Jan 16 2008 Michael Perzl <michael@perzl.org> - 0.9.3-1
- first version for AIX V5.1 and higher

