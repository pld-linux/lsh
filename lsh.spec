%define 	date	1999-05-11

Summary:	SSH replacement
Name:		lsh
Version:	19990511
Release:	1
Copyright:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	%{name}-snapshot-%{date}.tar.gz
BuildPrereq:	autoconf
#Prereq:		/sbin/install-info
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
/sbin/install-info %{_infodir}/%{name}.info.gz /etc/info-dir >&2
/sbin/chkconfig --add zebra >&2

if [ -f /var/run/zebra.pid ]; then
	/etc/rc.d/init.d/zebra restart >&2
else
	echo "Run \"/etc/rc.d/init.d/zebra start\" to start routing deamon." >&2
fi
    
%preun
if [ "$1" = "0" ]; then
        /sbin/install-info --delete %{_infodir}/%{name}.info.gz \
		/etc/info-dir >&2
	/etc/rc.d/init.d/zebra stop >&2
        /sbin/chkconfig --del zebra >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(640,root,root,755)
%attr(644,root,root) %doc *.gz tools/*
%attr(644,root,root) %{_infodir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /etc/rc.d/init.d/*
/etc/sysconfig/*
/etc/logrotate.d/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%doc %{_sysconfdir}/*.sample

%files guile
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%changelog
* Sun May 16 1999 Artur Frysiak <wiget@pld.org.pl>
  [19990516-1]
- initial version
