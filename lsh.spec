#
# Conditional build:
%bcond_without	kerberos5	# without kerberos V support
#
Summary:	GNU implementation of the Secure Shell protocols
Summary(pl.UTF-8):	Implementacja GNU bezpiecznego shella
Name:		lsh
Version:	2.1
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz
# Source0-md5:	cde8e1306b1c544909e1e9ecb86e6402
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	164cdde8060577b54954c3f9f067927e
Patch0:		%{name}-info.patch
URL:		http://www.lysator.liu.se/~nisse/lsh/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	gmp-devel >= 3.1
BuildRequires:	groff
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	liboop-devel
BuildRequires:	libwrap-devel
BuildRequires:	m4
BuildRequires:	nettle-devel >= 1.14
BuildRequires:	pam-devel
BuildRequires:	texinfo
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	zlib-devel
# only for maintainer mode
#BuildRequires:	guile
#BuildRequires:	slib
Requires:	nettle >= 1.14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	 /etc/%{name}

%description
LSH is the GNU implementation of the secure shell protocols (secsh2).
LSH includes a client, a server, and a few scripts and utility
programs.

Note: it doesn't support SSH1 protocol, but the server can fallback to
/usr/sbin/sshd - if you need SSH1 support in server, please install
appropriate daemon (openssh-server, SSH.COM 1.2.x) as /usr/sbin/sshd.

%description -l pl.UTF-8
LSH jest implementacją GNU protokołów bezpiecznego shella (secsh2).
Zawiera klienta, serwer, kilka skryptów i narzędzi.

Uwaga: ta implementacja nie obsługuje protokołu SSH1, ale serwer może
wywołać /usr/sbin/sshd. Jeśli obsługa SSH1 jest potrzebna w serwerze,
należy zainstalować odpowiedniego demona (openssh-server lub SSH.COM
1.2.x) jako /usr/sbin/sshd.

%prep
%setup -q
%patch0 -p1

%build
cd src/spki
%{__aclocal}
%{__autoconf}
%{__automake}
cd ../..
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	XAUTH_PROGRAM=/usr/bin/xauth \
	%{!?with_kerberos5:--disable-kerberos} \
	--with-sshd1=%{_sbindir}/sshd \
	--with-tcpwrappers \
	--with-zlib

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig,logrotate.d},/var/spool/lsh}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}
bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{README.lsh-man-pages,diff.*}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc ANNOUNCE AUTHORS ChangeLog* FAQ NEWS README doc/{HACKING,NOTES,PORTS,TASKLIST,TODO,*.txt}
#%attr(754,root,root) /etc/rc.d/init.d/*
#%attr(640,root,root) /etc/sysconfig/*
#%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/*
%attr(6750,root,root) %dir /var/spool/lsh
%attr(755,root,root) %{_bindir}/lcp
%attr(755,root,root) %{_bindir}/lsftp
%attr(755,root,root) %{_bindir}/lsh
%attr(755,root,root) %{_bindir}/lsh-authorize
%attr(755,root,root) %{_bindir}/lsh-decode-key
%attr(755,root,root) %{_bindir}/lsh-decrypt-key
%attr(755,root,root) %{_bindir}/lsh-export-key
%attr(755,root,root) %{_bindir}/lsh-keygen
%attr(755,root,root) %{_bindir}/lsh-make-seed
%attr(755,root,root) %{_bindir}/lsh-upgrade
%attr(755,root,root) %{_bindir}/lsh-upgrade-key
%attr(755,root,root) %{_bindir}/lsh-writekey
%attr(755,root,root) %{_bindir}/lshg
%attr(755,root,root) %{_bindir}/srp-gen
%attr(755,root,root) %{_bindir}/ssh-conv
%attr(755,root,root) %{_sbindir}/lsh-execuv
%{?with_kerberos5:%attr(755,root,root) %{_sbindir}/lsh-krb-checkpw}
%attr(755,root,root) %{_sbindir}/lsh-pam-checkpw
%attr(755,root,root) %{_sbindir}/lshd
%attr(755,root,root) %{_sbindir}/sftp-server
%{_infodir}/lsh.info*
%{_mandir}/man1/lsftp.1*
%{_mandir}/man1/lsh.1*
%{_mandir}/man1/lsh-authorize.1*
%{_mandir}/man1/lsh-decode-key.1*
%{_mandir}/man1/lsh-decrypt-key.1*
%{_mandir}/man1/lsh-export-key.1*
%{_mandir}/man1/lsh-keygen.1*
%{_mandir}/man1/lsh-make-seed.1*
%{_mandir}/man1/lsh-upgrade.1*
%{_mandir}/man1/lsh-upgrade-key.1*
%{_mandir}/man1/lsh-writekey.1*
%{_mandir}/man1/lshg.1*
%{_mandir}/man1/sexp-conv.1*
%{_mandir}/man1/srp-gen.1*
%{_mandir}/man1/ssh-conv.1*
%{_mandir}/man5/DSA.5*
%{_mandir}/man5/SHA.5*
%{_mandir}/man5/SPKI.5*
%{_mandir}/man5/secsh.5*
%{_mandir}/man8/lshd.8*
%{_mandir}/man8/sftp-server.8*
