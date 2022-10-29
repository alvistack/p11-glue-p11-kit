# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: p11-kit
Epoch: 100
Version: 0.24.1
Release: 1%{?dist}
Summary: Library to work with PKCS#11 modules
License: BSD-3-Clause
URL: https://github.com/p11-glue/p11-kit/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
BuildRequires: bash-completion-devel
%endif
BuildRequires: bash-completion
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libffi-devel
BuildRequires: libtasn1-devel >= 2.3
BuildRequires: libtasn1-tools
BuildRequires: meson
BuildRequires: ninja-build
BuildRequires: pkgconfig
BuildRequires: systemd
BuildRequires: systemd-devel

%description
p11-kit provides a way to load and enumerate PKCS#11 modules, as well as
a standard configuration setup for installing PKCS#11 modules in such a
way that they're discoverable.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%meson \
    -Dbash_completion=enabled \
    -Dgtk_doc=false \
    -Dman=false
%meson_build

%install
%meson_install
find %{buildroot} -type f -name '*.la' -exec rm -rf {} \;

%check

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libp11-kit0
Summary: Library to work with PKCS#11 modules

%description -n libp11-kit0
p11-kit provides a way to load and enumerate PKCS#11 modules, as well as
a standard configuration setup for installing PKCS#11 modules in such a
way that they're discoverable.

%package -n p11-kit-devel
Summary: Library to work with PKCS#11 modules -- Development Files
Requires: libp11-kit0 = %{epoch}:%{version}-%{release}

%description -n p11-kit-devel
p11-kit provides a way to load and enumerate PKCS#11 modules, as well as
a standard configuration setup for installing PKCS#11 modules in such a
way that they're discoverable.

%package -n p11-kit-tools
Summary: Library to work with PKCS#11 modules -- Tools
Requires: libp11-kit0 = %{epoch}:%{version}-%{release}

%description -n p11-kit-tools
p11-kit provides a way to load and enumerate PKCS#11 modules, as well as
a standard configuration setup for installing PKCS#11 modules in such a
way that they're discoverable.

%package -n p11-kit-server
Summary: Server and client commands for p11-kit
Requires: p11-kit = %{epoch}:%{version}-%{release}

%description -n p11-kit-server
Command line tools that enable to export PKCS#11 modules through a Unix
domain socket. Note that this feature is still experimental.

%post -n libp11-kit0 -p /sbin/ldconfig
%postun -n libp11-kit0 -p /sbin/ldconfig

%files
%dir %{_datadir}/locale/*
%dir %{_datadir}/locale/*/*
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%dir %{_libdir}/pkcs11
%dir %{_libexecdir}/p11-kit
%{_datadir}/locale/*/LC_MESSAGES/*
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libdir}/pkcs11/p11-kit-trust.so
%{_libexecdir}/p11-kit/p11-kit-remote
%{_libexecdir}/p11-kit/trust-extract-compat

%files -n libp11-kit0
%license COPYING
%dir %{_sysconfdir}/pkcs11
%{_libdir}/libp11-kit.so.*
%{_libdir}/p11-kit-proxy.so
%{_sysconfdir}/pkcs11/pkcs11.conf.example

%files -n p11-kit-devel
%{_includedir}/p11-kit-1
%{_libdir}/libp11-kit.so
%{_libdir}/pkgconfig/p11-kit-1.pc

%files -n p11-kit-tools
%{_bindir}/p11-kit
%{_bindir}/trust
%{_datadir}/bash-completion/completions/p11-kit
%{_datadir}/bash-completion/completions/trust

%files -n p11-kit-server
%{_libdir}/pkcs11/p11-kit-client.so
%{_libexecdir}/p11-kit/p11-kit-server
%{_userunitdir}/p11-kit-server.service
%{_userunitdir}/p11-kit-server.socket
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n p11-kit-devel
Summary: Development files for p11-kit
Requires: p11-kit = %{epoch}:%{version}-%{release}

%description -n p11-kit-devel
The p11-kit-devel package contains libraries and header files for
developing applications that use p11-kit.

%package -n p11-kit-trust
Summary: System trust module from p11-kit
Requires: p11-kit = %{epoch}:%{version}-%{release}

%description -n p11-kit-trust
The p11-kit-trust package contains a system trust PKCS#11 module which
contains certificate anchors and black lists.

%package -n p11-kit-server
Summary: Server and client commands for p11-kit
Requires: p11-kit = %{epoch}:%{version}-%{release}

%description -n p11-kit-server
The p11-kit-server package contains command line tools that enable to
export PKCS#11 modules through a Unix domain socket. Note that this
feature is still experimental.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/p11-kit
%{_datadir}/bash-completion/completions/p11-kit
%{_datadir}/locale/*/LC_MESSAGES/*
%{_libdir}/libp11-kit.so.*
%{_libdir}/p11-kit-proxy.so
%{_libexecdir}/p11-kit/p11-kit-remote
%{_sysconfdir}/pkcs11/pkcs11.conf.example

%files -n p11-kit-devel
%{_includedir}/p11-kit-1
%{_libdir}/libp11-kit.so
%{_libdir}/pkgconfig/p11-kit-1.pc

%files -n p11-kit-trust
%{_bindir}/trust
%{_datadir}/bash-completion/completions/trust
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libdir}/pkcs11/p11-kit-trust.so
%{_libexecdir}/p11-kit/trust-extract-compat

%files -n p11-kit-server
%{_libdir}/pkcs11/p11-kit-client.so
%{_libexecdir}/p11-kit/p11-kit-server
%{_userunitdir}/p11-kit-server.service
%{_userunitdir}/p11-kit-server.socket
%endif

%changelog
