Name: mono
Version: 6.7.0.235
Release: 1
License: MIT X11, Mozilla.MPL, Ms-PL, Info-ZIP, GPLv2, Creative Commons 2.5, Creative Commons 4.0 Public License with included packages using 3-clause BSD
Summary: Cross-platform, Open Source, .NET development framework 
Url: https://www.mono-project.com/

%define mono_corlib_version 69f9feb5-e6ef-4d90-8722-17346c85efb6
Source0: https://download.mono-project.com/sources/mono/nightly/mono-%{version}.tar.xz
# XXX: Why are we downloadng monolite seperate if we're using a tarball?
Source1: http://download.mono-project.com/monolite/monolite-unix-%{mono_corlib_version}-latest.tar.gz

# Reverts MailKit regression per Richard
Patch0: revert-068e8fe0424806753d7ab72a7b9bf0e54b58408b.diff
# Reverts crashes in things like XSP
Patch1: reworked-pr14153.diff

# XXX: Incomplete list
BuildRequires: libtool
BuildRequires: grep-gnu
BuildRequires: m4-gnu
BuildRequires: patch-gnu
BuildRequires: coreutils-gnu
BuildRequires: diffutils
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: pkg-config
# btls requires cmake
# We should get OpenSSL working instead:
# https://github.com/mono/mono/issues/8888
BuildRequires: cmake
BuildRequires: gettext-tools
BuildRequires: gettext-runtime
BuildRequires: libstdcplusplus-devel
BuildRequires: zlib-devel
BuildRequires: libiconv-devel
BuildRequires: xz
BuildRequires: python2
BuildRequires: curl
BuildRequires: wget
BuildRequires: bash
# Not hooked up to build just yet; future PR will enable this to be used
BuildRequires: libutil-devel
#Recommends:     libgdiplus0


%description
Sponsored by Microsoft, Mono is an open source implementation of Microsoft's 
.NET Framework based on the ECMA standards for C# and the Common Language 
Runtime. A growing family of solutions and an active and enthusiastic 
contributing community is helping position Mono to become the leading choice for 
development of cross platform applications. 

%prep

%setup -q
%patch0 -p1
%patch1 -p1

