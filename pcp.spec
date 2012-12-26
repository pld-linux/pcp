# TODO:
# - pcp user/group, log dirs (see Debian packaging)
# - PLDify init scripts
# - /var/lib/pcp looks like mess, configs/variable data/scripts/ELFs (maybe consult Debian packaging?)
#
%include	/usr/lib/rpm/macros.perl
Summary:	Performance Co-Pilot - system level performance monitoring and management
Summary(pl.UTF-8):	Performance Co-Pilot - monitorowanie i zarządzanie wydajnością na poziomie systemu
Name:		pcp
Version:	3.6.10
Release:	1
License:	LGPL v2.1 (libraries), GPL v2 (the rest)
Group:		Applications/System
Source0:	ftp://oss.sgi.com/projects/pcp/download/%{name}-%{version}.src.tar.gz
# Source0-md5:	f39a581638ab9419d30f3d814841938b
Patch0:		%{name}-ps.patch
Patch1:		%{name}-opt.patch
URL:		http://oss.sgi.com/projects/pcp/
BuildRequires:	autoconf >= 2.60
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Performance Co-Pilot (PCP) is a framework and services to support
system-level performance monitoring and performance management.

The Performance Co-Pilot provides a unifying abstraction for all of
the interesting performance data in a system, and allows client
applications to easily retrieve and process any subset of that data.

%description -l pl.UTF-8
PCP (Performance Co-Pilot) to szkielet i usługi mające na celu
obsługę monitorowania wydajności i zarządzania wydajnością.

PCP udostępnia ujednoliconą abstrakcję dla wszystkich interesujących
danych związanych z wydajnością w systemie i pozwala aplikacjom
klienckim łatwo odczytywać i przetwarzać dowolny podzbiór tych danych.

%package libs
Summary:	PCP libraries
Summary(pl.UTF-8):	Biblioteki PCP
Group:		Libraries

%description libs
PCP libraries.

%description libs -l pl.UTF-8
Biblioteki PCP.

%package devel
Summary:	Header files for PCP libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek PCP
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for PCP libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek PCP.

%package static
Summary:	Static PCP libraries
Summary(pl.UTF-8):	Statyczne biblioteki PCP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PCP libraries.

%description static -l pl.UTF-8
Statyczne biblioteki PCP.

%package -n perl-pcp
Summary:	Perl interface to PCP libraries
Summary(pl.UTF-8):	Perlowy interfejs do bibliotek PCP
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{version}-%{release}

%description -n perl-pcp
Perl interface to PCP libraries.

%description -n perl-pcp -l pl.UTF-8
Perlowy interfejs do bibliotek PCP.

%package -n python-pcp
Summary:	Python interface to PCP libraries
Summary(pl.UTF-8):	Pythonowy interfejs do bibliotek PCP
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-pcp
Python interface to PCP libraries.

%description -n python-pcp -l pl.UTF-8
Pythonowy interfejs do bibliotek PCP.

%package -n bash-completion-pcp
Summary:	bash-completion for PCP utilities
Summary(pl.UTF-8):	Bashowe uzupełnianie nazw dla narzędzi PCP
Group:		Applications/Shells
Requires:	bash-completion

%description -n bash-completion-pcp
bash-completion for PCP utilities.

%description -n bash-completion-pcp -l pl.UTF-8
Bashowe uzupełnianie nazw dla narzędzi PCP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure \
	--with-rcdir=/etc/rc.d/init.d
# ensure not *zipping man pages on install
%{__sed} -i -e '/^HAVE_.*ED_MANPAGES/s,true,false,' src/include/builddefs

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DIST_ROOT=$RPM_BUILD_ROOT \
	INSTALL='$(INSTALL_SH)' \
	HAVE_BZIP2ED_MANPAGES=false \
	HAVE_GZIPPED_MANPAGES=false \
	HAVE_LZMAED_MANPAGES=false \
	HAVE_XZED_MANPAGES=false

install -p src/pmns/stdpmid $RPM_BUILD_ROOT/var/lib/pcp/pmns

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

# ???
%{__rm} -r $RPM_BUILD_ROOT/default
# could be eventually packaged in examplesdir / docdir resp.
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/pcp/{demos,examples}
# tests
%{__rm} -r $RPM_BUILD_ROOT/var/lib/pcp/testsuite

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs
/sbin/ldconfig
cd /var/lib/pcp/pmns
umask 022
PCP_DIR= PCP_TMP_DIR=/tmp ./Make.stdpmid

