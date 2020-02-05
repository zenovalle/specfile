Name: elixir
Version: 1.10.0
Release: 1qsecofr
Summary: Dynamic, functional language designed for building scalable and maintainable applications
License: Apache-2.0
Group: Development/Languages
URL: https://elixir-lang.org/

Source: https://github.com/elixir-lang/elixir/archive/v%{version}.tar.gz

Requires: erlang
BuildRequires: erlang
BuildRequires: make-gnu

%description
Elixir is a dynamic, functional language designed for building scalable and
maintainable applications.

Elixir leverages the Erlang VM, known for running low-latency, distributed and
fault-tolerant systems, while also being successfully used in web development
and the embedded software domain.

%prep

%setup -q

%build

# Elixir prefers to have a UTF-8 environment. Set this if not so.
export LC_ALL=EN_US

%make_build PREFIX=%{_prefix}

%install

%make_install PREFIX=%{_prefix}

%files
%defattr(-, qsys, *none)
%doc NOTICE SECURITY.md LICENSE README.md
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_libdir}/elixir/*
%{_mandir}/man1/elixir.1
%{_mandir}/man1/elixirc.1
%{_mandir}/man1/iex.1
%{_mandir}/man1/mix.1

%changelog
* Wed Feb 5 2020 Calvin Buckley <calvin@cmpct.info> 1.10.0-1qsecofr
- Init