echo cleaning up monolite dirs
rm -rf mcs/class/lib/monolite-unix/%{mono_corlib_version}/*
echo Setting up latest monolite class libraries
mkdir -p mcs/class/lib/monolite-unix/%{mono_corlib_version}
tar -C mcs/class/lib/monolite-unix/%{mono_corlib_version} --strip-components 1 -xzf %{SOURCE1}


%build
# hackity hack hack, so "/usr/bin/env python"
mkdir -p ./tmp_python
ln -s /QOpenSys/pkgs/bin/python2 ./tmp_python/python
PATH=$PWD/tmp_python:$PATH
export PATH

# CONFIG_SHELL is to work around a libtool performance issue on AIX.
# Force OBJECT_MODE=64. It's set for i RPM builds anyways; but may be useful
# for a possible AIX build from the same specfile.
# XXX: static_mono=yes seems to build a dynamic Mono with aix sonames always,
# but it's a bit sketchy if it does or not with svr4 sonames. Play it safe.
OBJECT_MODE=64 CONFIG_SHELL=/QOpenSys/pkgs/bin/bash autogen.sh \
  LDFLAGS=-Wl,-blibpath:/QOpenSys/pkgs/lib:/QOpenSys/usr/lib,-bnoquiet \
  --prefix=/QOpenSys/pkgs \
  --with-aix-soname=svr4 --enable-shared \
  --with-static_mono=no --disable-static \
  --enable-minimal=shared_perfcounters

%make_build

%install

%make_install V=1

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%package -n mono-core
Summary: The Mono CIL runtime, suitable for running .NET code
# Use this if runtime is dynamically linked
#Requires: libmono-2_0-1
Requires: libmonosgen-2_0-1
# Dependencies of helper libs
Requires: libz1, libiconv2, libstdcplusplus6, libintl9

%description -n mono-core
This package contains the core of the Mono runtime including its
Virtual Machine, Just-in-time compiler, C# compiler, security
tools and libraries (corlib, XML, System.Security, ZipLib,
I18N, Cairo and Mono.*).

%files -n mono-core
%defattr(-, qsys, *none)
%dir %{_prefix}/etc/mono
%dir %{_prefix}/etc/mono/2.0
%dir %{_prefix}/etc/mono/4.0
%{_prefix}/etc/mono/config
%{_prefix}/etc/mono/2.0/machine.config
%{_prefix}/etc/mono/2.0/settings.map
%{_prefix}/etc/mono/4.0/machine.config
%{_prefix}/etc/mono/4.0/settings.map
%{_prefix}/etc/mono/4.5/machine.config
%{_prefix}/etc/mono/4.5/settings.map

%dir %{_libdir}/mono
%dir %{_libdir}/mono/4.5
%dir %{_libdir}/mono/4.5/Facades
%dir %{_libdir}/mono/gac

%{_bindir}/al
%{_bindir}/al2
%{_bindir}/aprofutil
%{_bindir}/cert-sync
%{_bindir}/certmgr
%{_bindir}/chktrust
%{_bindir}/crlupdate
%{_bindir}/csharp

%{_bindir}/dmcs
%{_bindir}/gacutil
%{_bindir}/gacutil2
%{_bindir}/ikdasm
%{_bindir}/mcs
%{_bindir}/mono
%{_bindir}/mono-configuration-crypto
%{_bindir}/mono-hang-watchdog
%{_bindir}/mono-sgen
%{_bindir}/mono-test-install
%{_bindir}/mozroots
%{_bindir}/peverify
%{_bindir}/setreg
%{_bindir}/sn

# These are .a libraries without svr4 sonames
%{_libdir}/libMonoPosixHelper.so
%{_libdir}/libikvm-native.so
%{_libdir}/libMonoSupportW.so
# Include both files even though this isn't a dev package.
# Mono prefers loading `.so` by default.
%{_libdir}/libmono-native.so*

%{_mandir}/man1/aprofutil.1
%{_mandir}/man1/cert-sync.1
%{_mandir}/man1/certmgr.1
%{_mandir}/man1/chktrust.1
%{_mandir}/man1/crlupdate.1
%{_mandir}/man1/csharp.1
%{_mandir}/man1/gacutil.1
%{_mandir}/man1/mcs.1
%{_mandir}/man1/mono-configuration-crypto.1
%{_mandir}/man1/mono.1
%{_mandir}/man1/mozroots.1
%{_mandir}/man1/setreg.1
%{_mandir}/man1/sn.1
%{_mandir}/man5/mono-config.5
%{_datadir}/locale/de/LC_MESSAGES/mcs.mo
%{_datadir}/locale/es/LC_MESSAGES/mcs.mo
%{_datadir}/locale/ja/LC_MESSAGES/mcs.mo
%{_datadir}/locale/pt_BR/LC_MESSAGES/mcs.mo

%{_libdir}/mono/4.5/System.IO.Compression.FileSystem.dll
%{_libdir}/mono/4.5/System.IO.Compression.dll
%{_libdir}/mono/4.5/al.exe*
%{_libdir}/mono/4.5/aprofutil.exe*
%{_libdir}/mono/4.5/cert-sync.exe*
%{_libdir}/mono/4.5/certmgr.exe*
%{_libdir}/mono/4.5/chktrust.exe*
%{_libdir}/mono/4.5/crlupdate.exe*
%{_libdir}/mono/4.5/culevel.exe*
%{_libdir}/mono/4.5/csharp.exe*
%{_libdir}/mono/4.5/gacutil.exe*
%{_libdir}/mono/4.5/ikdasm.exe*
%{_libdir}/mono/4.5/mcs.exe*
%{_libdir}/mono/4.5/mozroots.exe*
%{_libdir}/mono/4.5/setreg.exe*
%{_libdir}/mono/4.5/sn.exe*
%{_libdir}/mono/4.5/Commons.Xml.Relaxng.dll
%{_libdir}/mono/4.5/CustomMarshalers.dll
%{_libdir}/mono/4.5/I18N.West.dll
%{_libdir}/mono/4.5/I18N.dll

%{_libdir}/mono/4.5/I18N.CJK.dll
%{_libdir}/mono/4.5/I18N.MidEast.dll
%{_libdir}/mono/4.5/I18N.Other.dll
%{_libdir}/mono/4.5/I18N.Rare.dll

%{_libdir}/mono/4.5/ICSharpCode.SharpZipLib.dll
%{_libdir}/mono/4.5/Microsoft.CSharp.dll
%{_libdir}/mono/4.5/Microsoft.VisualC.dll
%{_libdir}/mono/4.5/Mono.CSharp.dll
%{_libdir}/mono/4.5/Mono.Cairo.dll
%{_libdir}/mono/4.5/Mono.CompilerServices.SymbolWriter.dll
%{_libdir}/mono/4.5/Mono.Management.dll
%{_libdir}/mono/4.5/Mono.Parallel.dll
%{_libdir}/mono/4.5/Mono.Posix.dll
%{_libdir}/mono/4.5/Mono.Profiler.Log.dll
%{_libdir}/mono/4.5/Mono.Security.dll

%{_libdir}/mono/4.5/Mono.Security.Win32.dll

%{_libdir}/mono/4.5/Mono.Simd.dll
%{_libdir}/mono/4.5/Mono.Tasklets.dll
%{_libdir}/mono/4.5/System.Configuration.dll
%{_libdir}/mono/4.5/System.Core.dll
%{_libdir}/mono/4.5/System.Drawing.dll
%{_libdir}/mono/4.5/System.Deployment.dll
%{_libdir}/mono/4.5/System.Dynamic.dll
%{_libdir}/mono/4.5/System.Json.dll
%{_libdir}/mono/4.5/System.Json.Microsoft.dll
%{_libdir}/mono/4.5/System.Memory.dll
%{_libdir}/mono/4.5/System.Net.dll
%{_libdir}/mono/4.5/System.Net.Http.dll
%{_libdir}/mono/4.5/System.Net.Http.Formatting.dll
%{_libdir}/mono/4.5/System.Net.Http.WebRequest.dll
%{_libdir}/mono/4.5/System.Numerics.dll
%{_libdir}/mono/4.5/System.Numerics.Vectors.dll
%{_libdir}/mono/4.5/System.Reflection.Context.dll
%{_libdir}/mono/4.5/System.Runtime.CompilerServices.Unsafe.dll
%{_libdir}/mono/4.5/System.Security.dll
%{_libdir}/mono/4.5/System.Threading.Tasks.Dataflow.dll
%{_libdir}/mono/4.5/System.Threading.Tasks.Extensions.dll
%{_libdir}/mono/4.5/System.Web.Mobile.dll
%{_libdir}/mono/4.5/System.Web.RegularExpressions.dll
%{_libdir}/mono/4.5/System.Workflow.Activities.dll
%{_libdir}/mono/4.5/System.Workflow.ComponentModel.dll
%{_libdir}/mono/4.5/System.Workflow.Runtime.dll
%{_libdir}/mono/4.5/System.Windows.dll
%{_libdir}/mono/4.5/System.Xml.Serialization.dll
%{_libdir}/mono/4.5/System.Xml.Linq.dll
%{_libdir}/mono/4.5/System.Xml.dll
%{_libdir}/mono/4.5/System.dll
%{_libdir}/mono/4.5/cscompmgd.dll
%{_libdir}/mono/4.5/mscorlib.dll*
%{_libdir}/mono/4.5/Facades/System*
%{_libdir}/mono/4.5/Facades/Microsoft*
%{_libdir}/mono/4.5/Facades/netstandard*
%{_libdir}/mono/gac/Commons.Xml.Relaxng/
%{_libdir}/mono/gac/CustomMarshalers/


# .NET 4.7 support

%{_libdir}/mono/4.7.2-api/Accessibility.dll
%{_libdir}/mono/4.7.2-api/Commons.Xml.Relaxng.dll
%{_libdir}/mono/4.7.2-api/CustomMarshalers.dll
%{_libdir}/mono/4.7.2-api/Facades/Microsoft.Win32.Primitives.dll
%{_libdir}/mono/4.7.2-api/Facades/System.AppContext.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Collections.Concurrent.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Collections.NonGeneric.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Collections.Specialized.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Collections.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ComponentModel.Annotations.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ComponentModel.EventBasedAsync.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ComponentModel.Primitives.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ComponentModel.TypeConverter.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ComponentModel.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Console.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Data.Common.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Diagnostics.Contracts.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Diagnostics.Debug.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Diagnostics.FileVersionInfo.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Diagnostics.Process.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Diagnostics.StackTrace.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Diagnostics.TextWriterTraceListener.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Diagnostics.Tools.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Diagnostics.TraceSource.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Drawing.Primitives.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Dynamic.Runtime.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Globalization.Calendars.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Globalization.Extensions.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Globalization.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.Compression.ZipFile.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.FileSystem.DriveInfo.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.FileSystem.Primitives.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.FileSystem.Watcher.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.FileSystem.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.IsolatedStorage.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.MemoryMappedFiles.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.Pipes.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.UnmanagedMemoryStream.dll
%{_libdir}/mono/4.7.2-api/Facades/System.IO.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Linq.Expressions.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Linq.Parallel.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Linq.Queryable.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Linq.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.Http.Rtc.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.NameResolution.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.NetworkInformation.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.Ping.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.Primitives.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.Requests.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.Security.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.Sockets.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.WebHeaderCollection.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.WebSockets.Client.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Net.WebSockets.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ObjectModel.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Reflection.Emit.ILGeneration.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Reflection.Emit.Lightweight.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Reflection.Emit.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Reflection.Extensions.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Reflection.Primitives.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Reflection.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Resources.Reader.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Resources.ResourceManager.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Resources.Writer.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.CompilerServices.VisualC.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.Extensions.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.Handles.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.InteropServices.RuntimeInformation.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.InteropServices.WindowsRuntime.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.InteropServices.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.Numerics.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.Serialization.Formatters.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.Serialization.Json.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.Serialization.Primitives.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.Serialization.Xml.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Runtime.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Security.Claims.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Security.Cryptography.Algorithms.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Security.Cryptography.Csp.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Security.Cryptography.Encoding.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Security.Cryptography.Primitives.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Security.Cryptography.X509Certificates.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Security.Principal.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Security.SecureString.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ServiceModel.Duplex.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ServiceModel.Http.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ServiceModel.NetTcp.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ServiceModel.Primitives.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ServiceModel.Security.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Text.Encoding.Extensions.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Text.Encoding.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Text.RegularExpressions.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Threading.Overlapped.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Threading.Tasks.Parallel.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Threading.Tasks.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Threading.Thread.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Threading.ThreadPool.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Threading.Timer.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Threading.dll
%{_libdir}/mono/4.7.2-api/Facades/System.ValueTuple.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Xml.ReaderWriter.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Xml.XDocument.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Xml.XPath.XDocument.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Xml.XPath.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Xml.XmlDocument.dll
%{_libdir}/mono/4.7.2-api/Facades/System.Xml.XmlSerializer.dll
%{_libdir}/mono/4.7.2-api/Facades/netstandard.dll
%{_libdir}/mono/4.7.2-api/I18N.CJK.dll
%{_libdir}/mono/4.7.2-api/I18N.MidEast.dll
%{_libdir}/mono/4.7.2-api/I18N.Other.dll
%{_libdir}/mono/4.7.2-api/I18N.Rare.dll
%{_libdir}/mono/4.7.2-api/I18N.West.dll
%{_libdir}/mono/4.7.2-api/I18N.dll
%{_libdir}/mono/4.7.2-api/IBM.Data.DB2.dll
%{_libdir}/mono/4.7.2-api/Microsoft.Build.Engine.dll
%{_libdir}/mono/4.7.2-api/Microsoft.Build.Framework.dll
%{_libdir}/mono/4.7.2-api/Microsoft.Build.Tasks.v4.0.dll
%{_libdir}/mono/4.7.2-api/Microsoft.Build.Utilities.v4.0.dll
%{_libdir}/mono/4.7.2-api/Microsoft.Build.dll
%{_libdir}/mono/4.7.2-api/Microsoft.CSharp.dll
%{_libdir}/mono/4.7.2-api/Microsoft.VisualBasic.dll
%{_libdir}/mono/4.7.2-api/Microsoft.VisualC.dll
%{_libdir}/mono/4.7.2-api/Microsoft.Web.Infrastructure.dll
%{_libdir}/mono/4.7.2-api/Mono.C5.dll
%{_libdir}/mono/4.7.2-api/Mono.CSharp.dll
%{_libdir}/mono/4.7.2-api/Mono.Cairo.dll
%{_libdir}/mono/4.7.2-api/Mono.CodeContracts.dll
%{_libdir}/mono/4.7.2-api/Mono.CompilerServices.SymbolWriter.dll
%{_libdir}/mono/4.7.2-api/Mono.Data.Sqlite.dll
%{_libdir}/mono/4.7.2-api/Mono.Data.Tds.dll
%{_libdir}/mono/4.7.2-api/Mono.Debugger.Soft.dll
%{_libdir}/mono/4.7.2-api/Mono.Http.dll
%{_libdir}/mono/4.7.2-api/Mono.Management.dll
%{_libdir}/mono/4.7.2-api/Mono.Messaging.RabbitMQ.dll
%{_libdir}/mono/4.7.2-api/Mono.Messaging.dll
%{_libdir}/mono/4.7.2-api/Mono.Options.dll
%{_libdir}/mono/4.7.2-api/Mono.Parallel.dll
%{_libdir}/mono/4.7.2-api/Mono.Posix.dll
%{_libdir}/mono/4.7.2-api/Mono.Security.Win32.dll
%{_libdir}/mono/4.7.2-api/Mono.Security.dll
%{_libdir}/mono/4.7.2-api/Mono.Simd.dll
%{_libdir}/mono/4.7.2-api/Mono.Tasklets.dll
%{_libdir}/mono/4.7.2-api/Mono.WebBrowser.dll
%{_libdir}/mono/4.7.2-api/Novell.Directory.Ldap.dll
%{_libdir}/mono/4.7.2-api/PEAPI.dll
%{_libdir}/mono/4.7.2-api/RabbitMQ.Client.dll
%{_libdir}/mono/4.7.2-api/SMDiagnostics.dll
%{_libdir}/mono/4.7.2-api/System.ComponentModel.Composition.dll
%{_libdir}/mono/4.7.2-api/System.ComponentModel.DataAnnotations.dll
%{_libdir}/mono/4.7.2-api/System.Configuration.Install.dll
%{_libdir}/mono/4.7.2-api/System.Configuration.dll
%{_libdir}/mono/4.7.2-api/System.Core.dll
%{_libdir}/mono/4.7.2-api/System.Data.DataSetExtensions.dll
%{_libdir}/mono/4.7.2-api/System.Data.Entity.dll
%{_libdir}/mono/4.7.2-api/System.Data.Linq.dll
%{_libdir}/mono/4.7.2-api/System.Data.OracleClient.dll
%{_libdir}/mono/4.7.2-api/System.Data.Services.Client.dll
%{_libdir}/mono/4.7.2-api/System.Data.Services.dll
%{_libdir}/mono/4.7.2-api/System.Data.dll
%{_libdir}/mono/4.7.2-api/System.Deployment.dll
%{_libdir}/mono/4.7.2-api/System.Design.dll
%{_libdir}/mono/4.7.2-api/System.Diagnostics.Tracing.dll
%{_libdir}/mono/4.7.2-api/System.DirectoryServices.Protocols.dll
%{_libdir}/mono/4.7.2-api/System.DirectoryServices.dll
%{_libdir}/mono/4.7.2-api/System.Drawing.Design.dll
%{_libdir}/mono/4.7.2-api/System.Drawing.dll
%{_libdir}/mono/4.7.2-api/System.Dynamic.dll
%{_libdir}/mono/4.7.2-api/System.EnterpriseServices.dll
%{_libdir}/mono/4.7.2-api/System.IO.Compression.FileSystem.dll
%{_libdir}/mono/4.7.2-api/System.IO.Compression.dll
%{_libdir}/mono/4.7.2-api/System.IdentityModel.Selectors.dll
%{_libdir}/mono/4.7.2-api/System.IdentityModel.dll
%{_libdir}/mono/4.7.2-api/System.Json.Microsoft.dll
%{_libdir}/mono/4.7.2-api/System.Json.dll
%{_libdir}/mono/4.7.2-api/System.Management.dll
%{_libdir}/mono/4.7.2-api/System.Messaging.dll
%{_libdir}/mono/4.7.2-api/System.Net.Http.Formatting.dll
%{_libdir}/mono/4.7.2-api/System.Net.Http.WebRequest.dll
%{_libdir}/mono/4.7.2-api/System.Net.Http.dll
%{_libdir}/mono/4.7.2-api/System.Net.dll
%{_libdir}/mono/4.7.2-api/System.Numerics.Vectors.dll
%{_libdir}/mono/4.7.2-api/System.Numerics.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Core.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Debugger.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Experimental.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Interfaces.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Linq.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Observable.Aliases.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.PlatformServices.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Providers.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Runtime.Remoting.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Windows.Forms.dll
%{_libdir}/mono/4.7.2-api/System.Reactive.Windows.Threading.dll
%{_libdir}/mono/4.7.2-api/System.Reflection.Context.dll
%{_libdir}/mono/4.7.2-api/System.Runtime.Caching.dll
%{_libdir}/mono/4.7.2-api/System.Runtime.DurableInstancing.dll
%{_libdir}/mono/4.7.2-api/System.Runtime.Remoting.dll
%{_libdir}/mono/4.7.2-api/System.Runtime.Serialization.Formatters.Soap.dll
%{_libdir}/mono/4.7.2-api/System.Runtime.Serialization.dll
%{_libdir}/mono/4.7.2-api/System.Security.dll
%{_libdir}/mono/4.7.2-api/System.ServiceModel.Activation.dll
%{_libdir}/mono/4.7.2-api/System.ServiceModel.Discovery.dll
%{_libdir}/mono/4.7.2-api/System.ServiceModel.Routing.dll
%{_libdir}/mono/4.7.2-api/System.ServiceModel.Web.dll
%{_libdir}/mono/4.7.2-api/System.ServiceModel.dll
%{_libdir}/mono/4.7.2-api/System.ServiceProcess.dll
%{_libdir}/mono/4.7.2-api/System.Threading.Tasks.Dataflow.dll
%{_libdir}/mono/4.7.2-api/System.Transactions.dll
%{_libdir}/mono/4.7.2-api/System.Web.Abstractions.dll
%{_libdir}/mono/4.7.2-api/System.Web.ApplicationServices.dll
%{_libdir}/mono/4.7.2-api/System.Web.DynamicData.dll
%{_libdir}/mono/4.7.2-api/System.Web.Extensions.Design.dll
%{_libdir}/mono/4.7.2-api/System.Web.Extensions.dll
%{_libdir}/mono/4.7.2-api/System.Web.Http.SelfHost.dll
%{_libdir}/mono/4.7.2-api/System.Web.Http.WebHost.dll
%{_libdir}/mono/4.7.2-api/System.Web.Http.dll
%{_libdir}/mono/4.7.2-api/System.Web.Mobile.dll
%{_libdir}/mono/4.7.2-api/System.Web.Mvc.dll
%{_libdir}/mono/4.7.2-api/System.Web.Razor.dll
%{_libdir}/mono/4.7.2-api/System.Web.RegularExpressions.dll
%{_libdir}/mono/4.7.2-api/System.Web.Routing.dll
%{_libdir}/mono/4.7.2-api/System.Web.Services.dll
%{_libdir}/mono/4.7.2-api/System.Web.WebPages.Deployment.dll
%{_libdir}/mono/4.7.2-api/System.Web.WebPages.Razor.dll
%{_libdir}/mono/4.7.2-api/System.Web.WebPages.dll
%{_libdir}/mono/4.7.2-api/System.Web.dll
%{_libdir}/mono/4.7.2-api/System.Windows.Forms.DataVisualization.dll
%{_libdir}/mono/4.7.2-api/System.Windows.Forms.dll
%{_libdir}/mono/4.7.2-api/System.Windows.dll
%{_libdir}/mono/4.7.2-api/System.Workflow.Activities.dll
%{_libdir}/mono/4.7.2-api/System.Workflow.ComponentModel.dll
%{_libdir}/mono/4.7.2-api/System.Workflow.Runtime.dll
%{_libdir}/mono/4.7.2-api/System.Xaml.dll
%{_libdir}/mono/4.7.2-api/System.Xml.Linq.dll
%{_libdir}/mono/4.7.2-api/System.Xml.Serialization.dll
%{_libdir}/mono/4.7.2-api/System.Xml.dll
%{_libdir}/mono/4.7.2-api/System.dll
%{_libdir}/mono/4.7.2-api/WebMatrix.Data.dll
%{_libdir}/mono/4.7.2-api/WindowsBase.dll
%{_libdir}/mono/4.7.2-api/cscompmgd.dll
%{_libdir}/mono/4.7.2-api/mscorlib.dll



# Should we include all of the I18N's?
%{_libdir}/mono/gac/I18N/
%{_libdir}/mono/gac/I18N.*/
%{_libdir}/mono/gac/ICSharpCode.SharpZipLib/
%{_libdir}/mono/gac/Microsoft.CSharp/
%{_libdir}/mono/gac/Microsoft.VisualC/
%{_libdir}/mono/gac/Mono.CSharp/
%{_libdir}/mono/gac/Mono.Cairo/
%{_libdir}/mono/gac/Mono.Cecil/
%{_libdir}/mono/gac/Mono.CompilerServices.SymbolWriter/
%{_libdir}/mono/gac/Mono.Management/
%{_libdir}/mono/gac/Mono.Parallel/
%{_libdir}/mono/gac/Mono.Posix/
%{_libdir}/mono/gac/Mono.Profiler.Log/
%{_libdir}/mono/gac/Mono.Security/

