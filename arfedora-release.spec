%global release_name Arfedora
# If you're not building this on Fedora, you're going to have a bad day.... but whatever.
%if 0%{?fedora}
%global dist_version %{fedora}
%else
%global dist_version 38
%endif

Summary:	Arfedora release files
Name:		arfedora-release
Version:	%{dist_version}
Release:	0.2
License:	MIT
URL:            https://github.com/yucefsourani/arfedora-release
Source0:	https://github.com/yucefsourani/arfedora-release/archive/main.zip
BuildArch: noarch

Provides: arfedora-release = %{version}-%{release}
Provides: arfedora-release-variant = %{version}-%{release}
Provides: arfedora-release-identity = %{version}-%{release}

# We need to Provides: and Conflicts: system release here and in each
# of the generic-release-$VARIANT subpackages to ensure that only one
# may be installed on the system at a time.
Conflicts: system-release
Provides: system-release
Provides: system-release(%{version})
Conflicts:	fedora-release
Conflicts:	fedora-release-identity
Conflicts:	generic-release
Conflicts:	generic-release-identity
Requires: arfedora-release-common = %{version}-%{release}

%description
Arfedora release files such as yum configs and various /etc/ files that
define the release.


%package common
Summary: Arfedora release files

Requires:   arfedora-release-variant = %{version}-%{release}
Suggests:   arfedora-release

Obsoletes:  arfedora-release < 30-0.1

Obsoletes:  convert-to-edition < 30-0.7
Requires:   fedora-repos(%{version})

Conflicts: fedora-release-common
Conflicts: generic-release-common

%description common
Release files common to all Editions and Spins


%package notes
Summary:	Release Notes
License:	Open Publication
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	fedora-release-notes
Conflicts:	generic-release-notes

%description notes
Arfedora release notes package.


%prep
%autosetup -n  arfedora-release-main

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "Arfedora release %{version} (%{release_name})" > %{buildroot}%{_prefix}/lib/fedora-release
echo "cpe:/o:arfedora:arfedora:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Symlink the -release files
install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/fedora-release %{buildroot}%{_sysconfdir}/fedora-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s fedora-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s fedora-release %{buildroot}%{_sysconfdir}/system-release

# Create the common os-release file
install -d $RPM_BUILD_ROOT/usr/lib/os.release.d/
cat << EOF >>%{buildroot}%{_prefix}/lib/os-release
NAME=Arfedora
VERSION="%{dist_version} (%{release_name})"
ID=arfedora
ID_LIKE=fedora
VERSION_ID=%{dist_version}
PRETTY_NAME="Arfedora %{dist_version} (%{release_name})"
ANSI_COLOR="0;34"
LOGO=fedora-logo-icon
CPE_NAME="cpe:/o:arfedora:arfedora:%{dist_version}"
HOME_URL="https://github.com/yucefsourani/arfedora"
SUPPORT_URL="https://github.com/yucefsourani/arfedora"
BUG_REPORT_URL="https://github.com/yucefsourani/arfedora/issues"
REDHAT_BUGZILLA_PRODUCT="Arfedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="Arfedora"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
PRIVACY_POLICY_URL="http://nsa.gov"
EOF

# Create the common /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create os-release and issue files for the different editions here
# There are no separate editions for generic-release

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release $RPM_BUILD_ROOT/etc/os-release

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora                %{dist_version}
%%dist                %%{?distprefix}.fc%{dist_version}%%{?with_bootstrap:~bootstrap}
%%fc%{dist_version}                1
EOF

# Install readme
mkdir -p readme
install -pm 0644 README.license readme/README.Arfedora-Release-Notes

# Install licenses
mkdir -p licenses
install -pm 0644 LICENSE licenses/LICENSE
install -pm 0644 README.Arfedora-Release-Notes licenses/README.license

# Add presets
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/user-preset/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

# Default system wide
install -Dm0644 85-display-manager.preset -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 90-default.preset -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 99-default-disable.preset -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -Dm0644 90-default-user.preset -t $RPM_BUILD_ROOT%{_prefix}/lib/systemd/user-preset/


%files common
%license licenses/LICENSE licenses/README.license
%{_prefix}/lib/fedora-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/fedora-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset


%files
%{_prefix}/lib/os-release


%files notes
%doc readme/README.Arfedora-Release-Notes


%changelog
* Sat May 6 2023 Yucef sourani <youssef.m.sourani@gmail.com> 38-0.2
- release 0.2

* Sat May 6 2023 Yucef sourani <youssef.m.sourani@gmail.com> 38-0.1
- initial 
- version 38
- release 0.1
