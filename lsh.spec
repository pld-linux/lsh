Summary:	GNU implementation of the Secure Shell protocols
Summary(pl):	Implementacja GNU bezpiecznego shella
Name:		lsh
Version:	1.3.4
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.lysator.liu.se/pub/security/lsh/%{name}-%{version}.tar.gz
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-man-pages.tar.bz2
Patch0:		%{name}-noc99.patch
Patch1:		%{name}-remove_ipv6_check.patch
Patch2:		%{name}-automake.patch
Patch3:		%{name}-UINT64.patch
URL:		http://www.lysator.liu.se/~nisse/lsh/
BuildRequires:	slib
BuildRequires:	zlib-devel
BuildRequires:	gmp-devel
#Prereq:	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	 /etc/%{name}

%description
LSH is the GNU implementation of the secure shell protocols (secsh2).
LSH includes a client, a server, and a few scripts and utility
programs.

%description -l pl
LSH jest implementacj± GNU protoko³ów bezpiecznego shella (secsh2).
Zawiera klienta, serwer, kilka skryptów i narzêdzi.

%package devel
Summary:	Nettle low-level cryptographic library
Summary(pl):	Niskopoziomowa biblioteka kryptograficzna nettle
Group:		Development/Libraries

%description devel
Nettle low-level cryptographic library.

%description devel -l pl
Niskopoziomowa biblioteka kryptograficzna nettle.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
aclocal
autoconf
rm -f missing
automake -a -c -f --foreign
%configure \
	--with-sshd1=%{_sbindir}/sshd1 \
	--with-zlib \
	--disable-ipv6

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

gzip -9nf ANNOUNCE AUTHORS FAQ NEWS README doc/{NOTES,TASKLIST,TODO,*.txt}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.gz
%{_infodir}/lsh.info*
%{_mandir}/man[158]/*
#%attr(754,root,root) /etc/rc.d/init.d/*
#%attr(640,root,root) /etc/sysconfig/*
#%attr(640,root,root) /etc/logrotate.d/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libnettle.a
%{_includedir}/nettle
%{_infodir}/nettle.info*