# Should rm this? Seems Windows specific
%{_libdir}/mono/gac/Mono.Security.Win32/

%{_libdir}/mono/gac/Mono.Simd/
%{_libdir}/mono/gac/Mono.Tasklets/
%{_libdir}/mono/gac/System
%{_libdir}/mono/gac/System.Configuration/
%{_libdir}/mono/gac/System.Core/
%{_libdir}/mono/gac/System.Drawing/
%{_libdir}/mono/gac/System.Deployment/
%{_libdir}/mono/gac/System.Dynamic/
%{_libdir}/mono/gac/System.Net/
%{_libdir}/mono/gac/System.Net.Http/
%{_libdir}/mono/gac/System.Net.Http.Formatting/
%{_libdir}/mono/gac/System.Net.Http.WebRequest/
%{_libdir}/mono/gac/System.Numerics/
%{_libdir}/mono/gac/System.Numerics.Vectors/
%{_libdir}/mono/gac/System.Reflection.Context/
%{_libdir}/mono/gac/System.Security/
%{_libdir}/mono/gac/System.Threading.Tasks.Dataflow/
%{_libdir}/mono/gac/System.Web.Mobile/
%{_libdir}/mono/gac/System.Web.RegularExpressions/
%{_libdir}/mono/gac/System.Workflow.Activities/
%{_libdir}/mono/gac/System.Workflow.ComponentModel/
%{_libdir}/mono/gac/System.Workflow.Runtime/
%{_libdir}/mono/gac/System.Windows/
%{_libdir}/mono/gac/System.Xml.Serialization/
%{_libdir}/mono/gac/System.Xml/
%{_libdir}/mono/gac/System.Xml.Linq/
%{_libdir}/mono/gac/System.Json/
%{_libdir}/mono/gac/System.Json.Microsoft/
%{_libdir}/mono/gac/System.IO.Compression.FileSystem/
%{_libdir}/mono/gac/System.IO.Compression/
%{_libdir}/mono/gac/cscompmgd/
%{_libdir}/mono/mono-configuration-crypto/