%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG README
%attr(755,root,root) %{_bindir}/dbpmda
%attr(755,root,root) %{_bindir}/genpmda
%attr(755,root,root) %{_bindir}/iostat2pcp
%attr(755,root,root) %{_bindir}/mrtg2pcp
%attr(755,root,root) %{_bindir}/pcp
%attr(755,root,root) %{_bindir}/pmafm
%attr(755,root,root) %{_bindir}/pmclient
%attr(755,root,root) %{_bindir}/pmcollectl
%attr(755,root,root) %{_bindir}/pmconfig
%attr(755,root,root) %{_bindir}/pmdate
%attr(755,root,root) %{_bindir}/pmdbg
%attr(755,root,root) %{_bindir}/pmdumplog
%attr(755,root,root) %{_bindir}/pmerr
%attr(755,root,root) %{_bindir}/pmevent
%attr(755,root,root) %{_bindir}/pmgenmap
%attr(755,root,root) %{_bindir}/pmie
%attr(755,root,root) %{_bindir}/pmie2col
%attr(755,root,root) %{_bindir}/pmieconf
%attr(755,root,root) %{_bindir}/pminfo
%attr(755,root,root) %{_bindir}/pmlc
%attr(755,root,root) %{_bindir}/pmlogcheck
%attr(755,root,root) %{_bindir}/pmloglabel
%attr(755,root,root) %{_bindir}/pmlogsummary
%attr(755,root,root) %{_bindir}/pmprobe
%attr(755,root,root) %{_bindir}/pmsocks
%attr(755,root,root) %{_bindir}/pmstat
%attr(755,root,root) %{_bindir}/pmstore
%attr(755,root,root) %{_bindir}/pmtrace
%attr(755,root,root) %{_bindir}/pmval
%attr(755,root,root) %{_bindir}/sar2pcp
%attr(755,root,root) %{_bindir}/sheet2pcp
%attr(755,root,root) %{_libdir}/pcp/bin/autofsd-probe
%attr(755,root,root) %{_libdir}/pcp/bin/chkhelp
%attr(755,root,root) %{_libdir}/pcp/bin/install-sh
%attr(755,root,root) %{_libdir}/pcp/bin/mkaf
%attr(755,root,root) %{_libdir}/pcp/bin/pmcd
%attr(755,root,root) %{_libdir}/pcp/bin/pmcd_wait
%attr(755,root,root) %{_libdir}/pcp/bin/pmhostname
%attr(755,root,root) %{_libdir}/pcp/bin/pmie_check
%attr(755,root,root) %{_libdir}/pcp/bin/pmie_daily
%attr(755,root,root) %{_libdir}/pcp/bin/pmie_email
%attr(755,root,root) %{_libdir}/pcp/bin/pmiestatus
%attr(755,root,root) %{_libdir}/pcp/bin/pmlock
%attr(755,root,root) %{_libdir}/pcp/bin/pmlogconf
%attr(755,root,root) %{_libdir}/pcp/bin/pmlogconf-setup
%attr(755,root,root) %{_libdir}/pcp/bin/pmlogextract
%attr(755,root,root) %{_libdir}/pcp/bin/pmlogger
%attr(755,root,root) %{_libdir}/pcp/bin/pmlogger_check
%attr(755,root,root) %{_libdir}/pcp/bin/pmlogger_daily
%attr(755,root,root) %{_libdir}/pcp/bin/pmlogger_merge
%attr(755,root,root) %{_libdir}/pcp/bin/pmlogreduce
%attr(755,root,root) %{_libdir}/pcp/bin/pmlogrewrite
%attr(755,root,root) %{_libdir}/pcp/bin/pmnewlog
%attr(755,root,root) %{_libdir}/pcp/bin/pmnsadd
%attr(755,root,root) %{_libdir}/pcp/bin/pmnsdel
%attr(755,root,root) %{_libdir}/pcp/bin/pmnsmerge
%attr(755,root,root) %{_libdir}/pcp/bin/pmpost
%attr(755,root,root) %{_libdir}/pcp/bin/pmproxy
%attr(755,root,root) %{_libdir}/pcp/bin/pmsignal
%attr(755,root,root) %{_libdir}/pcp/bin/pmsleep
%attr(755,root,root) %{_libdir}/pcp/bin/pmwtf
%attr(755,root,root) %{_libdir}/pcp/bin/telnet-probe
%dir %{_datadir}/pcp
%dir %{_datadir}/pcp/lib
%attr(755,root,root) %{_datadir}/pcp/lib/ReplacePmnsSubtree
%attr(755,root,root) %{_datadir}/pcp/lib/lockpmns
%attr(755,root,root) %{_datadir}/pcp/lib/unlockpmns
%{_datadir}/pcp/lib/bashproc.sh
%{_datadir}/pcp/lib/pmdaproc.sh
%{_datadir}/pcp/lib/rc-proc.sh
%{_datadir}/pcp/lib/rc-proc.sh.minimal
%{_sysconfdir}/pcp.sh
%attr(754,root,root) /etc/rc.d/init.d/pcp
%attr(754,root,root) /etc/rc.d/init.d/pmcd
%attr(754,root,root) /etc/rc.d/init.d/pmie
%attr(754,root,root) /etc/rc.d/init.d/pmlogger
%attr(754,root,root) /etc/rc.d/init.d/pmproxy
%dir /var/lib/pcp/config
%dir /var/lib/pcp/config/pmafm
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmafm/pcp
%dir /var/lib/pcp/config/pmcd
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmcd/pmcd.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmcd/pmcd.options
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmcd/rc.local
%dir /var/lib/pcp/config/pmchart
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Apache
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Cisco
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Sendmail
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Sample
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Web.*
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/shping.*
%dir /var/lib/pcp/config/pmie
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmie/config.default
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmie/control
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmie/crontab
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmie/stomp
%dir /var/lib/pcp/config/pmie/cisco
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmie/cisco/in_util
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmie/cisco/out_util
%dir /var/lib/pcp/config/pmieconf
%dir /var/lib/pcp/config/pmieconf/cpu
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/context_switch
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/load_average
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/low_util
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/system
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/util
%dir /var/lib/pcp/config/pmieconf/filesys
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/filesys/filling
%dir /var/lib/pcp/config/pmieconf/global
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/global/parameters
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/global/pcp_actions
%dir /var/lib/pcp/config/pmieconf/memory
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/memory/exhausted
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/memory/swap_low
%dir /var/lib/pcp/config/pmieconf/percpu
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/percpu/many_util
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/percpu/some_util
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/percpu/system
%dir /var/lib/pcp/config/pmieconf/pernetif
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/pernetif/collisions
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/pernetif/errors
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/pernetif/packets
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/pernetif/util
%dir /var/lib/pcp/config/pmieconf/shping
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/shping/response
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/shping/status
%dir /var/lib/pcp/config/pmlogconf
%dir /var/lib/pcp/config/pmlogconf/apache
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/apache/processes
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/apache/summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/apache/uptime
%dir /var/lib/pcp/config/pmlogconf/cpu
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/cpu/percpu
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/cpu/summary
%dir /var/lib/pcp/config/pmlogconf/disk
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/disk/percontroller
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/disk/perdisk
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/disk/summary
%dir /var/lib/pcp/config/pmlogconf/filesystem
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/xfs-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/xfs-io-irix
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/xfs-io-linux
%dir /var/lib/pcp/config/pmlogconf/kernel
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/bufcache-activity
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/bufcache-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/inode-cache
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/interrupts-irix
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/load
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/memory-irix
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/memory-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/queues-irix
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/read-write-data
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/summary-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/summary-windows
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/syscalls-irix
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/syscalls-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/syscalls-percpu-irix
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/vnodes
%dir /var/lib/pcp/config/pmlogconf/mailq
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/mailq/summary
%dir /var/lib/pcp/config/pmlogconf/memory
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/swap-activity
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/swap-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/swap-config
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/tlb-irix
%dir /var/lib/pcp/config/pmlogconf/mysql
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/mysql/summary
%dir /var/lib/pcp/config/pmlogconf/netfilter
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/netfilter/config
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/netfilter/summary
%dir /var/lib/pcp/config/pmlogconf/networking
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/interface-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/interface-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/mbufs
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/multicast
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs2-client
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs2-server
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs3-client
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs3-server
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/other-protocols
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/rpc
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/socket-irix
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/socket-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/streams
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/tcp-activity-irix
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/tcp-activity-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/tcp-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/udp-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/udp-packets-irix
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/udp-packets-linux
%dir /var/lib/pcp/config/pmlogconf/platform
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/platform/hinv
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/platform/linux
%dir /var/lib/pcp/config/pmlogconf/postgresql
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/postgresql/summary
%dir /var/lib/pcp/config/pmlogconf/sgi
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/cpu-evctr
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/craylink
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/efs
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/hub
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/kaio
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/node-memory
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/numa
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/numa-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/xbow
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/xlv-activity
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/xlv-stripe-io
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/xvm-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/xvm-ops
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sgi/xvm-stats
%dir /var/lib/pcp/config/pmlogconf/shping
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/shping/summary
%dir /var/lib/pcp/config/pmlogconf/sqlserver
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sqlserver/summary
%dir /var/lib/pcp/config/pmlogconf/v1.0
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/v1.0/C2
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/v1.0/C3
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/v1.0/D3
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/v1.0/K0
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/v1.0/S0
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/v1.0/S1
%dir /var/lib/pcp/config/pmlogconf/zimbra
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zimbra/all
%dir /var/lib/pcp/config/pmlogger
/var/lib/pcp/config/pmlogger/Makefile
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.*
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/control
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/crontab
%dir /var/lib/pcp/config/pmlogrewrite
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_proc_migrate.conf
%dir /var/lib/pcp/config/pmproxy
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmproxy/pmproxy.options
%dir /var/lib/pcp/pmdas
%dir /var/lib/pcp/pmdas/apache
%doc /var/lib/pcp/pmdas/apache/README
%attr(755,root,root) /var/lib/pcp/pmdas/apache/Install
%attr(755,root,root) /var/lib/pcp/pmdas/apache/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/apache/pmdaapache
/var/lib/pcp/pmdas/apache/domain.h
/var/lib/pcp/pmdas/apache/help
/var/lib/pcp/pmdas/apache/pmns
/var/lib/pcp/pmdas/apache/root
%dir /var/lib/pcp/pmdas/bash
%attr(755,root,root) /var/lib/pcp/pmdas/bash/Install
%attr(755,root,root) /var/lib/pcp/pmdas/bash/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/bash/pmdabash
/var/lib/pcp/pmdas/bash/domain.h
/var/lib/pcp/pmdas/bash/help
/var/lib/pcp/pmdas/bash/pmns
/var/lib/pcp/pmdas/bash/root
%dir /var/lib/pcp/pmdas/bonding
%attr(755,root,root) /var/lib/pcp/pmdas/bonding/Install
%attr(755,root,root) /var/lib/pcp/pmdas/bonding/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/bonding/pmdabonding.pl
%dir /var/lib/pcp/pmdas/cisco
%doc /var/lib/pcp/pmdas/cisco/README
%attr(755,root,root) /var/lib/pcp/pmdas/cisco/Install
%attr(755,root,root) /var/lib/pcp/pmdas/cisco/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/cisco/pmdacisco
%attr(755,root,root) /var/lib/pcp/pmdas/cisco/parse
%attr(755,root,root) /var/lib/pcp/pmdas/cisco/probe
/var/lib/pcp/pmdas/cisco/domain.h
/var/lib/pcp/pmdas/cisco/help
/var/lib/pcp/pmdas/cisco/pmns
/var/lib/pcp/pmdas/cisco/root
%dir /var/lib/pcp/pmdas/dbping
%attr(755,root,root) /var/lib/pcp/pmdas/dbping/Install
%attr(755,root,root) /var/lib/pcp/pmdas/dbping/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/dbping/dbprobe.pl
%attr(755,root,root) /var/lib/pcp/pmdas/dbping/pmdadbping.pl
%dir /var/lib/pcp/pmdas/elasticsearch
%attr(755,root,root) /var/lib/pcp/pmdas/elasticsearch/Install
%attr(755,root,root) /var/lib/pcp/pmdas/elasticsearch/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/elasticsearch/pmdaelasticsearch.pl
%dir /var/lib/pcp/pmdas/gpsd
%attr(755,root,root) /var/lib/pcp/pmdas/gpsd/Install
%attr(755,root,root) /var/lib/pcp/pmdas/gpsd/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/gpsd/pmdagpsd.pl
%dir /var/lib/pcp/pmdas/kvm
%attr(755,root,root) /var/lib/pcp/pmdas/kvm/Install
%attr(755,root,root) /var/lib/pcp/pmdas/kvm/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/kvm/pmdakvm.pl
%dir /var/lib/pcp/pmdas/linux
%attr(755,root,root) /var/lib/pcp/pmdas/linux/pmdalinux
%attr(755,root,root) /var/lib/pcp/pmdas/linux/pmda_linux.so
/var/lib/pcp/pmdas/linux/domain.h
/var/lib/pcp/pmdas/linux/help*
%dir /var/lib/pcp/pmdas/lmsensors
%doc /var/lib/pcp/pmdas/lmsensors/README
%attr(755,root,root) /var/lib/pcp/pmdas/lmsensors/Install
%attr(755,root,root) /var/lib/pcp/pmdas/lmsensors/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/lmsensors/pmdalmsensors
/var/lib/pcp/pmdas/lmsensors/domain.h
/var/lib/pcp/pmdas/lmsensors/help
/var/lib/pcp/pmdas/lmsensors/pmns
/var/lib/pcp/pmdas/lmsensors/root
%dir /var/lib/pcp/pmdas/logger
%doc /var/lib/pcp/pmdas/logger/README
%attr(755,root,root) /var/lib/pcp/pmdas/logger/Install
%attr(755,root,root) /var/lib/pcp/pmdas/logger/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/logger/pmdalogger
/var/lib/pcp/pmdas/logger/domain.h
/var/lib/pcp/pmdas/logger/help
/var/lib/pcp/pmdas/logger/pmns
/var/lib/pcp/pmdas/logger/root
%dir /var/lib/pcp/pmdas/lustrecomm
%doc /var/lib/pcp/pmdas/lustrecomm/README
%attr(755,root,root) /var/lib/pcp/pmdas/lustrecomm/Install
%attr(755,root,root) /var/lib/pcp/pmdas/lustrecomm/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/lustrecomm/pmdalustrecomm
/var/lib/pcp/pmdas/lustrecomm/domain.h
/var/lib/pcp/pmdas/lustrecomm/help
/var/lib/pcp/pmdas/lustrecomm/pmns
/var/lib/pcp/pmdas/lustrecomm/root
%dir /var/lib/pcp/pmdas/mailq
%doc /var/lib/pcp/pmdas/mailq/README
%attr(755,root,root) /var/lib/pcp/pmdas/mailq/Install
%attr(755,root,root) /var/lib/pcp/pmdas/mailq/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/mailq/pmdamailq
/var/lib/pcp/pmdas/mailq/domain.h
/var/lib/pcp/pmdas/mailq/help
/var/lib/pcp/pmdas/mailq/pmns
/var/lib/pcp/pmdas/mailq/root
%dir /var/lib/pcp/pmdas/memcache
%attr(755,root,root) /var/lib/pcp/pmdas/memcache/Install
%attr(755,root,root) /var/lib/pcp/pmdas/memcache/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/memcache/pmdamemcache.pl
%dir /var/lib/pcp/pmdas/mmv
%attr(755,root,root) /var/lib/pcp/pmdas/mmv/Install
%attr(755,root,root) /var/lib/pcp/pmdas/mmv/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/mmv/pmdammv
%attr(755,root,root) /var/lib/pcp/pmdas/mmv/pmda_mmv.so
%attr(755,root,root) /var/lib/pcp/pmdas/mmv/mmvdump
/var/lib/pcp/pmdas/mmv/domain.h
/var/lib/pcp/pmdas/mmv/root_mmv
%dir /var/lib/pcp/pmdas/mounts
%doc /var/lib/pcp/pmdas/mounts/README
%attr(755,root,root) /var/lib/pcp/pmdas/mounts/Install
%attr(755,root,root) /var/lib/pcp/pmdas/mounts/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/mounts/pmdamounts
/var/lib/pcp/pmdas/mounts/domain.h
/var/lib/pcp/pmdas/mounts/help
/var/lib/pcp/pmdas/mounts/pmns
/var/lib/pcp/pmdas/mounts/root
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/mounts/mounts.conf
%dir /var/lib/pcp/pmdas/mysql
%attr(755,root,root) /var/lib/pcp/pmdas/mysql/Install
%attr(755,root,root) /var/lib/pcp/pmdas/mysql/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/mysql/pmdamysql.pl
%dir /var/lib/pcp/pmdas/named
%attr(755,root,root) /var/lib/pcp/pmdas/named/Install
%attr(755,root,root) /var/lib/pcp/pmdas/named/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/named/pmdanamed.pl
%dir /var/lib/pcp/pmdas/netfilter
%attr(755,root,root) /var/lib/pcp/pmdas/netfilter/Install
%attr(755,root,root) /var/lib/pcp/pmdas/netfilter/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/netfilter/pmdanetfilter.pl
%dir /var/lib/pcp/pmdas/news
%doc /var/lib/pcp/pmdas/news/README
%attr(755,root,root) /var/lib/pcp/pmdas/news/Install
%attr(755,root,root) /var/lib/pcp/pmdas/news/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/news/pmdanews.pl
/var/lib/pcp/pmdas/news/active
%dir /var/lib/pcp/pmdas/pdns
%attr(755,root,root) /var/lib/pcp/pmdas/pdns/Install
%attr(755,root,root) /var/lib/pcp/pmdas/pdns/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/pdns/pmdapdns.pl
%dir /var/lib/pcp/pmdas/pmcd
%attr(755,root,root) /var/lib/pcp/pmdas/pmcd/pmda_pmcd.so
/var/lib/pcp/pmdas/pmcd/help.*
%dir /var/lib/pcp/pmdas/postfix
%attr(755,root,root) /var/lib/pcp/pmdas/postfix/Install
%attr(755,root,root) /var/lib/pcp/pmdas/postfix/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/postfix/pmdapostfix.pl
%dir /var/lib/pcp/pmdas/postgresql
%attr(755,root,root) /var/lib/pcp/pmdas/postgresql/Install
%attr(755,root,root) /var/lib/pcp/pmdas/postgresql/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/postgresql/pmdapostgresql.pl
%dir /var/lib/pcp/pmdas/proc
%attr(755,root,root) /var/lib/pcp/pmdas/proc/Install
%attr(755,root,root) /var/lib/pcp/pmdas/proc/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/proc/pmdaproc
%attr(755,root,root) /var/lib/pcp/pmdas/proc/pmda_proc.so
/var/lib/pcp/pmdas/proc/domain.h
/var/lib/pcp/pmdas/proc/help
/var/lib/pcp/pmdas/proc/pmns
/var/lib/pcp/pmdas/proc/pmns.cgroup
/var/lib/pcp/pmdas/proc/root
%dir /var/lib/pcp/pmdas/process
%doc /var/lib/pcp/pmdas/process/README
%attr(755,root,root) /var/lib/pcp/pmdas/process/Install
%attr(755,root,root) /var/lib/pcp/pmdas/process/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/process/pmdaprocess
/var/lib/pcp/pmdas/process/domain.h
/var/lib/pcp/pmdas/process/help
/var/lib/pcp/pmdas/process/pmns
/var/lib/pcp/pmdas/process/root
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/process/process.conf
%dir /var/lib/pcp/pmdas/roomtemp
%doc /var/lib/pcp/pmdas/roomtemp/README
%attr(755,root,root) /var/lib/pcp/pmdas/roomtemp/Install
%attr(755,root,root) /var/lib/pcp/pmdas/roomtemp/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/roomtemp/pmdaroomtemp
/var/lib/pcp/pmdas/roomtemp/domain.h
/var/lib/pcp/pmdas/roomtemp/help
/var/lib/pcp/pmdas/roomtemp/pmns
/var/lib/pcp/pmdas/roomtemp/root
%dir /var/lib/pcp/pmdas/rsyslog
%attr(755,root,root) /var/lib/pcp/pmdas/rsyslog/Install
%attr(755,root,root) /var/lib/pcp/pmdas/rsyslog/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/rsyslog/pmdarsyslog.pl
%dir /var/lib/pcp/pmdas/samba
%attr(755,root,root) /var/lib/pcp/pmdas/samba/Install
%attr(755,root,root) /var/lib/pcp/pmdas/samba/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/samba/pmdasamba.pl
%dir /var/lib/pcp/pmdas/sample
%doc /var/lib/pcp/pmdas/sample/README
%attr(755,root,root) /var/lib/pcp/pmdas/sample/Install
%attr(755,root,root) /var/lib/pcp/pmdas/sample/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/sample/pmdasample
%attr(755,root,root) /var/lib/pcp/pmdas/sample/pmda_sample.so
/var/lib/pcp/pmdas/sample/domain.h
/var/lib/pcp/pmdas/sample/help
/var/lib/pcp/pmdas/sample/pmns
/var/lib/pcp/pmdas/sample/root
%dir /var/lib/pcp/pmdas/sendmail
%doc /var/lib/pcp/pmdas/sendmail/README
%attr(755,root,root) /var/lib/pcp/pmdas/sendmail/Install
%attr(755,root,root) /var/lib/pcp/pmdas/sendmail/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/sendmail/pmdasendmail
%attr(755,root,root) /var/lib/pcp/pmdas/sendmail/pmda_sendmail.so
/var/lib/pcp/pmdas/sendmail/domain.h
/var/lib/pcp/pmdas/sendmail/help
/var/lib/pcp/pmdas/sendmail/pmns
/var/lib/pcp/pmdas/sendmail/root
%dir /var/lib/pcp/pmdas/shping
%doc /var/lib/pcp/pmdas/shping/README
%attr(755,root,root) /var/lib/pcp/pmdas/shping/Install
%attr(755,root,root) /var/lib/pcp/pmdas/shping/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/shping/pmdashping
/var/lib/pcp/pmdas/shping/domain.h
/var/lib/pcp/pmdas/shping/help
/var/lib/pcp/pmdas/shping/pmns
/var/lib/pcp/pmdas/shping/root
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/shping/sample.conf
%dir /var/lib/pcp/pmdas/simple
%doc /var/lib/pcp/pmdas/simple/README
%attr(755,root,root) /var/lib/pcp/pmdas/simple/Install
%attr(755,root,root) /var/lib/pcp/pmdas/simple/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/simple/pmdasimple.pl
/var/lib/pcp/pmdas/simple/domain.h
/var/lib/pcp/pmdas/simple/help
/var/lib/pcp/pmdas/simple/pmns
/var/lib/pcp/pmdas/simple/root
/var/lib/pcp/pmdas/simple/Makefile
/var/lib/pcp/pmdas/simple/simple.c
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/simple/simple.conf
%dir /var/lib/pcp/pmdas/snmp
%attr(755,root,root) /var/lib/pcp/pmdas/snmp/Install
%attr(755,root,root) /var/lib/pcp/pmdas/snmp/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/snmp/pmdasnmp.pl
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/snmp/snmp.conf
%dir /var/lib/pcp/pmdas/summary
%doc /var/lib/pcp/pmdas/summary/README
%attr(755,root,root) /var/lib/pcp/pmdas/summary/Install
%attr(755,root,root) /var/lib/pcp/pmdas/summary/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/summary/pmdasummary
/var/lib/pcp/pmdas/summary/domain.h
/var/lib/pcp/pmdas/summary/help
/var/lib/pcp/pmdas/summary/pmns
/var/lib/pcp/pmdas/summary/root
/var/lib/pcp/pmdas/summary/expr.pmie
%dir /var/lib/pcp/pmdas/systemtap
%attr(755,root,root) /var/lib/pcp/pmdas/systemtap/Install
%attr(755,root,root) /var/lib/pcp/pmdas/systemtap/Remove
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/systemtap/pmdasystemtap.pl
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/systemtap/probes.stp
%dir /var/lib/pcp/pmdas/trace
%doc /var/lib/pcp/pmdas/trace/README
%attr(755,root,root) /var/lib/pcp/pmdas/trace/Install
%attr(755,root,root) /var/lib/pcp/pmdas/trace/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/trace/pmdatrace
/var/lib/pcp/pmdas/trace/domain.h
/var/lib/pcp/pmdas/trace/help
/var/lib/pcp/pmdas/trace/pmns
/var/lib/pcp/pmdas/trace/root
%dir /var/lib/pcp/pmdas/trivial
%doc /var/lib/pcp/pmdas/trivial/README
%attr(755,root,root) /var/lib/pcp/pmdas/trivial/Install
%attr(755,root,root) /var/lib/pcp/pmdas/trivial/Remove
/var/lib/pcp/pmdas/trivial/domain.h
/var/lib/pcp/pmdas/trivial/help
/var/lib/pcp/pmdas/trivial/pmns
/var/lib/pcp/pmdas/trivial/root
/var/lib/pcp/pmdas/trivial/Makefile
/var/lib/pcp/pmdas/trivial/trivial.c
%dir /var/lib/pcp/pmdas/txmon
%doc /var/lib/pcp/pmdas/txmon/README
%attr(755,root,root) /var/lib/pcp/pmdas/txmon/Install
%attr(755,root,root) /var/lib/pcp/pmdas/txmon/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/txmon/pmdatxmon
%attr(755,root,root) /var/lib/pcp/pmdas/txmon/genload
%attr(755,root,root) /var/lib/pcp/pmdas/txmon/txrecord
/var/lib/pcp/pmdas/txmon/domain.h
/var/lib/pcp/pmdas/txmon/help
/var/lib/pcp/pmdas/txmon/pmns
/var/lib/pcp/pmdas/txmon/root
/var/lib/pcp/pmdas/txmon/Makefile
/var/lib/pcp/pmdas/txmon/txmon.c
/var/lib/pcp/pmdas/txmon/txmon.h
/var/lib/pcp/pmdas/txmon/txrecord.c
%dir /var/lib/pcp/pmdas/vmware
%attr(755,root,root) /var/lib/pcp/pmdas/vmware/Install
%attr(755,root,root) /var/lib/pcp/pmdas/vmware/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/vmware/pmdavmware.pl
%dir /var/lib/pcp/pmdas/weblog
%doc /var/lib/pcp/pmdas/weblog/README
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/Install
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/pmdaweblog
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/check_match
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/server.sh
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/weblogconv.sh
/var/lib/pcp/pmdas/weblog/domain.h
/var/lib/pcp/pmdas/weblog/help
/var/lib/pcp/pmdas/weblog/pmns
/var/lib/pcp/pmdas/weblog/root
%dir /var/lib/pcp/pmdas/zimbra
%attr(755,root,root) /var/lib/pcp/pmdas/zimbra/Install
%attr(755,root,root) /var/lib/pcp/pmdas/zimbra/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/zimbra/pmdazimbra.pl
%attr(755,root,root) /var/lib/pcp/pmdas/zimbra/zimbraprobe
%{_mandir}/man1/PCPIntro.1*
%{_mandir}/man1/autofsd-probe.1*
%{_mandir}/man1/chkhelp.1*
%{_mandir}/man1/dbpmda.1*
%{_mandir}/man1/dbprobe.1*
%{_mandir}/man1/genpmda.1*
%{_mandir}/man1/iostat2pcp.1*
%{_mandir}/man1/mkaf.1*
%{_mandir}/man1/mrtg2pcp.1*
%{_mandir}/man1/pcp.1*
%{_mandir}/man1/pmafm.1*
%{_mandir}/man1/pmcd.1*
%{_mandir}/man1/pmcd_wait.1*
%{_mandir}/man1/pmclient.1*
%{_mandir}/man1/pmcollectl.1*
%{_mandir}/man1/pmconfig.1*
%{_mandir}/man1/pmdabash.1*
%{_mandir}/man1/pmdabonding.1*
%{_mandir}/man1/pmdacisco.1*
%{_mandir}/man1/pmdadbping.1*
%{_mandir}/man1/pmdaelasticsearch.1*
%{_mandir}/man1/pmdagpsd.1*
%{_mandir}/man1/pmdakvm.1*
%{_mandir}/man1/pmdamailq.1*
%{_mandir}/man1/pmdamemcache.1*
%{_mandir}/man1/pmdamysql.1*
%{_mandir}/man1/pmdanamed.1*
%{_mandir}/man1/pmdanetfilter.1*
%{_mandir}/man1/pmdanews.1*
%{_mandir}/man1/pmdapdns.1*
%{_mandir}/man1/pmdapostfix.1*
%{_mandir}/man1/pmdapostgresql.1*
%{_mandir}/man1/pmdarsyslog.1*
%{_mandir}/man1/pmdasamba.1*
%{_mandir}/man1/pmdasample.1*
%{_mandir}/man1/pmdasendmail.1*
%{_mandir}/man1/pmdashping.1*
%{_mandir}/man1/pmdasimple.1*
%{_mandir}/man1/pmdasnmp.1*
%{_mandir}/man1/pmdasummary.1*
%{_mandir}/man1/pmdasystemtap.1*
%{_mandir}/man1/pmdate.1*
%{_mandir}/man1/pmdatrace.1*
%{_mandir}/man1/pmdatrivial.1*
%{_mandir}/man1/pmdatxmon.1*
%{_mandir}/man1/pmdavmware.1*
%{_mandir}/man1/pmdaweblog.1*
%{_mandir}/man1/pmdazimbra.1*
%{_mandir}/man1/pmdbg.1*
%{_mandir}/man1/pmdumplog.1*
%{_mandir}/man1/pmerr.1*
%{_mandir}/man1/pmevent.1*
%{_mandir}/man1/pmgenmap.1*
%{_mandir}/man1/pmhostname.1*
%{_mandir}/man1/pmie.1*
%{_mandir}/man1/pmie2col.1*
%{_mandir}/man1/pmie_check.1*
%{_mandir}/man1/pmie_daily.1*
%{_mandir}/man1/pmieconf.1*
%{_mandir}/man1/pmiestatus.1*
%{_mandir}/man1/pminfo.1*
%{_mandir}/man1/pmlc.1*
%{_mandir}/man1/pmlock.1*
%{_mandir}/man1/pmlogcheck.1*
%{_mandir}/man1/pmlogconf.1*
%{_mandir}/man1/pmlogextract.1*
%{_mandir}/man1/pmlogger.1*
%{_mandir}/man1/pmlogger_check.1*
%{_mandir}/man1/pmlogger_daily.1*
%{_mandir}/man1/pmlogger_merge.1*
%{_mandir}/man1/pmloglabel.1*
%{_mandir}/man1/pmlogreduce.1*
%{_mandir}/man1/pmlogrewrite.1*
%{_mandir}/man1/pmlogsummary.1*
%{_mandir}/man1/pmnewlog.1*
%{_mandir}/man1/pmnsadd.1*
%{_mandir}/man1/pmnsdel.1*
%{_mandir}/man1/pmnsmerge.1*
%{_mandir}/man1/pmpost.1*
%{_mandir}/man1/pmprobe.1*
%{_mandir}/man1/pmproxy.1*
%{_mandir}/man1/pmsignal.1*
%{_mandir}/man1/pmsleep.1*
%{_mandir}/man1/pmsocks.1*
%{_mandir}/man1/pmstat.1*
%{_mandir}/man1/pmstore.1*
%{_mandir}/man1/pmtrace.1*
%{_mandir}/man1/pmval.1*
%{_mandir}/man1/sar2pcp.1*
%{_mandir}/man1/sheet2pcp.1*
%{_mandir}/man1/telnet-probe.1*

