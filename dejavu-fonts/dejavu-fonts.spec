%global fontname    dejavu
%global archivename %{name}-%{archiveversion}

%define _fontdir %{_datadir}/fonts
%define _fontconfig_confdir %{_sysconfdir}/fonts/conf.d
%define _fontconfig_templatedir %{_datadir}/fontconfig/conf.avail

Name:    %{fontname}-fonts
Version: 2.37
Release: 2
Summary: DejaVu fonts
Group:   User Interface/X
License: Bitstream Vera and Public Domain
URL:     http://%{name}.org/
Source0: http://sourceforge.net/projects/%{fontname}/files/%{fontname}/%{version}/%{name}-ttf-%{version}.tar.bz2
Source1: http://sourceforge.net/projects/%{fontname}/files/%{fontname}/%{version}/%{fontname}-lgc-fonts-ttf-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

BuildRequires: bzip2

%description
This is just a dummy to satisfy RPM.


%package -n %{fontname}-sans-fonts
Summary:  Variable-width sans-serif font faces
Group:    User Interface/X
Requires: fontconfig

%description -n %{fontname}-sans-fonts
The DejaVu font set is based on the Bitstream Vera fonts, release 1.10. Its
purpose is to provide a wider range of characters, while maintaining the
original style, using an open collaborative development process.

This package consists of the DejaVu sans-serif variable-width font faces, in
their unabridged version.


%package -n %{fontname}-serif-fonts
Summary:  Variable-width serif font faces
Group:    User Interface/X
Requires: fontconfig

%description -n %{fontname}-serif-fonts
The DejaVu font set is based on the Bitstream Vera fonts, release 1.10. Its
purpose is to provide a wider range of characters, while maintaining the
original style, using an open collaborative development process.

This package consists of the DejaVu serif variable-width font faces, in their
unabridged version.


%package -n %{fontname}-sans-mono-fonts
Summary:  Monospace sans-serif font faces
Group:    User Interface/X
Requires: fontconfig

%description -n %{fontname}-sans-mono-fonts
The DejaVu font set is based on the Bitstream Vera fonts, release 1.10. Its
purpose is to provide a wider range of characters, while maintaining the
original style, using an open collaborative development process.

This package consists of the DejaVu sans-serif monospace font faces, in their
unabridged version.


%package -n %{fontname}-lgc-sans-fonts
Summary:  Variable-width sans-serif font faces, Latin-Greek-Cyrillic subset
Group:    User Interface/X
Requires: fontconfig

%description -n %{fontname}-lgc-sans-fonts
The DejaVu font set is based on the Bitstream Vera fonts, release 1.10. Its
purpose is to provide a wider range of characters, while maintaining the
original style, using an open collaborative development process.

This package consists of the DejaVu sans-serif variable-width font faces, with
unicode coverage restricted to Latin, Greek and Cyrillic.


%package -n %{fontname}-lgc-serif-fonts
Summary:  Variable-width serif font faces, Latin-Greek-Cyrillic subset
Group:    User Interface/X
Requires: fontconfig

%description -n %{fontname}-lgc-serif-fonts
The DejaVu font set is based on the Bitstream Vera fonts, release 1.10. Its
purpose is to provide a wider range of characters, while maintaining the
original style, using an open collaborative development process.

This package consists of the DejaVu serif variable-width font faces, with
unicode coverage restricted to Latin, Greek and Cyrillic.


%package -n %{fontname}-lgc-sans-mono-fonts
Summary:  Monospace sans-serif font faces, Latin-Greek-Cyrillic subset
Group:    User Interface/X
Requires: fontconfig

%description -n %{fontname}-lgc-sans-mono-fonts
The DejaVu font set is based on the Bitstream Vera fonts, release 1.10. Its
purpose is to provide a wider range of characters, while maintaining the
original style, using an open collaborative development process.

This package consists of the DejaVu sans-serif monospace font faces, with
unicode coverage restricted to Latin, Greek and Cyrillic.


%prep
%setup -q -n %{name}-ttf-%{version} -a 1
cd %{fontname}-lgc-fonts-ttf-%{version}
tar cf - . | (cd `pwd`/.. && tar xpf -)


%build


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_fontdir}/%{fontname}
chmod 0755 ${RPM_BUILD_ROOT}%{_fontdir}/%{fontname}