#if btls
%{_libdir}/mono/4.5/Mono.Btls.Interface.dll
%{_libdir}/mono/gac/Mono.Btls.Interface/
%{_libdir}/libmono-btls-shared.so


#if roslyn
%{_bindir}/csc
%{_prefix}/lib/mono/4.5/csc.*
%{_bindir}/csi
%{_bindir}/vbc
%{_prefix}/lib/mono/4.5/csi.*
%{_prefix}/lib/mono/4.5/vbc.*
%{_libdir}/mono/4.5/System.Collections.Immutable.dll
%{_libdir}/mono/4.5/Microsoft.CodeAnalysis.dll
%{_libdir}/mono/4.5/Microsoft.CodeAnalysis.CSharp.dll
%{_libdir}/mono/4.5/Microsoft.CodeAnalysis.CSharp.Scripting.dll
%{_libdir}/mono/4.5/Microsoft.CodeAnalysis.Scripting.dll
%{_libdir}/mono/4.5/Microsoft.CodeAnalysis.VisualBasic.dll
%{_libdir}/mono/4.5/System.Reflection.Metadata.dll
%{_libdir}/mono/4.5/VBCSCompiler.*

# TODO: Merge libmono and libmonosgen because it's stubby
# libmono is a symlink to libmonosgen provided for compat
%package -n libmono-2_0-1
Summary: A Library for embedding Mono in your Application
License: MIT X11
Requires: libmonosgen-2_0-1
Requires: mono-core = %{version}

%description -n libmono-2_0-1
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

A Library for embedding Mono in your Application.

%files -n libmono-2_0-1
%defattr(-, qsys, *none)
%{_libdir}/libmono-2.0.so.1

%package -n libmono-2_0-devel
Summary: Development files for libmono
License: MIT X11
Requires: libmono-2_0-1 = %{version}
Requires: libmonosgen-2_0-devel
Requires: mono-core = %{version}

%description -n libmono-2_0-devel
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Development files for libmono.

%files -n libmono-2_0-devel
%defattr(-, qsys, *none)
%{_bindir}/mono-gdb.py
%{_includedir}/mono-2.0/
%{_libdir}/libmono-2.0.so
%{_libdir}/pkgconfig/mono-2.pc

%package -n libmonosgen-2_0-1
Summary: A Library for embedding Mono in your Application (SGen GC)
License: MIT X11

%description -n libmonosgen-2_0-1
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

A Library for embedding Mono in your application using the precise SGen
garbage collector.

%files -n libmonosgen-2_0-1
%defattr(-, qsys, *none)
%{_libdir}/libmonosgen-2.0.so.1

