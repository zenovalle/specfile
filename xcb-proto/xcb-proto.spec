# Very important to manually specify the Python version.
# A generic "python" could be from OPS, which is Awful No Good.
%define python_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

Name:           xcb-proto
Version:        1.13
Release:        1
Summary:        XCB protocol descriptions

Group:          Development/Libraries
License:        MIT
URL:            http://xcb.freedesktop.org/
Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

# XXX
BuildRequires:	python2-devel >= 2.6.2
Requires:	python2 >= 2.6.2
Requires:       pkg-config

%description
XCB is a project to enable efficient language bindings to the X11 protocol.
This package contains the protocol descriptions themselves.  Language
bindings use these protocol descriptions to generate code for marshalling
the protocol.


%prep
%setup -q

%build

# Not a lot here since it doesn't make objects.

export PYTHON=python2

%configure
%make_build

%install

%make_install

%files
%defattr(-, qsys, *none)
%doc COPYING NEWS README TODO doc/xml-xcb.txt
%{_libdir}/pkgconfig/xcb-proto.pc
%dir %{_datadir}/xcb/
%{_datadir}/xcb/*.xsd
%{_datadir}/xcb/*.xml
%{python_sitelib}/xcbgen

%changelog
* Wed Mar 27 2019 Calvin Buckley <calvin@cmpct.info> - 1.10-1
- Update to latest
- De-AIX

* Wed Jul 03 2013 Michael Perzl <michael@perzl.org> - 1.8-1
- updated to version 1.8

* Wed Jul 03 2013 Michael Perzl <michael@perzl.org> - 1.7.1-1
- updated to version 1.7.1

* Wed Nov 10 2010 Michael Perzl <michael@perzl.org> - 1.6-1
- first version for AIX V5.1 and higher