%files libs
%defattr(644,root,root,755)
# NOTE: some of them are compatibility symlinks; regular files are SONAMEs directly
%attr(755,root,root) %{_libdir}/libpcp.so.2
%attr(755,root,root) %{_libdir}/libpcp.so.3
%attr(755,root,root) %{_libdir}/libpcp_gui.so.1
%attr(755,root,root) %{_libdir}/libpcp_gui.so.2
%attr(755,root,root) %{_libdir}/libpcp_import.so.1
%attr(755,root,root) %{_libdir}/libpcp_mmv.so.1
%attr(755,root,root) %{_libdir}/libpcp_pmda.so.2
%attr(755,root,root) %{_libdir}/libpcp_pmda.so.3
%attr(755,root,root) %{_libdir}/libpcp_trace.so.2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp.conf
%{_sysconfdir}/pcp.env
%{_mandir}/man1/newhelp.1*
%{_mandir}/man1/pmcpp.1*
%{_mandir}/man4/mmv.4*
%{_mandir}/man4/pcp.conf.4*
%{_mandir}/man4/pcp.env.4*
%{_mandir}/man4/pmieconf.4*
%{_mandir}/man4/pmns.4*
%dir %{_libdir}/pcp
%dir %{_libdir}/pcp/bin
%attr(755,root,root) %{_libdir}/pcp/bin/newhelp
%attr(755,root,root) %{_libdir}/pcp/bin/pmcpp
%dir /var/lib/pcp
%dir /var/lib/pcp/pmns
%config(missingok) /var/lib/pcp/pmns/.NeedRebuild
%attr(755,root,root) /var/lib/pcp/pmns/Make.stdpmid
%attr(755,root,root) /var/lib/pcp/pmns/Rebuild
/var/lib/pcp/pmns/Makefile
/var/lib/pcp/pmns/root_linux
/var/lib/pcp/pmns/root_mmv
/var/lib/pcp/pmns/root_pmcd
/var/lib/pcp/pmns/stdpmid.pcp
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmns/stdpmid.local
%ghost /var/lib/pcp/pmns/stdpmid

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpcp.so
%attr(755,root,root) %{_libdir}/libpcp_gui.so
%attr(755,root,root) %{_libdir}/libpcp_import.so
%attr(755,root,root) %{_libdir}/libpcp_mmv.so
%attr(755,root,root) %{_libdir}/libpcp_pmda.so
%attr(755,root,root) %{_libdir}/libpcp_trace.so
%{_includedir}/pcp
%{_mandir}/man3/LOGIMPORT.3*
%{_mandir}/man3/PCPIntro.3*
%{_mandir}/man3/PMAPI.3*
%{_mandir}/man3/PMDA.3*
%{_mandir}/man3/__pm*.3*
%{_mandir}/man3/mmv_*.3*
%{_mandir}/man3/pm*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libpcp.a
%{_libdir}/libpcp_gui.a
%{_libdir}/libpcp_import.a
%{_libdir}/libpcp_mmv.a
%{_libdir}/libpcp_pmda.a
%{_libdir}/libpcp_trace.a