%package -n libmonosgen-2_0-devel
Summary: Development files for libmonosgen
License: MIT X11
Requires: libmono-2_0-devel
Requires: libmonosgen-2_0-1 = %{version}
Requires: mono-core = %{version}

%description -n libmonosgen-2_0-devel
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Development files for libmonosgen.

%files -n libmonosgen-2_0-devel
%defattr(-, qsys, *none)
%{_bindir}/mono-sgen-gdb.py
%{_libdir}/libmonosgen-2.0.so
%{_libdir}/pkgconfig/monosgen-2.pc

%package -n mono-data
Summary: Database connectivity for Mono
License: MIT X11
Requires: mono-core = %{version}
# Include the tools instead of just libodbc2
Requires: unixODBC

%description -n mono-data
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.

%files -n mono-data
%defattr(-, qsys, *none)
%{_bindir}/sqlmetal
%{_bindir}/sqlsharp
%{_mandir}/man1/sqlsharp.1
%{_libdir}/mono/4.5/Mono.Data.Tds.dll
%{_libdir}/mono/4.5/Novell.Directory.Ldap.dll
%{_libdir}/mono/4.5/System.Data.DataSetExtensions.dll
%{_libdir}/mono/4.5/System.Data.Linq.dll
%{_libdir}/mono/4.5/System.Data.dll
%{_libdir}/mono/4.5/System.Data.Entity.dll
%{_libdir}/mono/4.5/System.DirectoryServices.dll
%{_libdir}/mono/4.5/System.DirectoryServices.Protocols.dll
%{_libdir}/mono/4.5/System.EnterpriseServices.dll
%{_libdir}/mono/4.5/System.Runtime.Serialization.dll
%{_libdir}/mono/4.5/System.Transactions.dll
%{_libdir}/mono/4.5/WebMatrix.Data.dll
%{_libdir}/mono/4.5/sqlmetal.exe*
%{_libdir}/mono/4.5/sqlsharp.exe*
%{_libdir}/mono/gac/Mono.Data.Tds/
%{_libdir}/mono/gac/Novell.Directory.Ldap/
%{_libdir}/mono/gac/System.Data/
%{_libdir}/mono/gac/System.Data.Entity/
%{_libdir}/mono/gac/System.Data.DataSetExtensions/
%{_libdir}/mono/gac/System.Data.Linq/
%{_libdir}/mono/gac/System.DirectoryServices/
%{_libdir}/mono/gac/System.DirectoryServices.Protocols/
%{_libdir}/mono/gac/System.EnterpriseServices/
%{_libdir}/mono/gac/System.Runtime.Serialization/
%{_libdir}/mono/gac/System.Transactions/
%{_libdir}/mono/gac/WebMatrix.Data/

%package -n mono-data-db2
Summary: Database connectivity for DB2
License: MIT X11
Requires: mono-core = %{version}
Requires: mono-data = %{version}

%description -n mono-data-db2
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for DB2 Linux/Unix/Windows.

%files -n mono-data-db2
%defattr(-, qsys, *none)
%{_libdir}/mono/4.5/IBM.Data.DB2.dll
%{_libdir}/mono/gac/IBM.Data.DB2/

%package -n mono-data-sqlite
Summary: Database connectivity for Mono
License: MIT X11
Requires: mono-core = %{version}
Requires: mono-data = %{version}
Requires: libsqlite3-0

%description -n mono-data-sqlite
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Sqlite.

%files -n mono-data-sqlite
%defattr(-, qsys, *none)
%{_libdir}/mono/4.5/Mono.Data.Sqlite.dll
%{_libdir}/mono/gac/Mono.Data.Sqlite/

%package -n mono-data-oracle
Summary:  Database connectivity for Mono
License:  LGPL-2.1
Requires: mono-core = %{version}
Requires: mono-data = %{version}


%description -n mono-data-oracle
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Oracle.

%files -n mono-data-oracle
%defattr(-, qsys, *none)
%{_libdir}/mono/4.5/System.Data.OracleClient.dll
%{_libdir}/mono/gac/System.Data.OracleClient/


%package -n mono-winforms
Summary: Mono's Windows Forms implementation
License: MIT X11
Requires: mono-core = %{version}
#Requires: libgdiplus0
Requires: libX11
Requires: libXcursor
Requires: libXinerama

%description -n mono-winforms
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono's Windows Forms implementation.

%files -n mono-winforms
%defattr(-, qsys, *none)
%{_libdir}/mono/4.5/Accessibility.dll
%{_libdir}/mono/4.5/Mono.WebBrowser.dll
%{_libdir}/mono/4.5/System.Design.dll
%{_libdir}/mono/4.5/System.Drawing.Design.dll
%{_libdir}/mono/4.5/System.Windows.Forms.DataVisualization.dll
%{_libdir}/mono/4.5/System.Windows.Forms.dll
%{_libdir}/mono/gac/Accessibility/
%{_libdir}/mono/gac/Mono.WebBrowser/
%{_libdir}/mono/gac/System.Design/
%{_libdir}/mono/gac/System.Drawing.Design/
%{_libdir}/mono/gac/System.Windows.Forms/
%{_libdir}/mono/gac/System.Windows.Forms.DataVisualization/

%package -n mono-extras
Summary: Extra packages
License: MIT X11
Requires: mono-core = %{version}

%description -n mono-extras
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Extra packages.

%files -n mono-extras
%defattr(-, qsys, *none)
%{_bindir}/mono-service
%{_bindir}/mono-service2
%{_mandir}/man1/mono-service.1
%{_libdir}/mono/4.5/installutil.exe*
%{_libdir}/mono/4.5/mono-service.exe*
%{_libdir}/mono/4.5/Mono.Messaging.RabbitMQ.dll
%{_libdir}/mono/4.5/Mono.Messaging.dll
%{_libdir}/mono/4.5/RabbitMQ.Client.Apigen.exe*
%{_libdir}/mono/4.5/RabbitMQ.Client.dll
%{_libdir}/mono/4.5/System.Configuration.Install.dll
%{_libdir}/mono/4.5/System.Management.dll
%{_libdir}/mono/4.5/System.Messaging.dll
%{_libdir}/mono/4.5/System.Runtime.Caching.dll
%{_libdir}/mono/4.5/System.ServiceProcess.dll
%{_libdir}/mono/4.5/System.Xaml.dll
%{_libdir}/mono/gac/Mono.Messaging/
%{_libdir}/mono/gac/Mono.Messaging.RabbitMQ/
%{_libdir}/mono/gac/RabbitMQ.Client/
%{_libdir}/mono/gac/System.Configuration.Install/
%{_libdir}/mono/gac/System.Management/
%{_libdir}/mono/gac/System.Messaging/
%{_libdir}/mono/gac/System.Runtime.Caching/
%{_libdir}/mono/gac/System.ServiceProcess/
%{_libdir}/mono/gac/System.Xaml/
%{_libdir}/mono/gac/mono-service/

%package -n mono-wcf
Summary: Mono implementation of WCF, Windows Communication Foundation
License: MIT and MS-PL
Requires: mono-core = %{version}

%description -n mono-wcf
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of WCF, Windows Communication Foundation

