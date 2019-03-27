Summary: X.Org X11 AIX compatibility layer
Name: xorg-compat-aix
Version: 1.2
Release: 2
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Source0: x11.pc
Source1: xproto.pc
Source2: xext.pc
Source3: xextproto.pc
Source5: fixesproto.pc
Source6: xfixes.pc
Source7: glproto.pc
Source8: xt.pc
Source9: xmu.pc
Source10: sm.pc
Source11: ice.pc

BuildRequires: pkg-config
Requires: pkg-config

%description
This RPM package provides a pkg-config compatibility layer for X11 on AIX.


%prep


%build
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig

cp %{SOURCE0} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE6} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE7} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE8} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE9} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE10} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{SOURCE11} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig

chmod 0644 ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/*


%install


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-, qsys, *none)
%{_libdir}/pkgconfig/*.pc


%changelog
* Wed Mar 27 2019 Calvin Buckley <calvin@cmpct.info> - 1.2-2
- Convert for PASE

* Thu Aug 22 2013 Michael Perzl <michael@perzl.org> - 1.2-1
- removed randrproto.pc, you need the 'randrproto' RPM for it now

* Sun Jun 03 2012 Michael Perzl <michael@perzl.org> - 1.1-1
- added xt.pc, xmu.pc, sm.pc and ice.pc
- increased version of randrproto.pc to 1.3

* Fri Nov 13 2009 Michael Perzl <michael@perzl.org> - 1.0-1
- first version for AIX V5.1 and higher
