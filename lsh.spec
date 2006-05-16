#
# Conditional build:
%bcond_without	kerberos	# without kerberos support
#
Summary:	GNU implementation of the Secure Shell protocols
Summary(pl):	Implementacja GNU bezpiecznego shella
Name:		lsh
Version:	2.0.3
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.lysator.liu.se/pub/security/lsh/%{name}-%{version}.tar.gz
# Source0-md5:	2edcb2f48f2b541e757ccdff70387fcb
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
# Source1-md5:	164cdde8060577b54954c3f9f067927e
Patch0:		%{name}-info.patch
Patch1:		%{name}-shared-nettle.patch
URL:		http://www.lysator.liu.se/~nisse/lsh/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmp-devel
%{?with_kerberos:BuildRequires:	heimdal-devel >= 0.7}
BuildRequires:	liboop-devel
BuildRequires:	nettle-devel >= 1.14
BuildRequires:	pam-devel
BuildRequires:	slib
BuildRequires:	texinfo
BuildRequires:	zlib-devel
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

%description -l pl
LSH jest implementacj± GNU protoko³ów bezpiecznego shella (secsh2).
Zawiera klienta, serwer, kilka skryptów i narzêdzi.

Uwaga: ta implementacja nie obs³uguje protoko³u SSH1, ale serwer mo¿e
wywo³aæ /usr/sbin/sshd. Je¶li obs³uga SSH1 jest potrzebna w serwerze,
nale¿y zainstalowaæ odpowiedniego demona (openssh-server lub SSH.COM
1.2.x) jako /usr/sbin/sshd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
	%{!?with_kerberos:--disable-kerberos} \
	--with-sshd1=%{_sbindir}/sshd \
	--with-zlib

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig,logrotate.d},/var/spool/lsh}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}
bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc ANNOUNCE AUTHORS ChangeLog FAQ NEWS README
%doc doc/{HACKING,NOTES,PORTS,TASKLIST,TODO,*.txt}
#%attr(754,root,root) /etc/rc.d/init.d/*
#%attr(640,root,root) /etc/sysconfig/*
#%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/*
%dir %attr(6750,root,root) /var/spool/lsh
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_infodir}/lsh.info*
%{_mandir}/man[158]/*