%files -n mono-wcf
%defattr(-, qsys, *none)
%{_bindir}/svcutil
%{_libdir}/pkgconfig/wcf.pc
%{_libdir}/mono/4.5/System.Data.Services.dll
%{_libdir}/mono/4.5/System.IdentityModel.Selectors.dll
%{_libdir}/mono/4.5/System.IdentityModel.dll
%{_libdir}/mono/4.5/System.Runtime.DurableInstancing.dll
%{_libdir}/mono/4.5/System.ServiceModel.Activation.dll
%{_libdir}/mono/4.5/System.ServiceModel.Discovery.dll
%{_libdir}/mono/4.5/System.ServiceModel.Internals.dll
%{_libdir}/mono/4.5/System.ServiceModel.Routing.dll
%{_libdir}/mono/4.5/System.ServiceModel.Web.dll
%{_libdir}/mono/4.5/System.ServiceModel.dll
%{_libdir}/mono/4.5/SMDiagnostics.dll
%{_libdir}/mono/4.5/svcutil.exe*
%{_libdir}/mono/gac/System.Data.Services/
%{_libdir}/mono/gac/System.IdentityModel/
%{_libdir}/mono/gac/System.IdentityModel.Selectors/
%{_libdir}/mono/gac/System.Runtime.DurableInstancing/
%{_libdir}/mono/gac/System.ServiceModel/
%{_libdir}/mono/gac/System.ServiceModel.Activation/
%{_libdir}/mono/gac/System.ServiceModel.Discovery/
%{_libdir}/mono/gac/System.ServiceModel.Internals/
%{_libdir}/mono/gac/System.ServiceModel.Routing/
%{_libdir}/mono/gac/System.ServiceModel.Web/
%{_libdir}/mono/gac/SMDiagnostics/

%package -n mono-winfxcore
Summary: Mono implementation of core WinFX APIs
License: MIT and MS-PL
Requires: mono-core = %{version}

%description -n mono-winfxcore
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of core WinFX APIs

%files -n mono-winfxcore
%defattr(-, qsys, *none)
%{_libdir}/mono/4.5/System.Data.Services.Client.dll
%{_libdir}/mono/4.5/WindowsBase.dll
%{_libdir}/mono/gac/System.Data.Services.Client/
%{_libdir}/mono/gac/WindowsBase/

%package -n mono-web
Summary: Mono implementation of ASP
License: MIT and MS-PL
Requires: mono-core = %{version}

%description -n mono-web
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of ASP.NET, Remoting and Web Services.

%files -n mono-web
%defattr(-, qsys, *none)
%{_prefix}/etc/mono/2.0/Browsers/
%{_prefix}/etc/mono/2.0/DefaultWsdlHelpGenerator.aspx
%{_prefix}/etc/mono/2.0/web.config
%{_prefix}/etc/mono/4.0/Browsers/
%{_prefix}/etc/mono/4.0/DefaultWsdlHelpGenerator.aspx
%{_prefix}/etc/mono/4.0/web.config
%{_prefix}/etc/mono/4.5/Browsers/
%{_prefix}/etc/mono/4.5/DefaultWsdlHelpGenerator.aspx
%{_prefix}/etc/mono/4.5/web.config
%{_prefix}/etc/mono/browscap.ini
%{_prefix}/etc/mono/mconfig/
#%{_prefix}/etc/mono/mconfig/config.xml
%{_bindir}/disco
%{_bindir}/mconfig
%{_bindir}/soapsuds
%{_bindir}/wsdl
%{_bindir}/wsdl2
%{_bindir}/xsd
%{_libdir}/pkgconfig/aspnetwebstack.pc
%{_mandir}/man1/disco.1
%{_mandir}/man1/mconfig.1
%{_mandir}/man1/soapsuds.1
%{_mandir}/man1/wsdl.1
%{_mandir}/man1/xsd.1
%{_libdir}/mono/4.5/Mono.Http.dll
%{_libdir}/mono/4.5/System.ComponentModel.Composition.dll
%{_libdir}/mono/4.5/System.ComponentModel.DataAnnotations.dll
%{_libdir}/mono/4.5/System.Runtime.Remoting.dll
%{_libdir}/mono/4.5/System.Runtime.Serialization.Formatters.Soap.dll
%{_libdir}/mono/4.5/System.Web.Abstractions.dll
%{_libdir}/mono/4.5/System.Web.ApplicationServices.dll
%{_libdir}/mono/4.5/System.Web.Http.dll
%{_libdir}/mono/4.5/System.Web.Http.SelfHost.dll
%{_libdir}/mono/4.5/System.Web.Http.WebHost.dll
%{_libdir}/mono/4.5/System.Web.Routing.dll
%{_libdir}/mono/4.5/System.Web.Razor.dll
%{_libdir}/mono/4.5/System.Web.Services.dll
%{_libdir}/mono/4.5/System.Web.WebPages.Deployment.dll
%{_libdir}/mono/4.5/System.Web.WebPages.Razor.dll
%{_libdir}/mono/4.5/System.Web.WebPages.dll
%{_libdir}/mono/4.5/System.Web.dll
%{_libdir}/mono/4.5/disco.exe*
%{_libdir}/mono/4.5/mconfig.exe*
%{_libdir}/mono/4.5/soapsuds.exe*
%{_libdir}/mono/4.5/wsdl.exe*
%{_libdir}/mono/4.5/xsd.exe*
%{_libdir}/mono/4.5/Microsoft.Web.Infrastructure.dll
%{_libdir}/mono/gac/Microsoft.Web.Infrastructure/
%{_libdir}/mono/gac/Mono.Http/
%{_libdir}/mono/gac/System.ComponentModel.Composition/
%{_libdir}/mono/gac/System.ComponentModel.DataAnnotations
%{_libdir}/mono/gac/System.Runtime.Remoting
%{_libdir}/mono/gac/System.Runtime.Serialization.Formatters.Soap
%{_libdir}/mono/gac/System.Web/
%{_libdir}/mono/gac/System.Web.Abstractions/
%{_libdir}/mono/gac/System.Web.ApplicationServices/
%{_libdir}/mono/gac/System.Web.Http/
%{_libdir}/mono/gac/System.Web.Http.SelfHost/
%{_libdir}/mono/gac/System.Web.Http.WebHost/
%{_libdir}/mono/gac/System.Web.Routing/
%{_libdir}/mono/gac/System.Web.Razor/
%{_libdir}/mono/gac/System.Web.Services
%{_libdir}/mono/gac/System.Web.WebPages.Deployment/
%{_libdir}/mono/gac/System.Web.WebPages.Razor/
%{_libdir}/mono/gac/System.Web.WebPages/


%package -n mono-mvc
Summary: Mono implementation of ASP
License: MIT and MS-PL
Requires: mono-core = %{version}

%description -n mono-mvc
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of ASP.NET MVC.

%files -n mono-mvc
%defattr(-, qsys, *none)
%{_libdir}/pkgconfig/system.web.extensions.design_1.0.pc
%{_libdir}/pkgconfig/system.web.extensions_1.0.pc
%{_libdir}/pkgconfig/system.web.mvc.pc
%{_libdir}/pkgconfig/system.web.mvc2.pc
%{_libdir}/pkgconfig/system.web.mvc3.pc
%{_libdir}/mono/4.5/System.Web.DynamicData.dll
%{_libdir}/mono/4.5/System.Web.Extensions.Design.dll
%{_libdir}/mono/4.5/System.Web.Extensions.dll
%{_libdir}/mono/4.5/System.Web.Mvc.dll
%{_libdir}/mono/gac/System.Web.DynamicData/
%{_libdir}/mono/gac/System.Web.Extensions/
%{_libdir}/mono/gac/System.Web.Extensions.Design/
%{_libdir}/mono/gac/System.Web.Mvc/

%package -n mono-devel
Summary: Mono development tools
License: MIT X11
Requires: mono-core = %{version}
# Required because they are referenced by .pc files
Requires: mono-data = %{version}
Requires: mono-data-oracle = %{version}
Requires: mono-extras = %{version}
Requires: mono-web = %{version}
Requires: mono-winforms = %{version}
#Requires: pkgconfig


%description -n mono-devel
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. This package contains compilers and
other tools needed to develop .NET applications.

Mono development tools.