%files -n perl-pcp
%defattr(644,root,root,755)
%dir %{perl_vendorarch}/PCP
%{perl_vendorarch}/PCP/LogImport.pm
%{perl_vendorarch}/PCP/MMV.pm
%{perl_vendorarch}/PCP/PMDA.pm
%attr(755,root,root) %{perl_vendorarch}/PCP/server.pl
%dir %{perl_vendorarch}/auto/PCP
%dir %{perl_vendorarch}/auto/PCP/LogImport
%attr(755,root,root) %{perl_vendorarch}/auto/PCP/LogImport/LogImport.so
%dir %{perl_vendorarch}/auto/PCP/LogSummary
%dir %{perl_vendorarch}/auto/PCP/MMV
%attr(755,root,root) %{perl_vendorarch}/auto/PCP/MMV/MMV.so
%dir %{perl_vendorarch}/auto/PCP/PMDA
%attr(755,root,root) %{perl_vendorarch}/auto/PCP/PMDA/PMDA.so
%dir %{perl_vendorlib}/PCP
%{perl_vendorlib}/PCP/LogSummary.pm
%{perl_vendorlib}/PCP/exceldemo.pl
%attr(755,root,root) %{perl_vendorlib}/PCP/extract.pl
%{_mandir}/man3/PCP::LogImport.3pm*
%{_mandir}/man3/PCP::LogSummary.3pm*
%{_mandir}/man3/PCP::MMV.3pm*
%{_mandir}/man3/PCP::PMDA.3pm*

%files -n python-pcp
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pmapi.so
%{py_sitedir}/pcp.py[co]
%{py_sitedir}/pcpi.py[co]
%{py_sitedir}/pcp-0.2-py*.egg-info

%files -n bash-completion-pcp
%defattr(644,root,root,755)
/etc/bash_completion.d/pcp
