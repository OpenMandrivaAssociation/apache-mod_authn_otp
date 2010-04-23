#Module-Specific definitions
%define mod_name mod_authn_otp
%define mod_conf B55_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module for one-time password authentication
Name:		apache-%{mod_name}
Version:	1.1.0
Release: 	%mkrel 3
Group:		System/Servers
License:	Apache License
URL:		http://code.google.com/p/mod-authn-otp/
Source0:	http://mod-authn-otp.googlecode.com/files/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_authn_otp-1.1.0-no_funky_cflags.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

mod_authn_otp is especially useful for setting up protected web sites that
require more security than simple username/password authentication yet also
don't require users to install special VPN software, and is compatible with
software tokens that run on cell phones.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

%build
rm -f configure
libtoolize --copy --force; aclocal; autoconf
export LIBS="-L%{_libdir} -lcrypto"

%configure2_5x

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_mandir}/man1

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_bindir}
install -m0755 otptool %{buildroot}%{_bindir}/otptool
install -m0644 otptool.1 %{buildroot}%{_mandir}/man1/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES LICENSE README TODO users.sample
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_bindir}/otptool
%{_mandir}/man1/otptool.1*

