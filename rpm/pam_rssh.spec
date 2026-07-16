# The rust toolchain's debug info trips up rpm's debuginfo extraction on
# some targets; the module is small, so skip the -debuginfo subpackage.
%global debug_package %{nil}

Name:           pam_rssh
Version:        1.2.0
Release:        1%{?dist}
Summary:        PAM module for SSH-agent based authentication

License:        MIT
URL:            https://github.com/z4yx/pam_rssh
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  pam-devel
BuildRequires:  openssl-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
Requires:       pam

%description
This PAM module provides ssh-agent based authentication. It allows
authentication using SSH keys forwarded through ssh-agent instead of
typing passwords. This is particularly useful for remote sudo access
with hardware security keys like Yubikey or Canokey.

Supported SSH key types: RSA (SHA256), ECDSA 256/384/521, ECDSA-SK
(FIDO2/U2F), ED25519 and ED25519-SK (FIDO2).

%prep
%autosetup -n %{name}-%{version}

%build
# A current toolchain is provided on PATH by the CI workflow (rustup); the
# crate's pinned dependencies require a newer rustc than the distro packages.
cargo build --release --locked

%install
install -D -m 0755 target/release/libpam_rssh.so \
    %{buildroot}%{_libdir}/security/libpam_rssh.so

%files
%license LICENSE
%doc README.md
%{_libdir}/security/libpam_rssh.so

%changelog
* Fri Jul 17 2026 Yuxiang Zhang <yuxiang.zhang@tuna.tsinghua.edu.cn> - 1.2.0-1
- Initial RPM package
