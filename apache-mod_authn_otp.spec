#Module-Specific definitions
%define apache_version 2.4.69
%define mod_name mod_authn_otp
%define mod_conf B55_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module for one-time password authentication
Name:		apache-%{mod_name}
Version:	1.1.12
Release:	1
Group:		System/Servers
License:	Apache License
URL:		https://github.com/archiecobbs/mod-authn-otp
Source0:	https://github.com/archiecobbs/mod-authn-otp/archive/refs/tags/%{version}/mod_authn_otp-%{version}.tar.gz
Source1:	%{mod_conf}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnu-config
BuildRequires:	make
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(apr-1)

%description
mod_authn_otp is an Apache web server module for two-factor authentication
using one-time passwords (OTP) generated via the HOTP/OATH algorithm defined in
RFC 4226. This creates a simple way to protect a web site with one-time
passwords, using any RFC 4226-compliant hardware or software token device.
mod_authn_otp also supports the Mobile-OTP algorithm.

mod_authn_otp supports both event and time based one-time passwords. It also
supports "lingering" which allows the repeated re-use of a previously used
one-time password up to a configurable maximum linger time. This allows
one-time passwords to be used directly in HTTP authentication without forcing
the user to enter a new one-time password for every page load.

mod_authn_otp supports both basic and digest authentication, and will
auto-synchronize with the user's token within a configurable maximum offset
(auto-synchronization is not supported with digest authentication).

%prep
%autosetup -n mod-authn-otp-%{version}
cp %{SOURCE1} %{mod_conf}

%build
sh autogen.sh
%configure --with-apxs=%{_bindir}/apxs
%make_build

%install
%make_install
mkdir -p %{buildroot}%{_libdir}/apache-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
# Keep the historical extramodules path the modules.d snippet loads.
mv %{buildroot}$(%{_bindir}/apxs -q LIBEXECDIR)/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%files
%doc CHANGES LICENSE README users.sample
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_bindir}/otptool
%{_bindir}/otplock
%{_bindir}/genotpurl
%{_mandir}/man1/otptool.1*
%{_mandir}/man1/otplock.1*
%{_mandir}/man1/genotpurl.1*
