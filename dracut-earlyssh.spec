%define gitrepo http://github.com/philfry/%{name}.git
%define gitrev v%{version}

%if 0%{?el7}%{?fedora}
%global dracut %{_usr}/lib/dracut
%endif

%if 0%{?el6}
%global dracut %{_datadir}/dracut
%endif

Name: dracut-earlyssh
Version: 1.0.2
Release: 6%{?dist}
Summary: A dracut module that adds ssh to the boot image (also known as earlyssh)
Group: System Environment/Base
License: GPLv2+
URL: https://github.com/philfry/%{name}
Source0: %{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: dracut libblkid-devel gcc
Requires: dropbear dracut dracut-network openssh


%description
Dracut initramfs module to start dropbear sshd on early boot to enter
encryption passphrase from across the internets or just connect and debug
whatever stuff there.

Idea is to use the thing on remote VDS servers, where full-disk encryption is
still desirable (if only to avoid data leaks when disks will be decomissioned
and sold by VDS vendor) but rather problematic due to lack of KVM or whatever
direct console access.

Authenticates users strictly by provided authorized_keys ("dropbear_acl"
option) file.

See dropbear(8) manpage for full list of supported restrictions there
(which are fairly similar to openssh).

Please read the README and configuration parameters in 
/etc/dracut.conf.d/earlyssh.conf before use.


%prep
%setup -q


%build
./configure
make %{?_smp_mflags}


%install
[ '%{buildroot}' != '/' ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
[ '%{buildroot}' != '/' ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md COPYING
%config(noreplace) %{_sysconfdir}/dracut.conf.d/earlyssh.conf
%dir %{_libexecdir}/dracut-earlyssh
%{_libexecdir}/dracut-earlyssh/unlock
%{_libexecdir}/dracut-earlyssh/console_auth
%dir %{dracut}/modules.d/60earlyssh
%{dracut}/modules.d/60earlyssh/module-setup.sh
%{dracut}/modules.d/60earlyssh/console_peek.sh
%{dracut}/modules.d/60earlyssh/unlock-reap-success.sh
%{dracut}/modules.d/60earlyssh/50-udev-pty.rules
%if 0%{?el6}
%{dracut}/modules.d/60earlyssh/dummyroot
%{dracut}/modules.d/60earlyssh/check
%{dracut}/modules.d/60earlyssh/install
%dir %{dracut}/modules.d/91cryptsettle-patch
%{dracut}/modules.d/91cryptsettle-patch/check
%{dracut}/modules.d/91cryptsettle-patch/install
%{dracut}/modules.d/91cryptsettle-patch/module-setup.sh
%endif