cp ttf/*.ttf ${RPM_BUILD_ROOT}%{_fontdir}/%{fontname}/
chmod 0644 ${RPM_BUILD_ROOT}%{_fontdir}/%{fontname}/*

mkdir -p ${RPM_BUILD_ROOT}%{_fontconfig_confdir}
mkdir -p ${RPM_BUILD_ROOT}%{_fontconfig_templatedir}

cd fontconfig
for f in *conf ; do
    cp ${f} ${RPM_BUILD_ROOT}%{_fontconfig_templatedir}/
    ln -s %{_fontconfig_templatedir}/${f} ${RPM_BUILD_ROOT}%{_fontconfig_confdir}/${f}
done
chmod 0644 ${RPM_BUILD_ROOT}%{_fontconfig_templatedir}/*.conf


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n %{fontname}-sans-fonts
%defattr(-, qsys, *none)
%doc AUTHORS BUGS LICENSE NEWS README.md
%{_fontconfig_confdir}/*-%{fontname}-sans.conf
%{_fontconfig_templatedir}/*-%{fontname}-sans.conf
%dir %{_fontdir}/%{fontname}
%{_fontdir}/%{fontname}/DejaVuSans.ttf
%{_fontdir}/%{fontname}/DejaVuSans-*.ttf
%{_fontdir}/%{fontname}/DejaVuSansCondensed*.ttf
%{_fontdir}/%{fontname}/DejaVuMathTeXGyre.ttf


%files -n %{fontname}-serif-fonts
%defattr(-, qsys, *none)
%doc AUTHORS BUGS LICENSE NEWS README.md
%{_fontconfig_confdir}/*-%{fontname}-serif.conf
%{_fontconfig_templatedir}/*-%{fontname}-serif.conf
%dir %{_fontdir}/%{fontname}
%{_fontdir}/%{fontname}/DejaVuSerif.ttf
%{_fontdir}/%{fontname}/DejaVuSerif-*.ttf
%{_fontdir}/%{fontname}/DejaVuSerifCondensed*.ttf


%files -n %{fontname}-sans-mono-fonts
%defattr(-, qsys, *none)
%doc AUTHORS BUGS LICENSE NEWS README.md
%{_fontconfig_confdir}/*-%{fontname}-sans-mono.conf
%{_fontconfig_templatedir}/*-%{fontname}-sans-mono.conf
%dir %{_fontdir}/%{fontname}
%{_fontdir}/%{fontname}/DejaVuSansMono*.ttf


%files -n %{fontname}-lgc-sans-fonts
%defattr(-, qsys, *none)
%doc AUTHORS BUGS LICENSE NEWS README.md
%{_fontconfig_confdir}/*-%{fontname}-lgc-sans.conf
%{_fontconfig_templatedir}/*-%{fontname}-lgc-sans.conf
%dir %{_fontdir}/%{fontname}
%{_fontdir}/%{fontname}/DejaVuLGCSans.ttf
%{_fontdir}/%{fontname}/DejaVuLGCSans-*.ttf
%{_fontdir}/%{fontname}/DejaVuLGCSansCondensed*.ttf


%files -n %{fontname}-lgc-serif-fonts
%defattr(-, qsys, *none)
%doc AUTHORS BUGS LICENSE NEWS README.md
%{_fontconfig_confdir}/*-%{fontname}-lgc-serif.conf
%{_fontconfig_templatedir}/*-%{fontname}-lgc-serif.conf
%dir %{_fontdir}/%{fontname}
%{_fontdir}/%{fontname}/DejaVuLGCSerif.ttf
%{_fontdir}/%{fontname}/DejaVuLGCSerif-*.ttf
%{_fontdir}/%{fontname}/DejaVuLGCSerifCondensed*.ttf


%files -n %{fontname}-lgc-sans-mono-fonts
%defattr(-, qsys, *none)
%doc AUTHORS BUGS LICENSE NEWS README.md
%{_fontconfig_confdir}/*-%{fontname}-lgc-sans-mono.conf
%{_fontconfig_templatedir}/*-%{fontname}-lgc-sans-mono.conf
%dir %{_fontdir}/%{fontname}
%{_fontdir}/%{fontname}/DejaVuLGCSansMono*.ttf


%changelog
* Wed Mar 26 2019 Calvin Buckley <calvin@cmpct.info> - 2.37-2
- PASE conversion
- Include DejaVuMathTeXGyre.ttf that Perzl didn't which trips up RPM

* Thu Oct 11 2018 Michael Perzl <michael@perzl.org> - 2.37-1
- updated to version 2.37

* Thu Oct 11 2018 Michael Perzl <michael@perzl.org> - 2.36-1
- updated to version 2.36

* Wed Aug 26 2015 Michael Perzl <michael@perzl.org> - 2.35-1
- updated to version 2.35

* Mon Aug 26 2013 Michael Perzl <michael@perzl.org> - 2.34-1
- updated to version 2.34

* Fri Mar 11 2011 Michael Perzl <michael@perzl.org> - 2.33-1
- first version for AIX V5.1 and higher

