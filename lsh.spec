%define 	date	1999-05-11

Summary:	SSH replacement
Name:		lsh
Version:	19990511
Release:	2
Copyright:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	%{name}-snapshot-%{date}.tar.gz
BuildRequires:	autoconf
Prereq:		/usr/sbin/fix-info-dir
#Prereq:		/sbin/chkconfig
#Obsoletes:	mrt
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir /etc/%{name}
%define		find_requires_packages no

%description
Routing daemon with IPv6 support.

%description -l pl
Program do dynamicznego ustawiania tablicy tras.
Mo¿e tak¿e ustalaæ trasy dla IPv6

%package guile
Summary:	Guile interface for zebra routing daemon
Summary:	Guile dla programu zebra
Group:          Networking/Daemons
Group(pl):      Sieciowe/Serwery
Requires:	%{name} = %{version}

%description
Guile interface for zebra routing daemon.

%description guile -l pl
Guile dla programu zebra.

%prep
%setup -q -n %{name}-snapshot-%{date}

%build
autoconf
LDFLAGS="-s" ; export LDFLAGS
%configure \
	--with-sshd1=/usr/sbin/sshd1 \
	--with-zlib

make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d}

make install \
	DESTDIR=$RPM_BUILD_ROOT


#gzip -9nf README AUTHORS NEWS ChangeLog tools/* \
#	$RPM_BUILD_ROOT%{_infodir}/* 

%post
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add zebra >&2

if [ -f /var/run/zebra.pid ]; then
	/etc/rc.d/init.d/zebra restart >&2
else
	echo "Run \"/etc/rc.d/init.d/zebra start\" to start routing deamon." >&2
fi
    
%preun
if [ "$1" = "0" ]; then
	/etc/rc.d/init.d/zebra stop >&2
        /sbin/chkconfig --del zebra >&2
fi

%postun
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(640,root,root,755)
%attr(644,root,root) %doc *.gz tools/*
%attr(644,root,root) %{_infodir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
/etc/sysconfig/*
/etc/logrotate.d/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%doc %{_sysconfdir}/*.sample

%files guile
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