%files -n mono-devel
%defattr(-, qsys, *none)
%{_bindir}/caspol
%{_bindir}/ccrewrite
%{_bindir}/cccheck
%{_bindir}/cert2spc
%{_bindir}/dtd2rng
%{_bindir}/dtd2xsd
%{_bindir}/genxs
%{_bindir}/httpcfg
%{_bindir}/ilasm
%{_bindir}/illinkanalyzer
%{_bindir}/installvst
%{_bindir}/lc
%{_bindir}/macpack
%{_bindir}/makecert
%{_bindir}/mdbrebase
%{_bindir}/mkbundle
%{_bindir}/mono-api-info
%{_bindir}/mono-api-html
%{_bindir}/mono-cil-strip
%{_bindir}/mono-find-provides
%{_bindir}/mono-find-requires
%{_bindir}/mono-heapviz
%{_bindir}/mono-package-runtime
%{_bindir}/mono-shlib-cop
%{_bindir}/mono-symbolicate
%{_bindir}/mono-xmltool
%{_bindir}/monodis
%{_bindir}/monolinker
%{_bindir}/monop
%{_bindir}/monop2
%{_bindir}/mprof-report
%{_bindir}/pdb2mdb
%{_bindir}/pedump
%{_bindir}/permview
%{_bindir}/resgen
%{_bindir}/resgen2
%{_bindir}/secutil
%{_bindir}/sgen
%{_bindir}/sgen-grep-binprot
%{_bindir}/signcode
%{_bindir}/xbuild
%dir %{_datadir}/mono-2.0
%dir %{_datadir}/mono-2.0/mono
%dir %{_datadir}/mono-2.0/mono/cil
%dir %{_datadir}/mono-2.0/mono/profiler
%{_datadir}/mono-2.0/mono/cil/cil-opcodes.xml
%{_datadir}/mono-2.0/mono/profiler/mono-profiler-coverage.suppression
%{_datadir}/mono-2.0/mono/eglib/eglib-config.h
%{_libdir}/libmono-profiler-*.*
%{_libdir}/pkgconfig/cecil.pc
%{_libdir}/pkgconfig/dotnet.pc
%{_libdir}/pkgconfig/dotnet35.pc
%{_libdir}/pkgconfig/mono-cairo.pc
%{_libdir}/pkgconfig/mono-lineeditor.pc
%{_libdir}/pkgconfig/mono-options.pc
%{_libdir}/pkgconfig/mono.pc
%{_libdir}/pkgconfig/xbuild12.pc
%{_mandir}/man1/al.1
%{_mandir}/man1/ccrewrite.1
%{_mandir}/man1/cccheck.1
%{_mandir}/man1/cert2spc.1
%{_mandir}/man1/cilc.1
%{_mandir}/man1/dtd2xsd.1
%{_mandir}/man1/genxs.1
%{_mandir}/man1/httpcfg.1
%{_mandir}/man1/ilasm.1
%{_mandir}/man1/illinkanalyzer.1
%{_mandir}/man1/lc.1
%{_mandir}/man1/macpack.1
%{_mandir}/man1/mdb2ppdb.1
%{_mandir}/man1/makecert.1
%{_mandir}/man1/mkbundle.1
%{_mandir}/man1/mono-api-info.1
%{_mandir}/man1/mono-cil-strip.1
%{_mandir}/man1/mono-profilers.1
%{_mandir}/man1/mono-shlib-cop.1
%{_mandir}/man1/mono-symbolicate.1
%{_mandir}/man1/mono-xmltool.1
%{_mandir}/man1/monodis.1
%{_mandir}/man1/monolinker.1
%{_mandir}/man1/monop.1
%{_mandir}/man1/mprof-report.1
%{_mandir}/man1/pdb2mdb.1
%{_mandir}/man1/permview.1
%{_mandir}/man1/resgen.1
%{_mandir}/man1/secutil.1
%{_mandir}/man1/sgen.1
%{_mandir}/man1/signcode.1
%{_mandir}/man1/xbuild.1
%{_libdir}/mono-source-libs/
%{_libdir}/mono/4.0
%{_libdir}/mono/4.7.1-api
%{_libdir}/mono/4.7-api
%{_libdir}/mono/4.6.2-api
%{_libdir}/mono/4.6.1-api
%{_libdir}/mono/4.6-api
%{_libdir}/mono/4.5.2-api
%{_libdir}/mono/4.5.1-api
%{_libdir}/mono/4.5-api
%{_libdir}/mono/4.0-api
%{_libdir}/mono/3.5-api
%{_libdir}/mono/2.0-api
%{_libdir}/mono/4.5/Microsoft.Build.dll
%{_libdir}/mono/4.5/Microsoft.Build.Engine.dll
%{_libdir}/mono/4.5/Microsoft.Build.Framework.dll
%{_libdir}/mono/4.5/Microsoft.Build.Tasks.v4.0.dll
%{_libdir}/mono/4.5/Microsoft.Build.Utilities.v4.0.dll
%{_libdir}/mono/4.5/Mono.Debugger.Soft.dll
%{_libdir}/mono/4.5/Mono.CodeContracts.dll
%{_libdir}/mono/4.5/PEAPI.dll
%{_libdir}/mono/4.5/browsercaps-updater.exe*
%{_libdir}/mono/4.5/caspol.exe*
%{_libdir}/mono/4.5/cccheck.exe*
%{_libdir}/mono/4.5/ccrewrite.exe*
%{_libdir}/mono/4.5/cert2spc.exe*
%{_libdir}/mono/4.5/dtd2rng.exe*
%{_libdir}/mono/4.5/dtd2xsd.exe*
%{_libdir}/mono/4.5/genxs.exe*
%{_libdir}/mono/4.5/httpcfg.exe*
%{_libdir}/mono/4.5/ictool.exe*
%{_libdir}/mono/4.5/ilasm.exe*
%{_libdir}/mono/4.5/illinkanalyzer.exe*
%{_libdir}/mono/4.5/installvst.exe*
%{_libdir}/mono/4.5/lc.exe*
%{_libdir}/mono/4.5/macpack.exe*
%{_libdir}/mono/4.5/makecert.exe*
%{_libdir}/mono/4.5/mdbrebase.exe*
%{_libdir}/mono/4.5/mkbundle.exe*
%{_libdir}/mono/4.5/mono-api-info.exe*
%{_libdir}/mono/4.5/mono-api-html.exe*
%{_libdir}/mono/4.5/mono-api-diff.exe*
%{_libdir}/mono/4.5/mono-cil-strip.exe*
%{_libdir}/mono/4.5/mono-shlib-cop.exe*
%{_libdir}/mono/4.5/mono-xmltool.exe*
%{_libdir}/mono/4.5/monolinker.*
%{_libdir}/mono/4.5/monop.exe*
%{_libdir}/mono/4.5/pdb2mdb.exe*
%{_libdir}/mono/4.5/permview.exe*
%{_libdir}/mono/4.5/resgen.exe*
%{_libdir}/mono/4.5/secutil.exe*
%{_libdir}/mono/4.5/sgen.exe*
%{_libdir}/mono/4.5/signcode.exe*
%{_libdir}/mono/4.5/*symbolicate.exe*
%{_libdir}/mono/4.5/xbuild.exe*
%{_libdir}/mono/4.5/xbuild.rsp
%{_libdir}/mono/4.5/MSBuild/
# if roslyn
%{_libdir}/mono/msbuild/
%{_libdir}/mono/4.5/Microsoft.Build.xsd
%{_libdir}/mono/4.5/Microsoft.CSharp.targets
%{_libdir}/mono/4.5/Microsoft.Common.targets
%{_libdir}/mono/4.5/Microsoft.Common.tasks
%{_libdir}/mono/4.5/Microsoft.VisualBasic.targets
%{_libdir}/mono/4.5/Mono.XBuild.Tasks.dll
%{_libdir}/mono/gac/Microsoft.Build/
%{_libdir}/mono/gac/Microsoft.Build.Engine/
%{_libdir}/mono/gac/Microsoft.Build.Framework/
%{_libdir}/mono/gac/Microsoft.Build.Tasks.v4.0/
%{_libdir}/mono/gac/Microsoft.Build.Tasks.v12.0/
%{_libdir}/mono/gac/Microsoft.Build.Tasks.Core/
%{_libdir}/mono/gac/Microsoft.Build.Utilities.v4.0
%{_libdir}/mono/gac/Microsoft.Build.Utilities.v12.0/
%{_libdir}/mono/gac/Microsoft.Build.Utilities.Core/
%{_libdir}/mono/gac/Mono.CodeContracts/
%{_libdir}/mono/gac/Mono.Debugger.Soft/
%{_libdir}/mono/gac/Mono.XBuild.Tasks/
%{_libdir}/mono/gac/PEAPI/
%{_libdir}/mono/xbuild
%{_prefix}/lib/mono/xbuild-frameworks
%dir %{_libdir}/mono/
%{_libdir}/mono/lldb

%package -n mono-reactive
Summary: Reactive Extensions
License: Apache-2.0
Requires: mono-core = %{version}

%description -n mono-reactive
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Microsoft's Reactive Extensions.

%files -n mono-reactive
%defattr(-, qsys, *none)
%{_libdir}/pkgconfig/reactive.pc
%{_libdir}/mono/4.5/System.Reactive.Core.dll
%{_libdir}/mono/4.5/System.Reactive.Debugger.dll
%{_libdir}/mono/4.5/System.Reactive.Experimental.dll
%{_libdir}/mono/4.5/System.Reactive.Interfaces.dll
%{_libdir}/mono/4.5/System.Reactive.Linq.dll
%{_libdir}/mono/4.5/System.Reactive.Observable.Aliases.dll
%{_libdir}/mono/4.5/System.Reactive.PlatformServices.dll
%{_libdir}/mono/4.5/System.Reactive.Providers.dll
%{_libdir}/mono/4.5/System.Reactive.Runtime.Remoting.dll
%{_libdir}/mono/4.5/System.Reactive.Windows.Forms.dll
%{_libdir}/mono/4.5/System.Reactive.Windows.Threading.dll
%{_libdir}/mono/gac/System.Reactive.Core/
%{_libdir}/mono/gac/System.Reactive.Debugger/
%{_libdir}/mono/gac/System.Reactive.Experimental/
%{_libdir}/mono/gac/System.Reactive.Interfaces/
%{_libdir}/mono/gac/System.Reactive.Linq/
%{_libdir}/mono/gac/System.Reactive.Observable.Aliases/
%{_libdir}/mono/gac/System.Reactive.PlatformServices/
%{_libdir}/mono/gac/System.Reactive.Providers/
%{_libdir}/mono/gac/System.Reactive.Runtime.Remoting/
%{_libdir}/mono/gac/System.Reactive.Windows.Forms/
%{_libdir}/mono/gac/System.Reactive.Windows.Threading/

%package -n monodoc-core
Summary: Monodoc - Documentation tools for C# code
License: MIT X11
Requires: mono-core = %{version}

%description -n monodoc-core
Monodoc-core contains documentation tools for C#.

%files -n monodoc-core
%defattr(-, qsys, *none)
# These depend on mdoc, which is unhooked from build as of 7ab3811b934779c0622f6343ab2b75d64099e3d0
# The scripts on the no longer installed mdoc.exe, which will break
# This sub-package should probably be removed in favour of packaging https://github.com/mono/api-doc-tools soon,
# by fixing mcs to work with modern mdoc,
# patching mdoc, (https://gist.github.com/NattyNarwhal/b4945bc5e1f5213d5eaa8303261416bd)
# or by fixing up Roslyn to be good enough on PPC (far harder than it sounds)
%exclude %{_bindir}/mdassembler
%exclude %{_bindir}/mdoc
%exclude %{_bindir}/mdoc-assemble
%exclude %{_bindir}/mdoc-export-html
%exclude %{_bindir}/mdoc-export-msxdoc
%exclude %{_bindir}/mdoc-update
%exclude %{_bindir}/mdoc-validate
%exclude %{_bindir}/mdvalidater
%{_bindir}/mod
%exclude %{_bindir}/monodocer
%exclude %{_bindir}/monodocs2html
%exclude %{_bindir}/monodocs2slashdoc
%{_libdir}/pkgconfig/monodoc.pc
%{_mandir}/man1/mdassembler.1
%{_mandir}/man1/mdoc-assemble.1
%{_mandir}/man1/mdoc-export-html.1
%{_mandir}/man1/mdoc-export-msxdoc.1
%{_mandir}/man1/mdoc-update.1
%{_mandir}/man1/mdoc-validate.1
%{_mandir}/man1/mdoc.1
%{_mandir}/man1/mdvalidater.1
%{_mandir}/man1/monodocer.1
%{_mandir}/man1/monodocs2html.1
%{_mandir}/man5/mdoc.5
#%{_prefix}/lib/mono/4.5/mdoc.exe*
%{_prefix}/lib/mono/4.5/mod.exe*
%{_prefix}/lib/mono/gac/monodoc
%{_prefix}/lib/mono/monodoc
%{_prefix}/lib/monodoc

%package -n mono-complete
Summary: Install everything built from the mono source tree
License: MIT X11
Requires: libmono-2_0-1 = %{version}
Requires: libmono-2_0-devel = %{version}
Requires: mono-core = %{version}
Requires: libmonosgen-2_0-1 = %{version}
Requires: libmonosgen-2_0-devel = %{version}
Requires: mono-data = %{version}
Requires: mono-data-db2 = %{version}
Requires: mono-data-oracle = %{version}
Requires: mono-data-sqlite = %{version}
Requires: mono-devel = %{version}
Requires: mono-extras = %{version}
Requires: mono-mvc = %{version}
Requires: mono-reactive = %{version}
Requires: mono-wcf = %{version}
Requires: mono-web = %{version}
Requires: mono-winforms = %{version}
Requires: mono-winfxcore = %{version}
Requires: monodoc-core = %{version}

%description -n mono-complete
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Install everything built from the mono source tree.  Note that this does
not install anything from outside the mono source (XSP, mono-basic, etc.).

%files -n mono-complete
%defattr(-, qsys, *none)

%changelog

* Tue Aug 20 2019 Calvin Buckley <calvin@cmpct.into> - 6.7.0.253-1
- Update version
- Ship hang watchdog and aprofutil
- Revert some commits to unbreak behaviour (not real fixes, but mitigates real world problems, blech)
- Fix up dependency graph (but don't merge packages, bad idea)
- Unhook mdoc executables from packaging due to mdoc not compiling with mcs (and explain workarounds for future me)

* Fri Mar 29 2019 Calvin Buckley <calvin@cmpct.info> - 6.1.0.713-1
- Update version
- Disable static objects
- Remove NUnit as shipped by Mono, which no longer installs it
- Reinstate purging libtool files. Patch allows loading of .so archives.

* Wed Mar 6 2019 Calvin Buckley <calvin@cmpct.info> - 6.1.0.313-3
- Use SVR4 sonames to be more consistent with Rochester... and work.
- Initial attempt at fixing dependencies

* Sun Mar 3 2019 Calvin Buckley <calvin@cmpct.info> - 6.1.0.313-0
- Updated to the latest Mono nightly
- Make notes of things to fix in the future
- Include Mono.Native
- Update license to MIT

* Sat Nov 24 2018 Yvan Janssens <qsecofr@qseco.fr> - 5.21.0.521-0
- Updated to the latest Mono nightly.

