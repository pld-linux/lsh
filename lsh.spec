%define 	date	1999-05-11

Summary:	SSH replacement
Name:		lsh
Version:	19990511
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	%{name}-snapshot-%{date}.tar.gz
BuildRequires:	autoconf
#Prereq:		/sbin/chkconfig
#Obsoletes:	mrt
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir /etc/%{name}
%define		find_requires_packages no

%description
Routing daemon with IPv6 support.

%description -l pl
Program do dynamicznego ustawiania tablicy tras. Mo¿e tak¿e ustalaæ
trasy dla IPv6

%package guile
Summary:	Guile interface for zebra routing daemon
Summary:	Guile dla programu zebra
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}

%description
Guile interface for zebra routing daemon.

%description guile -l pl
Guile dla programu zebra.

%prep
%setup -q -n %{name}-snapshot-%{date}

%build
autoconf
%configure \
	--with-sshd1=%{_sbindir}/sshd1 \
	--with-zlib

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#gzip -9nf README AUTHORS NEWS ChangeLog tools/*

%post
%fix_info_dir
NAME=zebra; DESC="routing daemon"; %chkconfig_add
    
%preun
NAME=zebra; %chkconfig_del

%postun
%fix_info_dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz tools/*
%{_infodir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) /etc/sysconfig/*
%attr(640,root,root) /etc/logrotate.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%attr(640,root,root) %doc %{_sysconfdir}/*.sample

%files guile
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
