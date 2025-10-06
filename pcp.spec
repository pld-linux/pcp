# TODO:
# - PLDify init scripts
# - /var/lib/pcp looks like mess, configs/variable data/scripts/ELFs (successively resolved upstream)
# NOTE: user/group must be in -libs because of /var/run/pcp, needed for Make.stdpmid in post
# - package zabbix agent
#
# Conditional build:
%bcond_without	qt		# Qt 5.x based GUI
%bcond_without	systemtap	# systemtap/dtrace support

Summary:	Performance Co-Pilot - system level performance monitoring and management
Summary(pl.UTF-8):	Performance Co-Pilot - monitorowanie i zarządzanie wydajnością na poziomie systemu
Name:		pcp
Version:	6.3.7
Release:	1
License:	LGPL v2.1 (libraries), GPL v2 (the rest)
Group:		Applications/System
Source0:	https://github.com/performancecopilot/pcp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	71723b3969ddbf5bc937e9394b4db2b3
Patch0:		build-man.patch
Patch1:		%{name}-opt.patch
Patch3:		%{name}-saslconfdir.patch
Patch5:		python-install.patch
Patch6:		install-icons.patch
Patch7:		no-perl-time-check.patch
URL:		https://pcp.io/
BuildRequires:	HdrHistogram_c-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	avahi-devel
BuildRequires:	bison
# for bpftrace PMDA
#BuildRequires:	bpftrace	# bpftrace.org, github.com/bpftrace/bpftrace
# for bpf PMDA
#BuildRequires:	clang >= 10
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	device-mapper-devel
BuildRequires:	elfutils-devel
BuildRequires:	flex
BuildRequires:	inih-devel
%ifarch i386
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libbpf-devel >= 1.0.0
#BuildRequires:	libchan-devel	# github.com/tylertreat/chan, for statsd PMDA
BuildRequires:	libdrm-devel >= 2.4.77
BuildRequires:	libibmad-devel
BuildRequires:	libibumad-devel
BuildRequires:	libmicrohttpd-devel >= 0.9.10
BuildRequires:	libpfm-devel
BuildRequires:	libuv-devel >= 1
BuildRequires:	ncurses-devel
BuildRequires:	nspr-devel >= 4
BuildRequires:	nss-devel >= 3
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	perl-DBD-Pg
BuildRequires:	perl-DBD-mysql
BuildRequires:	perl-DBI
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-File-Slurp
BuildRequires:	perl-JSON
BuildRequires:	perl-Net-SNMP
BuildRequires:	perl-XML-LibXML
BuildRequires:	perl-YAML-LibYAML
BuildRequires:	perl-base
BuildRequires:	perl-libwww
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
#BuildRequires:	postfix-qshape /usr/share/doc/packages/postfix-doc/auxiliary/qshape/qshape.pl for postfix PMDA
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-jsonpointer
BuildRequires:	python3-psycopg2
BuildRequires:	python3-six
#TODO
#BuildRequires:	python3-bpfcc		# github.com/iovisor/bcc, for bcc PMDA
#BuildRequires:	python3-libvirt		# for libvirt PMDA
#BuildRequires:	python3-lxml		# for libvirt PMDA
#BuildRequires:	python3-openpyxl	# for ?
#BuildRequires:	python3-pyarrow		# for ?
#BuildRequires:	python3-pymongo		# for mongodb PMDA
#BuildRequires:	python3-pyodbc		# for mssql PMDA
#BuildRequires:	python3-requests	# for influxdb
#BuildRequires:	python3-rtslib		# for LIO PMDA
#BuildRequires:	python3-setuptools	# for ?
BuildRequires:	readline-devel
BuildRequires:	rpm-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	systemd-devel >= 1:239
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	xz-devel
BuildRequires:	zfs-devel
BuildRequires:	zlib-devel >= 1.0.0
%if %{with qt}
# or qt6 6.0+, but must be consistent with SoQt
BuildRequires:	Qt5Concurrent-devel >= 5.6
BuildRequires:	Qt5Core-devel >= 5.6
BuildRequires:	Qt5Gui-devel >= 5.6
BuildRequires:	Qt5Network-devel >= 5.6
BuildRequires:	Qt5PrintSupport-devel >= 5.6
BuildRequires:	Qt5Svg-devel >= 5.6
BuildRequires:	SoQt-devel
BuildRequires:	qt5-build >= 5.6
BuildRequires:	qt5-qmake >= 5.6
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libmicrohttpd >= 0.9.10
Requires:	perl-pcp = %{version}-%{release}
Requires:	python-pcp = %{version}-%{release}
Requires:	systemd-units >= 1:239
Suggests:	crondaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Performance Co-Pilot (PCP) is a framework and services to support
system-level performance monitoring and performance management.

The Performance Co-Pilot provides a unifying abstraction for all of
the interesting performance data in a system, and allows client
applications to easily retrieve and process any subset of that data.

%description -l pl.UTF-8
PCP (Performance Co-Pilot) to szkielet i usługi mające na celu obsługę
monitorowania wydajności i zarządzania wydajnością.

PCP udostępnia ujednoliconą abstrakcję dla wszystkich interesujących
danych związanych z wydajnością w systemie i pozwala aplikacjom
klienckim łatwo odczytywać i przetwarzać dowolny podzbiór tych danych.

%package gui
Summary:	Performance Co-Pilot GUI tools
Summary(pl.UTF-8):	Performance Co-Pilot - narzędzia GUI
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gui
pmchart is designed to produce stripcharts from Performance Co-Pilot
(PCP) performance metrics fetched from live sources (one or more pmcd
hosts) and also historical sources (one or more PCP archives).

pmtime is a graphical time controller utility that coordinates time
updates and VCR-like playback for other utilities like pmchart and
pmval.

%description gui -l pl.UTF-8
pmchart służy do tworzenia wykresów z danych o wydajności pakietu PCP
(Performance Co-Pilot) pobranych z żywych źródeł (jednego lub większej
liczby hostów pmcd) oraz źródeł historycznych (jednego lub większej
liczby archiwów PCP).

pmtime to graficzne narzędzie do kontroli czasu, koordynujące
aktualizację czasu oraz odtwarzanie w stylu VCR dla innych narzędzi,
takich jak pmchart czy pmval.

%package libs
Summary:	PCP libraries
Summary(pl.UTF-8):	Biblioteki PCP
Group:		Libraries
Requires(post):	/usr/bin/gawk
Requires(post,postun):	/sbin/ldconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(pcp)
Provides:	user(pcp)

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
Summary:	Python 2 interface to PCP libraries
Summary(pl.UTF-8):	Interfejs Pythona 2 do bibliotek PCP
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-pcp
Python 2 interface to PCP libraries.

%description -n python-pcp -l pl.UTF-8
Interfejs Pythona 2 do bibliotek PCP.

%package -n python3-pcp
Summary:	Python 3 interface to PCP libraries
Summary(pl.UTF-8):	Interfejs Pythona 3 do bibliotek PCP
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python3-pcp
Python 3 interface to PCP libraries.

%description -n python3-pcp -l pl.UTF-8
Interfejs Pythona 3 do bibliotek PCP.

%package -n bash-completion-pcp
Summary:	bash-completion for PCP utilities
Summary(pl.UTF-8):	Bashowe uzupełnianie nazw dla narzędzi PCP
Group:		Applications/Shells
Requires:	bash-completion
BuildArch:	noarch

%description -n bash-completion-pcp
bash-completion for PCP utilities.

%description -n bash-completion-pcp -l pl.UTF-8
Bashowe uzupełnianie nazw dla narzędzi PCP.

%package -n systemtap-pcp
Summary:	systemtap/dtrace probes for PCP
Summary(pl.UTF-8):	Sondy systemtap/dtrace dla PCP
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	systemtap-client

%description -n systemtap-pcp
systemtap/dtrace probes for PCP.

%description -n systemtap-pcp -l pl.UTF-8
Sondy systemtap/dtrace dla PCP.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 3 -p1
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+perl(\s|$),#!%{__perl}\1,' \
      src/ganglia2pcp/ganglia2pcp \
      src/iostat2pcp/iostat2pcp \
      src/mrtg2pcp/mrtg2pcp \
      src/perl/LogSummary/extract.pl \
      src/perl/MMV/server.pl \
      src/pmdas/oracle/connect.pl \
      src/pmdas/redis/pmdaredis.pl \
      src/pmdas/simple/pmdasimple.perl \
      src/sar2pcp/sar2pcp \
      src/sheet2pcp/sheet2pcp \
      src/pmdas/perfevent/perfevent-makerewrite.pl

find \( -name '*.py' -o -name '*.python' \) -print0 | xargs -0 \
      %{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+pmpython(\s|$),#!%{_bindir}/pmpython\1,'

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+pmpython(\s|$),#!%{_bindir}/pmpython\1,' \
      src/pmdas/haproxy/connect \
      src/pmdas/json/generate_ceph_metadata \
      src/pmdas/libvirt/connect \
      src/pmdas/netcheck/pyprep

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+bash(\s|$),#!/bin/bash\1,' \
      src/pmdas/bash/test-child.sh \
      src/pmdas/bash/test-trace.sh

%build
%{__autoconf}
%configure \
	QMAKE=/usr/bin/qmake-qt5 \
	--with-qt%{!?with_qt:=no} \
	--with-static-probes%{!?with_systemtap:=no} \
	--with-python_prefix=%{_prefix} \
	--with-rcdir=/etc/rc.d/init.d \
	--with-rundir=/run/pcp

# ensure not *zipping man pages on install
%{__sed} -i -e '/^HAVE_.*ED_MANPAGES/s,true,false,' src/include/builddefs

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DIST_ROOT=$RPM_BUILD_ROOT \
	BASHDIR=/etc/bash_completion.d/pcp \
	INSTALL='$(INSTALL_SH)' \
	HAVE_BZIP2ED_MANPAGES=false \
	HAVE_GZIPPED_MANPAGES=false \
	HAVE_LZMAED_MANPAGES=false \
	HAVE_XZED_MANPAGES=false

install -p src/pmns/stdpmid $RPM_BUILD_ROOT/var/lib/pcp/pmns

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

# kill man pages specific to other OSs (note: pmdaaix.1 is installed as actual man source)
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/{pmdaaix,pmdakernel}.1
ln -snf pmdakernel.1 $RPM_BUILD_ROOT%{_mandir}/man1/pmdalinux.1
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{pmdadarwin,pmdafreebsd,pmdanetbsd,pmdasolaris,pmdawindows}.1
# already present as pcp-dstat.1 and conflicts with dstat package
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/dstat.1*
# could be eventually packaged in examplesdir / docdir resp.
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/pcp/{demos,examples}
# tests (package in -testsuite using pcpqa:pcpqa UID/GID?)
%{__rm} -r $RPM_BUILD_ROOT/var/lib/pcp/testsuite
%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/sysusers.d/pcp-testsuite.conf
# packaged as %doc
%{__rm} -rf html
%{__mv} $RPM_BUILD_ROOT%{_docdir}/pcp-doc/html html
# some files packaged as %doc, the rest useless in package
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-{%{version},doc}

%clean
rm -rf $RPM_BUILD_ROOT

%pre libs
%groupadd -g 308 pcp
%useradd -u 308 -d /var/lib/pcp -g pcp -s /bin/false -c "Performance Co-Pilot user" pcp

%post	libs
/sbin/ldconfig
cd /var/lib/pcp/pmns
umask 022
PCP_DIR= PCP_TMP_DIR=/tmp ./Make.stdpmid

%postun	libs
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove pcp
	%groupremove pcp
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README.md
%attr(755,root,root) %{_bindir}/collectl2pcp
%attr(755,root,root) %{_bindir}/dbpmda
%attr(755,root,root) %{_bindir}/dstat
%attr(755,root,root) %{_bindir}/ganglia2pcp
%attr(755,root,root) %{_bindir}/genpmda
%attr(755,root,root) %{_bindir}/iostat2pcp
%attr(755,root,root) %{_bindir}/mrtg2pcp
%attr(755,root,root) %{_bindir}/pcp
%attr(755,root,root) %{_bindir}/pcp2csv
%attr(755,root,root) %{_bindir}/pcp2elasticsearch
%attr(755,root,root) %{_bindir}/pcp2graphite
%attr(755,root,root) %{_bindir}/pcp2influxdb
%attr(755,root,root) %{_bindir}/pcp2json
%attr(755,root,root) %{_bindir}/pcp2openmetrics
%attr(755,root,root) %{_bindir}/pcp2spark
%attr(755,root,root) %{_bindir}/pcp2xml
%attr(755,root,root) %{_bindir}/pcp2zabbix
%attr(755,root,root) %{_bindir}/pmafm
%attr(755,root,root) %{_bindir}/pmclient
%attr(755,root,root) %{_bindir}/pmclient_fg
%attr(755,root,root) %{_bindir}/pmdate
%attr(755,root,root) %{_bindir}/pmdbg
%attr(755,root,root) %{_bindir}/pmdiff
%attr(755,root,root) %{_bindir}/pmdumplog
%attr(755,root,root) %{_bindir}/pmerr
%attr(755,root,root) %{_bindir}/pmevent
%attr(755,root,root) %{_bindir}/pmfind
%attr(755,root,root) %{_bindir}/pmgenmap
%attr(755,root,root) %{_bindir}/pmie
%attr(755,root,root) %{_bindir}/pmie2col
%attr(755,root,root) %{_bindir}/pmieconf
%attr(755,root,root) %{_bindir}/pmiectl
%attr(755,root,root) %{_bindir}/pmiostat
%attr(755,root,root) %{_bindir}/pmjson
%attr(755,root,root) %{_bindir}/pmlc
%attr(755,root,root) %{_bindir}/pmlogbasename
%attr(755,root,root) %{_bindir}/pmlogcheck
%attr(755,root,root) %{_bindir}/pmlogcompress
%attr(755,root,root) %{_bindir}/pmlogconf
%attr(755,root,root) %{_bindir}/pmlogctl
%attr(755,root,root) %{_bindir}/pmlogdump
%attr(755,root,root) %{_bindir}/pmlogextract
%attr(755,root,root) %{_bindir}/pmlogger
%attr(755,root,root) %{_bindir}/pmloglabel
%attr(755,root,root) %{_bindir}/pmlogmv
%attr(755,root,root) %{_bindir}/pmlogpaste
%attr(755,root,root) %{_bindir}/pmlogredact
%attr(755,root,root) %{_bindir}/pmlogreduce
%attr(755,root,root) %{_bindir}/pmlogrewrite
%attr(755,root,root) %{_bindir}/pmlogsize
%attr(755,root,root) %{_bindir}/pmlogsummary
%attr(755,root,root) %{_bindir}/pmprobe
%attr(755,root,root) %{_bindir}/pmpython
%attr(755,root,root) %{_bindir}/pmrep
%attr(755,root,root) %{_bindir}/pmrepconf
%attr(755,root,root) %{_bindir}/pmsearch
%attr(755,root,root) %{_bindir}/pmseries
%attr(755,root,root) %{_bindir}/pmsocks
%attr(755,root,root) %{_bindir}/pmstat
%attr(755,root,root) %{_bindir}/pmstore
%attr(755,root,root) %{_bindir}/pmtrace
%attr(755,root,root) %{_bindir}/pmval
%attr(755,root,root) %{_bindir}/sar2pcp
%attr(755,root,root) %{_bindir}/sheet2pcp
%dir %{_libexecdir}/pcp/bin/discover
%attr(755,root,root) %{_libexecdir}/pcp/bin/discover/pcp-kube-pods
%attr(755,root,root) %{_libexecdir}/pcp/bin/chkhelp
%attr(755,root,root) %{_libexecdir}/pcp/bin/find-filter
%attr(755,root,root) %{_libexecdir}/pcp/bin/indomcachectl
%attr(755,root,root) %{_libexecdir}/pcp/bin/install-sh
%attr(755,root,root) %{_libexecdir}/pcp/bin/mkaf
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-atop
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-atopsar
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-buddyinfo
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-check
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-dmcache
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-dstat
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-free
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-geolocate
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-htop
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-iostat
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-ipcs
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-lvmcache
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-meminfo
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-mpstat
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-netstat
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-numastat
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-pidstat
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-ps
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-python
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-reboot-init
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-shping
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-slabinfo
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-ss
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-summary
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-tapestat
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-uptime
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-verify
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-vmstat
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-xsos
%attr(755,root,root) %{_libexecdir}/pcp/bin/pcp-zoneinfo
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmcd
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmcd_wait
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmcheck
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmconfig
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmfind_check
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmgetopt
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmhostname
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmie_check
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmie_daily
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmie_dump_stats
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmie_email
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmie_farm
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmie_webhook
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmiestatus
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlock
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogconf
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogextract
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogger
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogger_check
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogger_daily
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogger_daily_report
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogger_farm
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogger_janitor
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogger_merge
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogredact
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogreduce
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogrewrite
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmnewlog
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmnsadd
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmnsdel
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmpause
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmpost
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmproxy
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmsignal
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmsleep
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmwtf
%attr(755,root,root) %{_libexecdir}/pcp/bin/runaspcp
%attr(755,root,root) %{_libexecdir}/pcp/bin/telnet-probe
%dir %{_libexecdir}/pcp/lib
%{_libexecdir}/pcp/lib/bashproc.sh
%{_libexecdir}/pcp/lib/checkproc.sh
%{_libexecdir}/pcp/lib/pmdaproc.sh
%{_libexecdir}/pcp/lib/rc-proc.sh
%{_libexecdir}/pcp/lib/rc-proc.sh.minimal
%{_libexecdir}/pcp/lib/utilproc.sh
%dir %{_libexecdir}/pcp/pmdas
%dir %{_libexecdir}/pcp/pmdas/activemq
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/activemq/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/activemq/Remove
%{_libexecdir}/pcp/pmdas/activemq/pmdaactivemq.pl
%{_libexecdir}/pcp/pmdas/activemq/PCP
%dir %{_libexecdir}/pcp/pmdas/amdgpu
%doc %{_libexecdir}/pcp/pmdas/amdgpu/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/amdgpu/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/amdgpu/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/amdgpu/pmda_amdgpu.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/amdgpu/pmdaamdgpu
%{_libexecdir}/pcp/pmdas/amdgpu/domain.h
%{_libexecdir}/pcp/pmdas/amdgpu/help
%{_libexecdir}/pcp/pmdas/amdgpu/pmns
%{_libexecdir}/pcp/pmdas/amdgpu/root
%dir %{_libexecdir}/pcp/pmdas/apache
%doc %{_libexecdir}/pcp/pmdas/apache/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/apache/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/apache/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/apache/pmdaapache
%{_libexecdir}/pcp/pmdas/apache/domain.h
%{_libexecdir}/pcp/pmdas/apache/help
%{_libexecdir}/pcp/pmdas/apache/pmns
%{_libexecdir}/pcp/pmdas/apache/root
%dir %{_libexecdir}/pcp/pmdas/bash
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/bash/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/bash/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/bash/pmdabash
%{_libexecdir}/pcp/pmdas/bash/domain.h
%{_libexecdir}/pcp/pmdas/bash/help
%{_libexecdir}/pcp/pmdas/bash/pmns
%{_libexecdir}/pcp/pmdas/bash/root
%{_libexecdir}/pcp/pmdas/bash/test-child.sh
%{_libexecdir}/pcp/pmdas/bash/test-trace.sh
%dir %{_libexecdir}/pcp/pmdas/bind2
%doc %{_libexecdir}/pcp/pmdas/bind2/README.md
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/bind2/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/bind2/Remove
%{_libexecdir}/pcp/pmdas/bind2/pmdabind2.pl
%dir %{_libexecdir}/pcp/pmdas/bonding
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/bonding/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/bonding/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/bonding/pmdabonding.pl
%dir %{_libexecdir}/pcp/pmdas/cifs
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/cifs/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/cifs/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/cifs/pmdacifs
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/cifs/pmda_cifs.so
%{_libexecdir}/pcp/pmdas/cifs/domain.h
%{_libexecdir}/pcp/pmdas/cifs/help
%{_libexecdir}/pcp/pmdas/cifs/pmns
%{_libexecdir}/pcp/pmdas/cifs/root
%dir %{_libexecdir}/pcp/pmdas/cisco
%doc %{_libexecdir}/pcp/pmdas/cisco/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/cisco/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/cisco/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/cisco/pmdacisco
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/cisco/parse
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/cisco/probe
%{_libexecdir}/pcp/pmdas/cisco/domain.h
%{_libexecdir}/pcp/pmdas/cisco/help
%{_libexecdir}/pcp/pmdas/cisco/pmns
%{_libexecdir}/pcp/pmdas/cisco/root
%dir %{_libexecdir}/pcp/pmdas/dbping
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/dbping/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/dbping/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/dbping/dbprobe.pl
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/dbping/pmdadbping.pl
%dir %{_libexecdir}/pcp/pmdas/denki
%doc %{_libexecdir}/pcp/pmdas/denki/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/denki/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/denki/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/denki/pmdadenki
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/denki/pmda_denki.so
%{_libexecdir}/pcp/pmdas/denki/domain.h
%{_libexecdir}/pcp/pmdas/denki/help
%{_libexecdir}/pcp/pmdas/denki/pmns
%{_libexecdir}/pcp/pmdas/denki/root
%dir %{_libexecdir}/pcp/pmdas/dm
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/dm/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/dm/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/dm/Upgrade
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/dm/pmda_dm.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/dm/pmdadm
%{_libexecdir}/pcp/pmdas/dm/domain.h
%{_libexecdir}/pcp/pmdas/dm/help
%{_libexecdir}/pcp/pmdas/dm/pmns.dmcache
%{_libexecdir}/pcp/pmdas/dm/pmns.dmstats
%{_libexecdir}/pcp/pmdas/dm/pmns.dmthin
%{_libexecdir}/pcp/pmdas/dm/pmns.vdo
%{_libexecdir}/pcp/pmdas/dm/root
%dir %{_libexecdir}/pcp/pmdas/docker
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/docker/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/docker/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/docker/pmda_docker.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/docker/pmdadocker
%{_libexecdir}/pcp/pmdas/docker/domain.h
%{_libexecdir}/pcp/pmdas/docker/help
%{_libexecdir}/pcp/pmdas/docker/pmns
%{_libexecdir}/pcp/pmdas/docker/root
%dir %{_libexecdir}/pcp/pmdas/ds389
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/ds389/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/ds389/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/ds389/pmdads389.pl
%{_libexecdir}/pcp/pmdas/ds389/ds389.conf.example
%dir %{_libexecdir}/pcp/pmdas/ds389log
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/ds389log/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/ds389log/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/ds389log/pmdads389log.pl
%dir %{_libexecdir}/pcp/pmdas/elasticsearch
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/elasticsearch/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/elasticsearch/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/elasticsearch/Upgrade
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/elasticsearch/pmdaelasticsearch.python
%dir %{_libexecdir}/pcp/pmdas/farm
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/farm/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/farm/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/farm/pmdafarm
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/farm/pmda_farm.so
%{_libexecdir}/pcp/pmdas/farm/domain.h
%{_libexecdir}/pcp/pmdas/farm/help
%{_libexecdir}/pcp/pmdas/farm/pmns
%{_libexecdir}/pcp/pmdas/farm/root
%dir %{_libexecdir}/pcp/pmdas/gfs2
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gfs2/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gfs2/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gfs2/pmdagfs2
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gfs2/pmda_gfs2.so
%{_libexecdir}/pcp/pmdas/gfs2/domain.h
%{_libexecdir}/pcp/pmdas/gfs2/help
%{_libexecdir}/pcp/pmdas/gfs2/pmns
%{_libexecdir}/pcp/pmdas/gfs2/root
%dir %{_libexecdir}/pcp/pmdas/gluster
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gluster/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gluster/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gluster/pmdagluster.python
%dir %{_libexecdir}/pcp/pmdas/gpfs
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gpfs/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gpfs/Remove
%{_libexecdir}/pcp/pmdas/gpfs/pmdagpfs.pl
%dir %{_libexecdir}/pcp/pmdas/gpsd
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gpsd/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gpsd/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/gpsd/pmdagpsd.pl
%dir %{_libexecdir}/pcp/pmdas/hacluster
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/hacluster/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/hacluster/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/hacluster/pmdahacluster
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/hacluster/pmda_hacluster.so
%{_libexecdir}/pcp/pmdas/hacluster/domain.h
%{_libexecdir}/pcp/pmdas/hacluster/help
%{_libexecdir}/pcp/pmdas/hacluster/pmns
%{_libexecdir}/pcp/pmdas/hacluster/root
%dir %{_libexecdir}/pcp/pmdas/haproxy
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/haproxy/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/haproxy/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/haproxy/connect
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/haproxy/pmdahaproxy.python
%dir %{_libexecdir}/pcp/pmdas/infiniband
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/infiniband/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/infiniband/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/infiniband/Upgrade
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/infiniband/pmdaib
%{_libexecdir}/pcp/pmdas/infiniband/domain.h
%{_libexecdir}/pcp/pmdas/infiniband/help
%{_libexecdir}/pcp/pmdas/infiniband/pmns
%{_libexecdir}/pcp/pmdas/infiniband/root
%dir %{_libexecdir}/pcp/pmdas/jbd2
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/jbd2/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/jbd2/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/jbd2/pmdajbd2
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/jbd2/pmda_jbd2.so
%{_libexecdir}/pcp/pmdas/jbd2/domain.h
%{_libexecdir}/pcp/pmdas/jbd2/help
%{_libexecdir}/pcp/pmdas/jbd2/help.dir
%{_libexecdir}/pcp/pmdas/jbd2/help.pag
%{_libexecdir}/pcp/pmdas/jbd2/root
%{_libexecdir}/pcp/pmdas/jbd2/root_jbd2
%dir %{_libexecdir}/pcp/pmdas/json
%doc %{_libexecdir}/pcp/pmdas/json/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/json/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/json/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/json/generate_ceph_metadata
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/json/pmdajson.python
%dir %{_libexecdir}/pcp/pmdas/kvm
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/kvm/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/kvm/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/kvm/Upgrade
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/kvm/pmda_kvm.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/kvm/pmdakvm
%{_libexecdir}/pcp/pmdas/kvm/domain.h
%{_libexecdir}/pcp/pmdas/kvm/help
%{_libexecdir}/pcp/pmdas/kvm/help.dir
%{_libexecdir}/pcp/pmdas/kvm/help.pag
%{_libexecdir}/pcp/pmdas/kvm/root
%{_libexecdir}/pcp/pmdas/kvm/root_kvm
%dir %{_libexecdir}/pcp/pmdas/linux
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/linux/pmdalinux
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/linux/pmda_linux.so
%{_libexecdir}/pcp/pmdas/linux/domain.h
%{_libexecdir}/pcp/pmdas/linux/help*
%dir %{_libexecdir}/pcp/pmdas/lmsensors
%doc %{_libexecdir}/pcp/pmdas/lmsensors/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/lmsensors/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/lmsensors/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/lmsensors/pmdalmsensors.python
%{_libexecdir}/pcp/pmdas/lmsensors/help
%{_libexecdir}/pcp/pmdas/lmsensors/pmns
%{_libexecdir}/pcp/pmdas/lmsensors/root
%dir %{_libexecdir}/pcp/pmdas/logger
%doc %{_libexecdir}/pcp/pmdas/logger/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/logger/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/logger/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/logger/pmdalogger
%{_libexecdir}/pcp/pmdas/logger/domain.h
%{_libexecdir}/pcp/pmdas/logger/help
%{_libexecdir}/pcp/pmdas/logger/pmns
%{_libexecdir}/pcp/pmdas/logger/root
%dir %{_libexecdir}/pcp/pmdas/lustre
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/lustre/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/lustre/Remove
%{_libexecdir}/pcp/pmdas/lustre/pmdalustre.pl
%dir %{_libexecdir}/pcp/pmdas/lustrecomm
%doc %{_libexecdir}/pcp/pmdas/lustrecomm/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/lustrecomm/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/lustrecomm/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/lustrecomm/pmdalustrecomm
%{_libexecdir}/pcp/pmdas/lustrecomm/domain.h
%{_libexecdir}/pcp/pmdas/lustrecomm/help
%{_libexecdir}/pcp/pmdas/lustrecomm/pmns
%{_libexecdir}/pcp/pmdas/lustrecomm/root
%dir %{_libexecdir}/pcp/pmdas/mailq
%doc %{_libexecdir}/pcp/pmdas/mailq/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mailq/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mailq/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mailq/pmdamailq
%{_libexecdir}/pcp/pmdas/mailq/domain.h
%{_libexecdir}/pcp/pmdas/mailq/help
%{_libexecdir}/pcp/pmdas/mailq/pmns
%{_libexecdir}/pcp/pmdas/mailq/root
%dir %{_libexecdir}/pcp/pmdas/memcache
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/memcache/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/memcache/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/memcache/pmdamemcache.pl
%dir %{_libexecdir}/pcp/pmdas/mic
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mic/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mic/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mic/pmdamic.python
%dir %{_libexecdir}/pcp/pmdas/mmv
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mmv/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mmv/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mmv/pmdammv
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mmv/pmda_mmv.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mmv/mmvdump
%{_libexecdir}/pcp/pmdas/mmv/domain.h
%{_libexecdir}/pcp/pmdas/mmv/root_mmv
%dir %{_libexecdir}/pcp/pmdas/mounts
%doc %{_libexecdir}/pcp/pmdas/mounts/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mounts/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mounts/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mounts/pmdamounts
%{_libexecdir}/pcp/pmdas/mounts/domain.h
%{_libexecdir}/pcp/pmdas/mounts/help
%{_libexecdir}/pcp/pmdas/mounts/pmns
%{_libexecdir}/pcp/pmdas/mounts/root
%dir %{_libexecdir}/pcp/pmdas/mysql
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mysql/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mysql/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mysql/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/mysql/pmdamysql.pl
%dir %{_libexecdir}/pcp/pmdas/named
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/named/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/named/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/named/pmdanamed.pl
%dir %{_libexecdir}/pcp/pmdas/netcheck
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/netcheck/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/netcheck/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/netcheck/pmdanetcheck.python
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/netcheck/pmdautil.python
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/netcheck/pyprep
%dir %{_libexecdir}/pcp/pmdas/nutcracker
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nutcracker/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nutcracker/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nutcracker/pmdanutcracker.pl
%dir %{_libexecdir}/pcp/pmdas/netcheck/modules
%{_libexecdir}/pcp/pmdas/netcheck/modules/__init__.python
%{_libexecdir}/pcp/pmdas/netcheck/modules/dns_lookup.python
%{_libexecdir}/pcp/pmdas/netcheck/modules/dns_reverse.python
%{_libexecdir}/pcp/pmdas/netcheck/modules/pcpnetcheck.python
%{_libexecdir}/pcp/pmdas/netcheck/modules/ping.python
%{_libexecdir}/pcp/pmdas/netcheck/modules/ping_latency.python
%{_libexecdir}/pcp/pmdas/netcheck/modules/ping_loss.python
%{_libexecdir}/pcp/pmdas/netcheck/modules/port_open.python
%{_libexecdir}/pcp/pmdas/netcheck/modules/url_get.python
%dir %{_libexecdir}/pcp/pmdas/netfilter
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/netfilter/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/netfilter/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/netfilter/pmdanetfilter.pl
%dir %{_libexecdir}/pcp/pmdas/news
%doc %{_libexecdir}/pcp/pmdas/news/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/news/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/news/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/news/pmdanews.pl
%{_libexecdir}/pcp/pmdas/news/active
%dir %{_libexecdir}/pcp/pmdas/nfsclient
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nfsclient/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nfsclient/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nfsclient/Upgrade
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nfsclient/pmdanfsclient.python
%dir %{_libexecdir}/pcp/pmdas/nginx
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nginx/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nginx/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nginx/pmdanginx.pl
%dir %{_libexecdir}/pcp/pmdas/nvidia
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nvidia/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nvidia/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nvidia/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nvidia/pmda_nvidia.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/nvidia/pmdanvidia
%{_libexecdir}/pcp/pmdas/nvidia/domain.h
%{_libexecdir}/pcp/pmdas/nvidia/help
%{_libexecdir}/pcp/pmdas/nvidia/pmns
%{_libexecdir}/pcp/pmdas/nvidia/root
%dir %{_libexecdir}/pcp/pmdas/openmetrics
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/openmetrics/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/openmetrics/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/openmetrics/Upgrade
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/openmetrics/pmdaopenmetrics.python
%dir %{_libexecdir}/pcp/pmdas/openvswitch
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/openvswitch/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/openvswitch/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/openvswitch/pmdaopenvswitch.python
%dir %{_libexecdir}/pcp/pmdas/oracle
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/oracle/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/oracle/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/oracle/connect.pl
%{_libexecdir}/pcp/pmdas/oracle/pmdaoracle.pl
%dir %{_libexecdir}/pcp/pmdas/overhead
%doc %{_libexecdir}/pcp/pmdas/overhead/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/overhead/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/overhead/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/overhead/pmdaoverhead
%{_libexecdir}/pcp/pmdas/overhead/domain.h
%{_libexecdir}/pcp/pmdas/overhead/pmns
%{_libexecdir}/pcp/pmdas/overhead/root
%dir %{_libexecdir}/pcp/pmdas/pdns
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/pdns/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/pdns/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/pdns/pmdapdns.pl
%dir %{_libexecdir}/pcp/pmdas/perfevent
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/perfevent/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/perfevent/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/perfevent/Upgrade
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/perfevent/perfalloc
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/perfevent/perfevent-makerewrite.pl
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/perfevent/pmdaperfevent
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/perfevent/pmda_perfevent.so
%{_libexecdir}/pcp/pmdas/perfevent/domain.h
%{_libexecdir}/pcp/pmdas/perfevent/help
%{_libexecdir}/pcp/pmdas/perfevent/pmns
%{_libexecdir}/pcp/pmdas/perfevent/root
%dir %{_libexecdir}/pcp/pmdas/pipe
%doc %{_libexecdir}/pcp/pmdas/pipe/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/pipe/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/pipe/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/pipe/pmdapipe
%{_libexecdir}/pcp/pmdas/pipe/domain.h
%{_libexecdir}/pcp/pmdas/pipe/help
%{_libexecdir}/pcp/pmdas/pipe/pmns
%{_libexecdir}/pcp/pmdas/pipe/root
%dir %{_libexecdir}/pcp/pmdas/podman
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/podman/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/podman/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/podman/pmdapodman
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/podman/pmda_podman.so
%{_libexecdir}/pcp/pmdas/podman/domain.h
%{_libexecdir}/pcp/pmdas/podman/help
%{_libexecdir}/pcp/pmdas/podman/pmns
%{_libexecdir}/pcp/pmdas/podman/root
%dir %{_libexecdir}/pcp/pmdas/pmcd
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/pmcd/pmda_pmcd.so
%{_libexecdir}/pcp/pmdas/pmcd/help.*
%dir %{_libexecdir}/pcp/pmdas/postgresql
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/postgresql/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/postgresql/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/postgresql/Upgrade
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/postgresql/pmdapostgresql.python
%dir %{_libexecdir}/pcp/pmdas/proc
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/proc/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/proc/Remove
%{_libexecdir}/pcp/pmdas/proc/help.dir
%{_libexecdir}/pcp/pmdas/proc/help.pag
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/proc/pmdaproc
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/proc/pmda_proc.so
%{_libexecdir}/pcp/pmdas/proc/domain.h
%{_libexecdir}/pcp/pmdas/proc/help
%{_libexecdir}/pcp/pmdas/proc/root
%{_libexecdir}/pcp/pmdas/proc/root_proc
%dir %{_libexecdir}/pcp/pmdas/rabbitmq
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/rabbitmq/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/rabbitmq/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/rabbitmq/pmdarabbitmq.python
%dir %{_libexecdir}/pcp/pmdas/redis
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/redis/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/redis/Remove
%{_libexecdir}/pcp/pmdas/redis/pmdaredis.pl
%dir %{_libexecdir}/pcp/pmdas/roomtemp
%doc %{_libexecdir}/pcp/pmdas/roomtemp/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/roomtemp/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/roomtemp/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/roomtemp/pmdaroomtemp
%{_libexecdir}/pcp/pmdas/roomtemp/domain.h
%{_libexecdir}/pcp/pmdas/roomtemp/help
%{_libexecdir}/pcp/pmdas/roomtemp/pmns
%{_libexecdir}/pcp/pmdas/roomtemp/root
%dir %{_libexecdir}/pcp/pmdas/root
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/root/pmdaroot
%{_libexecdir}/pcp/pmdas/root/domain.h
%{_libexecdir}/pcp/pmdas/root/help
%{_libexecdir}/pcp/pmdas/root/help.dir
%{_libexecdir}/pcp/pmdas/root/help.pag
%{_libexecdir}/pcp/pmdas/root/root
%{_libexecdir}/pcp/pmdas/root/root_root
%dir %{_libexecdir}/pcp/pmdas/rsyslog
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/rsyslog/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/rsyslog/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/rsyslog/pmdarsyslog.pl
%dir %{_libexecdir}/pcp/pmdas/samba
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/samba/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/samba/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/samba/pmdasamba.pl
%dir %{_libexecdir}/pcp/pmdas/sample
%doc %{_libexecdir}/pcp/pmdas/sample/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sample/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sample/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sample/pmda_sample.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sample/pmdasample
%{_libexecdir}/pcp/pmdas/sample/Makefile
%{_libexecdir}/pcp/pmdas/sample/domain.h
%{_libexecdir}/pcp/pmdas/sample/events.[ch]
%{_libexecdir}/pcp/pmdas/sample/libpcp.h
%{_libexecdir}/pcp/pmdas/sample/percontext.[ch]
%{_libexecdir}/pcp/pmdas/sample/pmda.c
%{_libexecdir}/pcp/pmdas/sample/proc.[ch]
%{_libexecdir}/pcp/pmdas/sample/sample.c
%{_libexecdir}/pcp/pmdas/sample/help
%{_libexecdir}/pcp/pmdas/sample/pmns
%{_libexecdir}/pcp/pmdas/sample/root
%dir %{_libexecdir}/pcp/pmdas/sendmail
%doc %{_libexecdir}/pcp/pmdas/sendmail/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sendmail/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sendmail/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sendmail/pmdasendmail
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sendmail/pmda_sendmail.so
%{_libexecdir}/pcp/pmdas/sendmail/domain.h
%{_libexecdir}/pcp/pmdas/sendmail/help
%{_libexecdir}/pcp/pmdas/sendmail/pmns
%{_libexecdir}/pcp/pmdas/sendmail/root
%dir %{_libexecdir}/pcp/pmdas/shping
%doc %{_libexecdir}/pcp/pmdas/shping/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/shping/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/shping/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/shping/pmdashping
%{_libexecdir}/pcp/pmdas/shping/domain.h
%{_libexecdir}/pcp/pmdas/shping/help
%{_libexecdir}/pcp/pmdas/shping/pmns
%{_libexecdir}/pcp/pmdas/shping/root
%dir %{_libexecdir}/pcp/pmdas/simple
%doc %{_libexecdir}/pcp/pmdas/simple/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/simple/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/simple/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/simple/pmdasimple.perl
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/simple/pmdasimple.python
%{_libexecdir}/pcp/pmdas/simple/domain.h
%{_libexecdir}/pcp/pmdas/simple/help
%{_libexecdir}/pcp/pmdas/simple/pmns
%{_libexecdir}/pcp/pmdas/simple/root
%{_libexecdir}/pcp/pmdas/simple/Makefile
%{_libexecdir}/pcp/pmdas/simple/simple.c
%dir %{_libexecdir}/pcp/pmdas/slurm
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/slurm/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/slurm/Remove
%{_libexecdir}/pcp/pmdas/slurm/pmdaslurm.pl
%dir %{_libexecdir}/pcp/pmdas/smart
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/smart/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/smart/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/smart/pmda_smart.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/smart/pmdasmart
%{_libexecdir}/pcp/pmdas/smart/domain.h
%{_libexecdir}/pcp/pmdas/smart/help
%{_libexecdir}/pcp/pmdas/smart/pmns
%{_libexecdir}/pcp/pmdas/smart/root
%dir %{_libexecdir}/pcp/pmdas/snmp
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/snmp/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/snmp/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/snmp/pmdasnmp.pl
%dir %{_libexecdir}/pcp/pmdas/sockets
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sockets/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sockets/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sockets/Upgrade
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sockets/pmdasockets
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/sockets/pmda_sockets.so
%{_libexecdir}/pcp/pmdas/sockets/domain.h
%{_libexecdir}/pcp/pmdas/sockets/help
%{_libexecdir}/pcp/pmdas/sockets/pmns
%{_libexecdir}/pcp/pmdas/sockets/root
%dir %{_libexecdir}/pcp/pmdas/summary
%doc %{_libexecdir}/pcp/pmdas/summary/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/summary/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/summary/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/summary/pmdasummary
%{_libexecdir}/pcp/pmdas/summary/domain.h
%{_libexecdir}/pcp/pmdas/summary/help
%{_libexecdir}/pcp/pmdas/summary/pmns
%{_libexecdir}/pcp/pmdas/summary/root
%dir %{_libexecdir}/pcp/pmdas/systemd
%doc %{_libexecdir}/pcp/pmdas/systemd/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/systemd/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/systemd/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/systemd/pmdasystemd
%{_libexecdir}/pcp/pmdas/systemd/domain.h
%{_libexecdir}/pcp/pmdas/systemd/help
%{_libexecdir}/pcp/pmdas/systemd/pmns
%{_libexecdir}/pcp/pmdas/systemd/root
%dir %{_libexecdir}/pcp/pmdas/trace
%doc %{_libexecdir}/pcp/pmdas/trace/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/trace/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/trace/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/trace/pmdatrace
%{_libexecdir}/pcp/pmdas/trace/domain.h
%{_libexecdir}/pcp/pmdas/trace/help
%{_libexecdir}/pcp/pmdas/trace/pmns
%{_libexecdir}/pcp/pmdas/trace/root
%dir %{_libexecdir}/pcp/pmdas/trivial
%doc %{_libexecdir}/pcp/pmdas/trivial/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/trivial/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/trivial/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/trivial/pmdatrivial.perl
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/trivial/pmdatrivial.python
%{_libexecdir}/pcp/pmdas/trivial/domain.h
%{_libexecdir}/pcp/pmdas/trivial/help
%{_libexecdir}/pcp/pmdas/trivial/pmns
%{_libexecdir}/pcp/pmdas/trivial/root
%{_libexecdir}/pcp/pmdas/trivial/Makefile
%{_libexecdir}/pcp/pmdas/trivial/trivial.c
%dir %{_libexecdir}/pcp/pmdas/txmon
%doc %{_libexecdir}/pcp/pmdas/txmon/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/txmon/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/txmon/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/txmon/genload
%{_libexecdir}/pcp/pmdas/txmon/domain.h
%{_libexecdir}/pcp/pmdas/txmon/help
%{_libexecdir}/pcp/pmdas/txmon/pmns
%{_libexecdir}/pcp/pmdas/txmon/root
%{_libexecdir}/pcp/pmdas/txmon/Makefile
%{_libexecdir}/pcp/pmdas/txmon/txmon.c
%{_libexecdir}/pcp/pmdas/txmon/txmon.h
%{_libexecdir}/pcp/pmdas/txmon/txrecord.c
%dir %{_libexecdir}/pcp/pmdas/unbound
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/unbound/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/unbound/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/unbound/pmdaunbound.python
%dir %{_libexecdir}/pcp/pmdas/uwsgi
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/uwsgi/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/uwsgi/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/uwsgi/pmdauwsgi.python
%dir %{_libexecdir}/pcp/pmdas/weblog
%doc %{_libexecdir}/pcp/pmdas/weblog/README
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/weblog/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/weblog/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/weblog/check_match
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/weblog/pmdaweblog
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/weblog/server.sh
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/weblog/weblogconv.sh
%{_libexecdir}/pcp/pmdas/weblog/domain.h
%{_libexecdir}/pcp/pmdas/weblog/help
%{_libexecdir}/pcp/pmdas/weblog/pmns
%{_libexecdir}/pcp/pmdas/weblog/root
%dir %{_libexecdir}/pcp/pmdas/xfs
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/xfs/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/xfs/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/xfs/pmda_xfs.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/xfs/pmdaxfs
%{_libexecdir}/pcp/pmdas/xfs/domain.h
%{_libexecdir}/pcp/pmdas/xfs/help
%{_libexecdir}/pcp/pmdas/xfs/help.dir
%{_libexecdir}/pcp/pmdas/xfs/help.pag
%{_libexecdir}/pcp/pmdas/xfs/root
%{_libexecdir}/pcp/pmdas/xfs/root_xfs
%dir %{_libexecdir}/pcp/pmdas/zfs
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zfs/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zfs/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zfs/pmda_zfs.so
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zfs/pmdazfs
%{_libexecdir}/pcp/pmdas/zfs/domain.h
%{_libexecdir}/pcp/pmdas/zfs/help
%{_libexecdir}/pcp/pmdas/zfs/pmns
%{_libexecdir}/pcp/pmdas/zfs/root
%dir %{_libexecdir}/pcp/pmdas/zimbra
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zimbra/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zimbra/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zimbra/pmdazimbra.pl
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zimbra/runaszimbra
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zimbra/zimbraprobe
%dir %{_libexecdir}/pcp/pmdas/zswap
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zswap/Install
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zswap/Remove
%attr(755,root,root) %{_libexecdir}/pcp/pmdas/zswap/pmdazswap.python
%dir %{_datadir}/pcp
%{_datadir}/pcp/htop
%dir %{_datadir}/pcp/lib
%attr(755,root,root) %{_datadir}/pcp/lib/ReplacePmnsSubtree
%attr(755,root,root) %{_datadir}/pcp/lib/lockpmns
%attr(755,root,root) %{_datadir}/pcp/lib/unlockpmns
%{_datadir}/pcp/lib/bashproc.sh
%{_datadir}/pcp/lib/checkproc.sh
%{_datadir}/pcp/lib/pmdaproc.sh
%{_datadir}/pcp/lib/rc-proc.sh
%{_datadir}/pcp/lib/rc-proc.sh.minimal
%{_datadir}/pcp/lib/utilproc.sh
%dir %{_datadir}/pcp/lib/pmcheck
%attr(755,root,root) %{_datadir}/pcp/lib/pmcheck/*
%{_datadir}/pcp/zeroconf
%config(noreplace) %verify(not md5 mtime size) /etc/sasl/pmcd.conf
%dir %{_sysconfdir}/pcp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/indom.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/labels.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/tls.conf
%dir %{_sysconfdir}/pcp/bind2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/bind2/bind2.conf
%dir %{_sysconfdir}/pcp/derived
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/derived/cpu-util.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/derived/denki.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/derived/iostat.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/derived/mssql.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/derived/openmetrics.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/derived/proc.conf
%dir %{_sysconfdir}/pcp/discover
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/discover/pcp-kube-pods.conf
%dir %{_sysconfdir}/pcp/dstat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/aio
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/battery
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/cpu
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/disk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/dm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/entropy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/freespace
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/fs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/gpfs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/int
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/io
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/ipc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/load
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/locks
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/md
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/mem
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/memcache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/mongodb
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/mysql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/net
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/nfs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/page
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/part
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/postfix
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/proc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/redis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/rpc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/sockets
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/swap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/sys
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/tcp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/topbio
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/topchildwait
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/topcpu
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/topio
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/topmem
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/utmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/vm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/dstat/zfs
%dir %{_sysconfdir}/pcp/elasticsearch
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/elasticsearch/elasticsearch.conf
%dir %{_sysconfdir}/pcp/haproxy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/haproxy/haproxy.conf
%dir %{_sysconfdir}/pcp/json
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/json/config.json
%dir %{_sysconfdir}/pcp/kvm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/kvm/kvm.conf
%dir %{_sysconfdir}/pcp/linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/linux/interfaces.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/linux/samplebandwidth.conf
%dir %{_sysconfdir}/pcp/lustre
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/lustre/lustre.conf
%dir %{_sysconfdir}/pcp/mounts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/mounts/mounts.conf
%dir %{_sysconfdir}/pcp/netcheck
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/netcheck/netcheck.conf
%dir %{_sysconfdir}/pcp/nginx
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/nginx/nginx.conf
%dir %{_sysconfdir}/pcp/nutcracker
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/nutcracker/nutcracker.conf
%dir %{_sysconfdir}/pcp/openmetrics
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/openmetrics/collectd.url
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/openmetrics/etcd.url
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/openmetrics/grafana.url
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/openmetrics/kepler.url
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/openmetrics/spark.url
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/openmetrics/vllm.url
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/openmetrics/vmware.url
%dir %{_sysconfdir}/pcp/oracle
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/oracle/sample.conf
%dir %{_sysconfdir}/pcp/overhead
%dir %{_sysconfdir}/pcp/overhead/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/overhead/conf.d/default.conf
%dir %{_sysconfdir}/pcp/overhead/examples
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/overhead/examples/sample.conf
%dir %{_sysconfdir}/pcp/perfevent
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/perfevent/perfevent.conf
%dir %{_sysconfdir}/pcp/pipe
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pipe/sample.conf
%dir %{_sysconfdir}/pcp/pmafm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmafm/pcp
%dir %{_sysconfdir}/pcp/pmcd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmcd/pmcd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmcd/pmcd.options
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmcd/rc.local
%dir %{_sysconfdir}/pcp/pmchart
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Apache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/ApacheServer
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/BusyCPU
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/CPU
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Cisco
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Disk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Diskbytes
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/ElasticsearchServer
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Filesystem
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Iostat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Iostat.DM
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Iostat.MD
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Loadavg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/MemAvailable
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Memory
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/NFS2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/NFS3
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Netbytes
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Netpackets
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Overview
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/PMCD
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Paging
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Sample
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Schemes
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Sendmail
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Sockets
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Swap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Syscalls
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Web.Alarms
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Web.Allservers
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Web.Perserver.Bytes
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Web.Perserver.Requests
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Web.Requests
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/Web.Volume
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/shping.CPUTime
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/shping.RealTime
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmchart/vCPU
%attr(775,root,pcp) %dir %{_sysconfdir}/pcp/pmie
%attr(664,pcp,pcp) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmie/control
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmie/rc
%attr(775,root,pcp) %dir %{_sysconfdir}/pcp/pmie/class.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmie/class.d/pmfind
%attr(775,root,pcp) %dir %{_sysconfdir}/pcp/pmie/control.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmie/control.d/local
%dir %{_sysconfdir}/pcp/pmieconf
%dir %{_sysconfdir}/pcp/pmieconf/cisco
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/cisco/in_util
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/cisco/out_util
%dir %{_sysconfdir}/pcp/pmieconf/cpu
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/cpu/context_switch
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/cpu/load_average
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/cpu/low_util
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/cpu/system
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/cpu/util
%dir %{_sysconfdir}/pcp/pmieconf/dm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/dm/data_high_util
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/dm/metadata_high_util
%dir %{_sysconfdir}/pcp/pmieconf/entropy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/entropy/available
%dir %{_sysconfdir}/pcp/pmieconf/filesys
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/filesys/filling
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/filesys/vfs_files
%dir %{_sysconfdir}/pcp/pmieconf/global
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/global/parameters
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/global/pcp_actions
%dir %{_sysconfdir}/pcp/pmieconf/memory
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/memory/exhausted
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/memory/oom_kill
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/memory/swap_low
%dir %{_sysconfdir}/pcp/pmieconf/network
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/network/tcplistenoverflows
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/network/tcpqfulldocookies
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/network/tcpqfulldrops
%dir %{_sysconfdir}/pcp/pmieconf/openvswitch
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/errors
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/mtu_exceeded_drops
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/rx_drops
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/rx_qos_drops
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/tx_drops
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/tx_failure_drops
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/tx_qos_drops
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/tx_retries
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/vhost_notification
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/openvswitch/vhost_tx_contention
%dir %{_sysconfdir}/pcp/pmieconf/percpu
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/percpu/many_util
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/percpu/some_util
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/percpu/system
%dir %{_sysconfdir}/pcp/pmieconf/perdisk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/perdisk/average_queue_length
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/perdisk/average_wait_time
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/perdisk/bandwidth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/perdisk/iops
%dir %{_sysconfdir}/pcp/pmieconf/pernetif
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/pernetif/collisions
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/pernetif/errors
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/pernetif/packets
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/pernetif/util
%dir %{_sysconfdir}/pcp/pmieconf/power
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/power/thermal_throttle
%dir %{_sysconfdir}/pcp/pmieconf/primary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/primary/pmda_status
%dir %{_sysconfdir}/pcp/pmieconf/shping
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/shping/response
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/shping/status
%dir %{_sysconfdir}/pcp/pmieconf/testing
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/testing/test_actions
%dir %{_sysconfdir}/pcp/pmieconf/zeroconf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmieconf/zeroconf/all_threads
%dir %{_sysconfdir}/pcp/pmlogconf
%dir %{_sysconfdir}/pcp/pmlogconf/apache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/apache/processes
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/apache/summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/apache/uptime
%dir %{_sysconfdir}/pcp/pmlogconf/cpu
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/cpu/percpu
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/cpu/summary
%dir %{_sysconfdir}/pcp/pmlogconf/disk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/disk/percontroller
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/disk/perdisk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/disk/perpartition
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/disk/summary
%dir %{_sysconfdir}/pcp/pmlogconf/elasticsearch
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/elasticsearch/summary
%dir %{_sysconfdir}/pcp/pmlogconf/filesystem
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/filesystem/all
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/filesystem/rpc-server
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/filesystem/summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/filesystem/xfs-all
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/filesystem/xfs-io-linux
%dir %{_sysconfdir}/pcp/pmlogconf/gfs2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/gfs2/gfs2-all
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/gfs2/gfs2-base
%dir %{_sysconfdir}/pcp/pmlogconf/kernel
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/bufcache-activity
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/bufcache-all
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/inode-cache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/load
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/memory-linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/read-write-data
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/summary-linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/summary-windows
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/syscalls-linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kernel/vnodes
%dir %{_sysconfdir}/pcp/pmlogconf/kvm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/kvm/kvm
%dir %{_sysconfdir}/pcp/pmlogconf/libvirt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/libvirt/libvirt
%dir %{_sysconfdir}/pcp/pmlogconf/mailq
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/mailq/summary
%dir %{_sysconfdir}/pcp/pmlogconf/memcache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memcache/summary
%dir %{_sysconfdir}/pcp/pmlogconf/memory
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/buddyinfo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/ksminfo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/meminfo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/proc-linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/slabinfo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/swap-activity
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/swap-all
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/swap-config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/vmstat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/memory/zoneinfo
%dir %{_sysconfdir}/pcp/pmlogconf/mmv
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/mmv/summary
%dir %{_sysconfdir}/pcp/pmlogconf/mysql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/mysql/summary
%dir %{_sysconfdir}/pcp/pmlogconf/netcheck
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/netcheck/summary
%dir %{_sysconfdir}/pcp/pmlogconf/netfilter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/netfilter/config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/netfilter/summary
%dir %{_sysconfdir}/pcp/pmlogconf/networking
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/icmp6
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/interface-all
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/interface-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/ip6
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/mbufs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/multicast
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/nfs2-client
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/nfs2-server
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/nfs3-client
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/nfs3-server
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/nfs4-client
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/nfs4-server
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/other-protocols
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/perprocess-linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/persocket-linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/rpc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/socket-linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/softnet
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/streams
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/tcp-activity-linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/tcp-all
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/udp-all
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/udp-packets-linux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/networking/udp6
%dir %{_sysconfdir}/pcp/pmlogconf/nginx
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/nginx/summary
%dir %{_sysconfdir}/pcp/pmlogconf/openmetrics
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/openmetrics/kepler
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/openmetrics/summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/openmetrics/vllm
%dir %{_sysconfdir}/pcp/pmlogconf/openvswitch
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/openvswitch/summary
%dir %{_sysconfdir}/pcp/pmlogconf/oracle
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/oracle/summary
%dir %{_sysconfdir}/pcp/pmlogconf/platform
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/platform/hinv
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/platform/linux
%dir %{_sysconfdir}/pcp/pmlogconf/postgresql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/postgresql/summary
%dir %{_sysconfdir}/pcp/pmlogconf/rabbitmq
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/rabbitmq/summary
%dir %{_sysconfdir}/pcp/pmlogconf/rsyslog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/rsyslog/summary
%dir %{_sysconfdir}/pcp/pmlogconf/services
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/services/pmproxy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/services/redis
%dir %{_sysconfdir}/pcp/pmlogconf/shping
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/shping/summary
%dir %{_sysconfdir}/pcp/pmlogconf/sqlserver
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/sqlserver/summary
%dir %{_sysconfdir}/pcp/pmlogconf/statsd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/statsd/statsd
%dir %{_sysconfdir}/pcp/pmlogconf/storage
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/storage/vdo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/storage/vdo-summary
%dir %{_sysconfdir}/pcp/pmlogconf/tools
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-gpustats
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-hotproc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-httpstats
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-infiniband
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-nfsclient
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-perfevent
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-proc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-zfs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/atop-zswap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/collectl
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/collectl-interrupts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/collectl-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/dmcache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/dstat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/dstat-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/free
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/free-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/hotproc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/htop
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/htop-proc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/htop-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/htop-zfs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/iostat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/ip
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/ipcs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/mpstat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/mpstat-interrupts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/mpstat-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/numastat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/pcp-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/pidstat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/pidstat-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/pmclient
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/pmclient-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/pmieconf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/pmstat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/sar
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/sar-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/tapestat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/uptime
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/vector
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/vector-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/vmstat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/tools/vmstat-summary
%dir %{_sysconfdir}/pcp/pmlogconf/uwsgi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/uwsgi/summary
%dir %{_sysconfdir}/pcp/pmlogconf/zeroconf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/atop-proc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/disk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/filesystem
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/hugepages
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/hv-balloon
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/hv-balloon-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/interrupts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/nfsclient
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/numa
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/numahugepages
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/numastat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/pidstat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/pidstat-summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/rpc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/tapestat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/tty
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/vmmemctl
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zeroconf/xfs-perdev
%dir %{_sysconfdir}/pcp/pmlogconf/zimbra
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogconf/zimbra/all
%attr(775,root,pcp) %dir %{_sysconfdir}/pcp/pmlogger
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/config.pmstat
%attr(664,pcp,pcp) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/control
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/options.pmstat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/rc
%dir %{_sysconfdir}/pcp/pmlogger/class.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/class.d/pmfind
%attr(775,root,pcp) %dir %{_sysconfdir}/pcp/pmlogger/control.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/control.d/local
%dir %{_sysconfdir}/pcp/pmlogredact
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogredact/network
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogredact/usernames
%dir %{_sysconfdir}/pcp/pmlogrewrite
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/bind2.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/cgroup_units.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/jbd2_kernel_ulong.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/kvm_fixups.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_disk_all_fixups.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_kernel_fixups.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_kernel_ulong.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_mem_fixups.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_proc_fs_nfsd_fixups.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_proc_migrate.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_proc_net_snmp_migrate.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_proc_net_tcp_migrate.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_xfs_migrate.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/linux_xfs_perdev_buffer.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/mysql_migrate.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/nfsclient_migrate.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/pmcd_migrate.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/pmproxy_fixups.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/proc_discrete_strings.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/proc_jiffies.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/proc_kernel_ulong.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/proc_kernel_ulong_migrate.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogrewrite/proc_scheduler.conf
%dir %{_sysconfdir}/pcp/pmproxy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmproxy/pmproxy.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmproxy/pmproxy.options
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmproxy/rc
%dir %{_sysconfdir}/pcp/pmrep
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/00-defaults.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/collectl.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/iostat.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/iostat_v10.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/iostat_v11.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/iostat_v12_5.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/mpstat.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/numa.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/pidstat.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/pmproxy.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/pmstat.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/proc.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/sar.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/sar_v11.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmrep/vmstat.conf
%dir %{_sysconfdir}/pcp/pmsearch
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmsearch/pmsearch.conf
%dir %{_sysconfdir}/pcp/pmseries
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmseries/pmseries.conf
%dir %{_sysconfdir}/pcp/postgresql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/postgresql/pmdapostgresql.conf
%dir %{_sysconfdir}/pcp/proc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/proc/access.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/proc/samplehotproc.conf
%dir %{_sysconfdir}/pcp/rabbitmq
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/rabbitmq/rabbitmq.conf
%dir %{_sysconfdir}/pcp/redis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/redis/redis.conf
%dir %{_sysconfdir}/pcp/shping
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/shping/sample.conf
%dir %{_sysconfdir}/pcp/simple
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/simple/simple.conf
%dir %{_sysconfdir}/pcp/snmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/snmp/snmp.conf
%dir %{_sysconfdir}/pcp/sockets
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/sockets/filter.conf
%dir %{_sysconfdir}/pcp/summary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/summary/expr.pmie
%dir %{_sysconfdir}/pcp/uwsgi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/uwsgi/uwsgi.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pmcd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pmfind
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pmie_timers
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pmlogger
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pmlogger_farm
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pmlogger_timers
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pmproxy
%attr(754,root,root) /etc/rc.d/init.d/pcp
%attr(754,root,root) /etc/rc.d/init.d/pmcd
%attr(754,root,root) /etc/rc.d/init.d/pmie
%attr(754,root,root) /etc/rc.d/init.d/pmlogger
%attr(754,root,root) /etc/rc.d/init.d/pmproxy
%{systemdunitdir}/pcp-geolocate.service
%{systemdunitdir}/pcp-reboot-init.service
%{systemdunitdir}/pmcd.service
%{systemdunitdir}/pmfind.service
%{systemdunitdir}/pmfind.timer
%{systemdunitdir}/pmie.service
%{systemdunitdir}/pmie_check.service
%{systemdunitdir}/pmie_check.timer
%{systemdunitdir}/pmie_farm.service
%{systemdunitdir}/pmie_farm_check.service
%{systemdunitdir}/pmie_farm_check.timer
%{systemdunitdir}/pmie_daily.service
%{systemdunitdir}/pmie_daily.timer
%{systemdunitdir}/pmlogger.service
%{systemdunitdir}/pmlogger_check.service
%{systemdunitdir}/pmlogger_check.timer
%{systemdunitdir}/pmlogger_daily.service
%{systemdunitdir}/pmlogger_daily.timer
%{systemdunitdir}/pmlogger_farm.service
%{systemdunitdir}/pmlogger_farm_check.service
%{systemdunitdir}/pmlogger_farm_check.timer
%{systemdunitdir}/pmproxy.service
%dir /var/lib/pcp/config
%dir /var/lib/pcp/config/derived
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/derived/cpu-util.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/derived/denki.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/derived/iostat.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/derived/mssql.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/derived/openmetrics.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/derived/proc.conf
%dir /var/lib/pcp/config/pmafm
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmafm/pcp
%dir /var/lib/pcp/config/pmchart
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Apache
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/BusyCPU
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Cisco
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Iostat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Iostat.DM
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Iostat.MD
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/MemAvailable
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Sample
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Sendmail
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/shping.*
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Web.*
%attr(775,pcp,pcp) %dir /var/lib/pcp/config/pmda
%dir /var/lib/pcp/config/pmie
%dir /var/lib/pcp/config/pmieconf
%dir /var/lib/pcp/config/pmieconf/cisco
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cisco/in_util
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cisco/out_util
%dir /var/lib/pcp/config/pmieconf/cpu
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/context_switch
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/load_average
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/low_util
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/system
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/cpu/util
%dir /var/lib/pcp/config/pmieconf/dm
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/dm/data_high_util
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/dm/metadata_high_util
%dir /var/lib/pcp/config/pmieconf/entropy
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/entropy/available
%dir /var/lib/pcp/config/pmieconf/filesys
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/filesys/filling
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/filesys/vfs_files
%dir /var/lib/pcp/config/pmieconf/global
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/global/parameters
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/global/pcp_actions
%dir /var/lib/pcp/config/pmieconf/memory
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/memory/exhausted
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/memory/oom_kill
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/memory/swap_low
%dir /var/lib/pcp/config/pmieconf/network
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/network/tcplistenoverflows
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/network/tcpqfulldocookies
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/network/tcpqfulldrops
%dir /var/lib/pcp/config/pmieconf/openvswitch
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/errors
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/mtu_exceeded_drops
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/rx_drops
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/rx_qos_drops
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/tx_drops
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/tx_failure_drops
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/tx_qos_drops
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/tx_retries
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/vhost_notification
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/openvswitch/vhost_tx_contention
%dir /var/lib/pcp/config/pmieconf/percpu
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/percpu/many_util
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/percpu/some_util
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/percpu/system
%dir /var/lib/pcp/config/pmieconf/perdisk
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/perdisk/average_queue_length
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/perdisk/average_wait_time
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/perdisk/bandwidth
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/perdisk/iops
%dir /var/lib/pcp/config/pmieconf/pernetif
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/pernetif/collisions
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/pernetif/errors
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/pernetif/packets
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/pernetif/util
%dir /var/lib/pcp/config/pmieconf/power
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/power/thermal_throttle
%dir /var/lib/pcp/config/pmieconf/primary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/primary/pmda_status
%dir /var/lib/pcp/config/pmieconf/shping
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/shping/response
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/shping/status
%dir /var/lib/pcp/config/pmieconf/testing
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/testing/test_actions
%dir /var/lib/pcp/config/pmieconf/zeroconf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmieconf/zeroconf/all_threads
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
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/disk/perpartition
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/disk/summary
%dir /var/lib/pcp/config/pmlogconf/elasticsearch
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/elasticsearch/summary
%dir /var/lib/pcp/config/pmlogconf/filesystem
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/rpc-server
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/xfs-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/filesystem/xfs-io-linux
%dir /var/lib/pcp/config/pmlogconf/kernel
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/bufcache-activity
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/bufcache-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/inode-cache
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/load
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/memory-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/read-write-data
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/summary-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/summary-windows
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/syscalls-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kernel/vnodes
%dir /var/lib/pcp/config/pmlogconf/kvm
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/kvm/kvm
%dir /var/lib/pcp/config/pmlogconf/libvirt
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/libvirt/libvirt
%dir /var/lib/pcp/config/pmlogconf/memcache
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memcache/summary
%dir /var/lib/pcp/config/pmlogconf/mailq
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/mailq/summary
%dir /var/lib/pcp/config/pmlogconf/memory
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/buddyinfo
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/ksminfo
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/meminfo
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/proc-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/slabinfo
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/swap-activity
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/swap-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/swap-config
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/vmstat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/memory/zoneinfo
%dir /var/lib/pcp/config/pmlogconf/mmv
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/mmv/summary
%dir /var/lib/pcp/config/pmlogconf/mysql
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/mysql/summary
%dir /var/lib/pcp/config/pmlogconf/netcheck
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/netcheck/summary
%dir /var/lib/pcp/config/pmlogconf/netfilter
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/netfilter/config
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/netfilter/summary
%dir /var/lib/pcp/config/pmlogconf/networking
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/icmp6
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/interface-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/interface-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/ip6
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/mbufs
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/multicast
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs2-client
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs2-server
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs3-client
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs3-server
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs4-client
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/nfs4-server
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/other-protocols
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/perprocess-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/persocket-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/rpc
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/socket-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/softnet
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/streams
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/tcp-activity-linux
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/tcp-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/udp6
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/udp-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/networking/udp-packets-linux
%dir /var/lib/pcp/config/pmlogconf/nginx
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/nginx/summary
%dir /var/lib/pcp/config/pmlogconf/openmetrics
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/openmetrics/kepler
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/openmetrics/summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/openmetrics/vllm
%dir /var/lib/pcp/config/pmlogconf/openvswitch
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/openvswitch/summary
%dir /var/lib/pcp/config/pmlogconf/oracle
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/oracle/summary
%dir /var/lib/pcp/config/pmlogconf/postgresql
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/postgresql/summary
%dir /var/lib/pcp/config/pmlogconf/platform
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/platform/hinv
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/platform/linux
%dir /var/lib/pcp/config/pmlogconf/rabbitmq
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/rabbitmq/summary
%dir /var/lib/pcp/config/pmlogconf/rsyslog
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/rsyslog/summary
%dir /var/lib/pcp/config/pmlogconf/services
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/services/pmproxy
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/services/redis
%dir /var/lib/pcp/config/pmlogconf/shping
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/shping/summary
%dir /var/lib/pcp/config/pmlogconf/sqlserver
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/sqlserver/summary
%dir /var/lib/pcp/config/pmlogconf/storage
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/storage/vdo
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/storage/vdo-summary
%dir /var/lib/pcp/config/pmlogconf/tools
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-gpustats
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-hotproc
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-httpstats
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-infiniband
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-nfsclient
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-perfevent
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-proc
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-zfs
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/atop-zswap
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/collectl
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/collectl-interrupts
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/collectl-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/dmcache
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/dstat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/dstat-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/free
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/free-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/hotproc
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/htop
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/htop-proc
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/htop-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/htop-zfs
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/iostat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/ip
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/ipcs
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/mpstat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/mpstat-interrupts
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/mpstat-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/numastat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/pcp-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/pidstat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/pidstat-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/pmclient
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/pmclient-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/pmieconf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/pmstat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/sar
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/sar-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/tapestat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/uptime
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/vector
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/vector-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/vmstat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/tools/vmstat-summary
%dir /var/lib/pcp/config/pmlogconf/uwsgi
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/uwsgi/summary
%dir /var/lib/pcp/config/pmlogconf/zeroconf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/atop-proc
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/disk
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/filesystem
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/hugepages
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/hv-balloon
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/hv-balloon-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/interrupts
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/nfsclient
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/numa
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/numahugepages
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/numastat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/pidstat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/pidstat-summary
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/rpc
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/tapestat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/tty
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/vmmemctl
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zeroconf/xfs-perdev
%dir /var/lib/pcp/config/pmlogconf/zimbra
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/zimbra/all
%dir /var/lib/pcp/config/pmlogconf/gfs2
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/gfs2/gfs2-all
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/gfs2/gfs2-base
%dir /var/lib/pcp/config/pmlogconf/statsd
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogconf/statsd/statsd
%dir /var/lib/pcp/config/pmlogger
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.pmstat
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/options.pmstat
%dir /var/lib/pcp/config/pmlogredact
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogredact/network
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogredact/usernames
%dir /var/lib/pcp/config/pmlogrewrite
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/bind2.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/cgroup_units.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/jbd2_kernel_ulong.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/kvm_fixups.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_disk_all_fixups.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_kernel_fixups.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_kernel_ulong.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_mem_fixups.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_proc_fs_nfsd_fixups.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_proc_migrate.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_proc_net_snmp_migrate.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_proc_net_tcp_migrate.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_xfs_migrate.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/linux_xfs_perdev_buffer.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/mysql_migrate.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/nfsclient_migrate.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/pmcd_migrate.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/pmproxy_fixups.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/proc_discrete_strings.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/proc_jiffies.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/proc_kernel_ulong.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/proc_kernel_ulong_migrate.conf
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogrewrite/proc_scheduler.conf
%dir /var/lib/pcp/pmdas
%dir /var/lib/pcp/pmdas/activemq
%attr(755,root,root) /var/lib/pcp/pmdas/activemq/Install
%attr(755,root,root) /var/lib/pcp/pmdas/activemq/Remove
/var/lib/pcp/pmdas/activemq/pmdaactivemq.pl
/var/lib/pcp/pmdas/activemq/PCP
%dir /var/lib/pcp/pmdas/amdgpu
%doc /var/lib/pcp/pmdas/amdgpu/README
%attr(755,root,root) /var/lib/pcp/pmdas/amdgpu/Install
%attr(755,root,root) /var/lib/pcp/pmdas/amdgpu/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/amdgpu/pmda_amdgpu.so
%attr(755,root,root) /var/lib/pcp/pmdas/amdgpu/pmdaamdgpu
/var/lib/pcp/pmdas/amdgpu/domain.h
/var/lib/pcp/pmdas/amdgpu/help
/var/lib/pcp/pmdas/amdgpu/pmns
/var/lib/pcp/pmdas/amdgpu/root
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
/var/lib/pcp/pmdas/bash/test-child.sh
/var/lib/pcp/pmdas/bash/test-trace.sh
%dir /var/lib/pcp/pmdas/bind2
%doc /var/lib/pcp/pmdas/bind2/README.md
%attr(755,root,root) /var/lib/pcp/pmdas/bind2/Install
%attr(755,root,root) /var/lib/pcp/pmdas/bind2/Remove
/var/lib/pcp/pmdas/bind2/bind2.conf
/var/lib/pcp/pmdas/bind2/pmdabind2.pl
%dir /var/lib/pcp/pmdas/bonding
%attr(755,root,root) /var/lib/pcp/pmdas/bonding/Install
%attr(755,root,root) /var/lib/pcp/pmdas/bonding/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/bonding/pmdabonding.pl
%dir /var/lib/pcp/pmdas/cifs
%attr(755,root,root) /var/lib/pcp/pmdas/cifs/Install
%attr(755,root,root) /var/lib/pcp/pmdas/cifs/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/cifs/pmdacifs
%attr(755,root,root) /var/lib/pcp/pmdas/cifs/pmda_cifs.so
/var/lib/pcp/pmdas/cifs/domain.h
/var/lib/pcp/pmdas/cifs/help
/var/lib/pcp/pmdas/cifs/pmns
/var/lib/pcp/pmdas/cifs/root
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
%dir /var/lib/pcp/pmdas/denki
%doc /var/lib/pcp/pmdas/denki/README
%attr(755,root,root) /var/lib/pcp/pmdas/denki/Install
%attr(755,root,root) /var/lib/pcp/pmdas/denki/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/denki/pmdadenki
%attr(755,root,root) /var/lib/pcp/pmdas/denki/pmda_denki.so
/var/lib/pcp/pmdas/denki/domain.h
/var/lib/pcp/pmdas/denki/help
/var/lib/pcp/pmdas/denki/pmns
/var/lib/pcp/pmdas/denki/root
%dir /var/lib/pcp/pmdas/dm
%attr(755,root,root) /var/lib/pcp/pmdas/dm/Install
%attr(755,root,root) /var/lib/pcp/pmdas/dm/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/dm/Upgrade
%attr(755,root,root) /var/lib/pcp/pmdas/dm/pmda_dm.so
%attr(755,root,root) /var/lib/pcp/pmdas/dm/pmdadm
/var/lib/pcp/pmdas/dm/domain.h
/var/lib/pcp/pmdas/dm/help
/var/lib/pcp/pmdas/dm/pmns.dmcache
/var/lib/pcp/pmdas/dm/pmns.dmstats
/var/lib/pcp/pmdas/dm/pmns.dmthin
/var/lib/pcp/pmdas/dm/pmns.vdo
/var/lib/pcp/pmdas/dm/root
%dir /var/lib/pcp/pmdas/docker
%attr(755,root,root) /var/lib/pcp/pmdas/docker/Install
%attr(755,root,root) /var/lib/pcp/pmdas/docker/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/docker/pmda_docker.so
%attr(755,root,root) /var/lib/pcp/pmdas/docker/pmdadocker
/var/lib/pcp/pmdas/docker/domain.h
/var/lib/pcp/pmdas/docker/help
/var/lib/pcp/pmdas/docker/pmns
/var/lib/pcp/pmdas/docker/root
%dir /var/lib/pcp/pmdas/ds389
%attr(755,root,root) /var/lib/pcp/pmdas/ds389/Install
%attr(755,root,root) /var/lib/pcp/pmdas/ds389/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/ds389/pmdads389.pl
/var/lib/pcp/pmdas/ds389/ds389.conf.example
%dir /var/lib/pcp/pmdas/ds389log
%attr(755,root,root) /var/lib/pcp/pmdas/ds389log/Install
%attr(755,root,root) /var/lib/pcp/pmdas/ds389log/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/ds389log/pmdads389log.pl
%dir /var/lib/pcp/pmdas/elasticsearch
%attr(755,root,root) /var/lib/pcp/pmdas/elasticsearch/Install
%attr(755,root,root) /var/lib/pcp/pmdas/elasticsearch/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/elasticsearch/Upgrade
%attr(755,root,root) /var/lib/pcp/pmdas/elasticsearch/pmdaelasticsearch.python
/var/lib/pcp/pmdas/elasticsearch/elasticsearch.conf
%dir /var/lib/pcp/pmdas/farm
%attr(755,root,root) /var/lib/pcp/pmdas/farm/Install
%attr(755,root,root) /var/lib/pcp/pmdas/farm/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/farm/pmdafarm
%attr(755,root,root) /var/lib/pcp/pmdas/farm/pmda_farm.so
/var/lib/pcp/pmdas/farm/domain.h
/var/lib/pcp/pmdas/farm/help
/var/lib/pcp/pmdas/farm/pmns
/var/lib/pcp/pmdas/farm/root
%dir /var/lib/pcp/pmdas/gfs2
%attr(755,root,root) /var/lib/pcp/pmdas/gfs2/Install
%attr(755,root,root) /var/lib/pcp/pmdas/gfs2/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/gfs2/pmdagfs2
%attr(755,root,root) /var/lib/pcp/pmdas/gfs2/pmda_gfs2.so
/var/lib/pcp/pmdas/gfs2/domain.h
/var/lib/pcp/pmdas/gfs2/help
/var/lib/pcp/pmdas/gfs2/pmns
/var/lib/pcp/pmdas/gfs2/root
%dir /var/lib/pcp/pmdas/gluster
%attr(755,root,root) /var/lib/pcp/pmdas/gluster/Install
%attr(755,root,root) /var/lib/pcp/pmdas/gluster/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/gluster/pmdagluster.python
%dir /var/lib/pcp/pmdas/gpfs
%attr(755,root,root) /var/lib/pcp/pmdas/gpfs/Install
%attr(755,root,root) /var/lib/pcp/pmdas/gpfs/Remove
/var/lib/pcp/pmdas/gpfs/pmdagpfs.pl
%dir /var/lib/pcp/pmdas/gpsd
%attr(755,root,root) /var/lib/pcp/pmdas/gpsd/Install
%attr(755,root,root) /var/lib/pcp/pmdas/gpsd/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/gpsd/pmdagpsd.pl
%dir /var/lib/pcp/pmdas/hacluster
%attr(755,root,root) /var/lib/pcp/pmdas/hacluster/Install
%attr(755,root,root) /var/lib/pcp/pmdas/hacluster/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/hacluster/pmdahacluster
%attr(755,root,root) /var/lib/pcp/pmdas/hacluster/pmda_hacluster.so
/var/lib/pcp/pmdas/hacluster/domain.h
/var/lib/pcp/pmdas/hacluster/help
/var/lib/pcp/pmdas/hacluster/pmns
/var/lib/pcp/pmdas/hacluster/root
%dir /var/lib/pcp/pmdas/haproxy
%attr(755,root,root) /var/lib/pcp/pmdas/haproxy/Install
%attr(755,root,root) /var/lib/pcp/pmdas/haproxy/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/haproxy/connect
%attr(755,root,root) /var/lib/pcp/pmdas/haproxy/pmdahaproxy.python
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/haproxy/haproxy.conf
%dir /var/lib/pcp/pmdas/infiniband
%attr(755,root,root) /var/lib/pcp/pmdas/infiniband/Install
%attr(755,root,root) /var/lib/pcp/pmdas/infiniband/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/infiniband/Upgrade
%attr(755,root,root) /var/lib/pcp/pmdas/infiniband/pmdaib
/var/lib/pcp/pmdas/infiniband/domain.h
/var/lib/pcp/pmdas/infiniband/help
/var/lib/pcp/pmdas/infiniband/pmns
/var/lib/pcp/pmdas/infiniband/root
%dir /var/lib/pcp/pmdas/jbd2
%attr(755,root,root) /var/lib/pcp/pmdas/jbd2/Install
%attr(755,root,root) /var/lib/pcp/pmdas/jbd2/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/jbd2/pmdajbd2
%attr(755,root,root) /var/lib/pcp/pmdas/jbd2/pmda_jbd2.so
/var/lib/pcp/pmdas/jbd2/domain.h
/var/lib/pcp/pmdas/jbd2/help
/var/lib/pcp/pmdas/jbd2/help.dir
/var/lib/pcp/pmdas/jbd2/help.pag
/var/lib/pcp/pmdas/jbd2/root
/var/lib/pcp/pmdas/jbd2/root_jbd2
%dir /var/lib/pcp/pmdas/json
%doc /var/lib/pcp/pmdas/json/README
%attr(755,root,root) /var/lib/pcp/pmdas/json/Install
%attr(755,root,root) /var/lib/pcp/pmdas/json/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/json/generate_ceph_metadata
%attr(755,root,root) /var/lib/pcp/pmdas/json/pmdajson.python
/var/lib/pcp/pmdas/json/config.json
%dir /var/lib/pcp/pmdas/kvm
%attr(755,root,root) /var/lib/pcp/pmdas/kvm/Install
%attr(755,root,root) /var/lib/pcp/pmdas/kvm/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/kvm/Upgrade
%attr(755,root,root) /var/lib/pcp/pmdas/kvm/pmda_kvm.so
%attr(755,root,root) /var/lib/pcp/pmdas/kvm/pmdakvm
/var/lib/pcp/pmdas/kvm/domain.h
/var/lib/pcp/pmdas/kvm/help
/var/lib/pcp/pmdas/kvm/help.dir
/var/lib/pcp/pmdas/kvm/help.pag
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/kvm/kvm.conf
/var/lib/pcp/pmdas/kvm/root
/var/lib/pcp/pmdas/kvm/root_kvm
%dir /var/lib/pcp/pmdas/linux
%attr(755,root,root) /var/lib/pcp/pmdas/linux/pmdalinux
%attr(755,root,root) /var/lib/pcp/pmdas/linux/pmda_linux.so
/var/lib/pcp/pmdas/linux/domain.h
/var/lib/pcp/pmdas/linux/help*
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/linux/samplebandwidth.conf
%dir /var/lib/pcp/pmdas/lmsensors
%doc /var/lib/pcp/pmdas/lmsensors/README
%attr(755,root,root) /var/lib/pcp/pmdas/lmsensors/Install
%attr(755,root,root) /var/lib/pcp/pmdas/lmsensors/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/lmsensors/pmdalmsensors.python
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
%dir /var/lib/pcp/pmdas/lustre
%attr(755,root,root) /var/lib/pcp/pmdas/lustre/Install
%attr(755,root,root) /var/lib/pcp/pmdas/lustre/Remove
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/lustre/lustre.conf
/var/lib/pcp/pmdas/lustre/pmdalustre.pl
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
%dir /var/lib/pcp/pmdas/mic
%attr(755,root,root) /var/lib/pcp/pmdas/mic/Install
%attr(755,root,root) /var/lib/pcp/pmdas/mic/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/mic/pmdamic.python
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
%attr(755,root,root) /var/lib/pcp/pmdas/mysql/README
%attr(755,root,root) /var/lib/pcp/pmdas/mysql/Install
%attr(755,root,root) /var/lib/pcp/pmdas/mysql/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/mysql/pmdamysql.pl
%dir /var/lib/pcp/pmdas/named
%attr(755,root,root) /var/lib/pcp/pmdas/named/Install
%attr(755,root,root) /var/lib/pcp/pmdas/named/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/named/pmdanamed.pl
%dir /var/lib/pcp/pmdas/netcheck
%attr(755,root,root) /var/lib/pcp/pmdas/netcheck/Install
%attr(755,root,root) /var/lib/pcp/pmdas/netcheck/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/netcheck/pmdanetcheck.python
%attr(755,root,root) /var/lib/pcp/pmdas/netcheck/pmdautil.python
%attr(755,root,root) /var/lib/pcp/pmdas/netcheck/pyprep
%dir /var/lib/pcp/pmdas/nutcracker
%attr(755,root,root) /var/lib/pcp/pmdas/nutcracker/Install
%attr(755,root,root) /var/lib/pcp/pmdas/nutcracker/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/nutcracker/pmdanutcracker.pl
/var/lib/pcp/pmdas/nutcracker/nutcracker.conf
%dir /var/lib/pcp/pmdas/netcheck/modules
/var/lib/pcp/pmdas/netcheck/modules/__init__.python
/var/lib/pcp/pmdas/netcheck/modules/dns_lookup.python
/var/lib/pcp/pmdas/netcheck/modules/dns_reverse.python
/var/lib/pcp/pmdas/netcheck/modules/pcpnetcheck.python
/var/lib/pcp/pmdas/netcheck/modules/ping.python
/var/lib/pcp/pmdas/netcheck/modules/ping_latency.python
/var/lib/pcp/pmdas/netcheck/modules/ping_loss.python
/var/lib/pcp/pmdas/netcheck/modules/port_open.python
/var/lib/pcp/pmdas/netcheck/modules/url_get.python
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/netcheck/netcheck.conf
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
%dir /var/lib/pcp/pmdas/nfsclient
%attr(755,root,root) /var/lib/pcp/pmdas/nfsclient/Install
%attr(755,root,root) /var/lib/pcp/pmdas/nfsclient/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/nfsclient/Upgrade
%attr(755,root,root) /var/lib/pcp/pmdas/nfsclient/pmdanfsclient.python
%dir /var/lib/pcp/pmdas/nginx
%attr(755,root,root) /var/lib/pcp/pmdas/nginx/Install
%attr(755,root,root) /var/lib/pcp/pmdas/nginx/Remove
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/nginx/nginx.conf
%attr(755,root,root) /var/lib/pcp/pmdas/nginx/pmdanginx.pl
%dir /var/lib/pcp/pmdas/nvidia
%attr(755,root,root) /var/lib/pcp/pmdas/nvidia/README
%attr(755,root,root) /var/lib/pcp/pmdas/nvidia/Install
%attr(755,root,root) /var/lib/pcp/pmdas/nvidia/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/nvidia/pmda_nvidia.so
%attr(755,root,root) /var/lib/pcp/pmdas/nvidia/pmdanvidia
/var/lib/pcp/pmdas/nvidia/domain.h
/var/lib/pcp/pmdas/nvidia/help
/var/lib/pcp/pmdas/nvidia/pmns
/var/lib/pcp/pmdas/nvidia/root
%dir /var/lib/pcp/pmdas/openmetrics
/var/lib/pcp/pmdas/openmetrics/config.d
%attr(755,root,root) /var/lib/pcp/pmdas/openmetrics/Install
%attr(755,root,root) /var/lib/pcp/pmdas/openmetrics/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/openmetrics/Upgrade
%attr(755,root,root) /var/lib/pcp/pmdas/openmetrics/pmdaopenmetrics.python
%dir /var/lib/pcp/pmdas/openvswitch
%attr(755,root,root) /var/lib/pcp/pmdas/openvswitch/Install
%attr(755,root,root) /var/lib/pcp/pmdas/openvswitch/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/openvswitch/pmdaopenvswitch.python
%dir /var/lib/pcp/pmdas/oracle
%attr(755,root,root) /var/lib/pcp/pmdas/oracle/Install
%attr(755,root,root) /var/lib/pcp/pmdas/oracle/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/oracle/connect.pl
/var/lib/pcp/pmdas/oracle/pmdaoracle.pl
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/oracle/sample.conf
%dir /var/lib/pcp/pmdas/overhead
%doc /var/lib/pcp/pmdas/overhead/README
%attr(755,root,root) /var/lib/pcp/pmdas/overhead/Install
%attr(755,root,root) /var/lib/pcp/pmdas/overhead/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/overhead/pmdaoverhead
/var/lib/pcp/pmdas/overhead/default.conf
/var/lib/pcp/pmdas/overhead/domain.h
/var/lib/pcp/pmdas/overhead/pmns
/var/lib/pcp/pmdas/overhead/root
/var/lib/pcp/pmdas/overhead/sample.conf
%dir /var/lib/pcp/pmdas/pdns
%attr(755,root,root) /var/lib/pcp/pmdas/pdns/Install
%attr(755,root,root) /var/lib/pcp/pmdas/pdns/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/pdns/pmdapdns.pl
%dir /var/lib/pcp/pmdas/perfevent
%attr(755,root,root) /var/lib/pcp/pmdas/perfevent/Install
%attr(755,root,root) /var/lib/pcp/pmdas/perfevent/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/perfevent/Upgrade
%attr(755,root,root) /var/lib/pcp/pmdas/perfevent/perfalloc
%attr(755,root,root) /var/lib/pcp/pmdas/perfevent/perfevent-makerewrite.pl
%attr(755,root,root) /var/lib/pcp/pmdas/perfevent/pmdaperfevent
%attr(755,root,root) /var/lib/pcp/pmdas/perfevent/pmda_perfevent.so
/var/lib/pcp/pmdas/perfevent/domain.h
/var/lib/pcp/pmdas/perfevent/help
/var/lib/pcp/pmdas/perfevent/perfevent.conf
/var/lib/pcp/pmdas/perfevent/pmns
/var/lib/pcp/pmdas/perfevent/root
%dir /var/lib/pcp/pmdas/pipe
%doc /var/lib/pcp/pmdas/pipe/README
%attr(755,root,root) /var/lib/pcp/pmdas/pipe/Install
%attr(755,root,root) /var/lib/pcp/pmdas/pipe/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/pipe/pmdapipe
/var/lib/pcp/pmdas/pipe/domain.h
/var/lib/pcp/pmdas/pipe/help
/var/lib/pcp/pmdas/pipe/pmns
/var/lib/pcp/pmdas/pipe/root
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/pipe/sample.conf
%dir /var/lib/pcp/pmdas/podman
%attr(755,root,root) /var/lib/pcp/pmdas/podman/Install
%attr(755,root,root) /var/lib/pcp/pmdas/podman/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/podman/pmdapodman
%attr(755,root,root) /var/lib/pcp/pmdas/podman/pmda_podman.so
/var/lib/pcp/pmdas/podman/domain.h
/var/lib/pcp/pmdas/podman/help
/var/lib/pcp/pmdas/podman/pmns
/var/lib/pcp/pmdas/podman/root
%dir /var/lib/pcp/pmdas/pmcd
%attr(755,root,root) /var/lib/pcp/pmdas/pmcd/pmda_pmcd.so
/var/lib/pcp/pmdas/pmcd/help.*
%dir /var/lib/pcp/pmdas/postgresql
%attr(755,root,root) /var/lib/pcp/pmdas/postgresql/Install
%attr(755,root,root) /var/lib/pcp/pmdas/postgresql/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/postgresql/Upgrade
%attr(755,root,root) /var/lib/pcp/pmdas/postgresql/pmdapostgresql.python
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/postgresql/pmdapostgresql.conf
%dir /var/lib/pcp/pmdas/proc
%attr(755,root,root) /var/lib/pcp/pmdas/proc/Install
%attr(755,root,root) /var/lib/pcp/pmdas/proc/Remove
/var/lib/pcp/pmdas/proc/help.dir
/var/lib/pcp/pmdas/proc/help.pag
%attr(755,root,root) /var/lib/pcp/pmdas/proc/pmdaproc
%attr(755,root,root) /var/lib/pcp/pmdas/proc/pmda_proc.so
/var/lib/pcp/pmdas/proc/domain.h
/var/lib/pcp/pmdas/proc/help
/var/lib/pcp/pmdas/proc/root
/var/lib/pcp/pmdas/proc/root_proc
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/proc/samplehotproc.conf
%dir /var/lib/pcp/pmdas/rabbitmq
%attr(755,root,root) /var/lib/pcp/pmdas/rabbitmq/Install
%attr(755,root,root) /var/lib/pcp/pmdas/rabbitmq/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/rabbitmq/pmdarabbitmq.python
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/rabbitmq/rabbitmq.conf
%dir /var/lib/pcp/pmdas/redis
%attr(755,root,root) /var/lib/pcp/pmdas/redis/Install
%attr(755,root,root) /var/lib/pcp/pmdas/redis/Remove
/var/lib/pcp/pmdas/redis/pmdaredis.pl
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/redis/redis.conf
%dir /var/lib/pcp/pmdas/roomtemp
%doc /var/lib/pcp/pmdas/roomtemp/README
%attr(755,root,root) /var/lib/pcp/pmdas/roomtemp/Install
%attr(755,root,root) /var/lib/pcp/pmdas/roomtemp/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/roomtemp/pmdaroomtemp
/var/lib/pcp/pmdas/roomtemp/domain.h
/var/lib/pcp/pmdas/roomtemp/help
/var/lib/pcp/pmdas/roomtemp/pmns
/var/lib/pcp/pmdas/roomtemp/root
%dir /var/lib/pcp/pmdas/root
%attr(755,root,root) /var/lib/pcp/pmdas/root/pmdaroot
/var/lib/pcp/pmdas/root/domain.h
/var/lib/pcp/pmdas/root/help
/var/lib/pcp/pmdas/root/help.dir
/var/lib/pcp/pmdas/root/help.pag
/var/lib/pcp/pmdas/root/root
/var/lib/pcp/pmdas/root/root_root
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
%attr(755,root,root) /var/lib/pcp/pmdas/sample/pmda_sample.so
%attr(755,root,root) /var/lib/pcp/pmdas/sample/pmdasample
/var/lib/pcp/pmdas/sample/Makefile
/var/lib/pcp/pmdas/sample/domain.h
/var/lib/pcp/pmdas/sample/events.[ch]
/var/lib/pcp/pmdas/sample/libpcp.h
/var/lib/pcp/pmdas/sample/percontext.[ch]
/var/lib/pcp/pmdas/sample/pmda.c
/var/lib/pcp/pmdas/sample/proc.[ch]
/var/lib/pcp/pmdas/sample/sample.c
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
%attr(755,root,root) /var/lib/pcp/pmdas/simple/pmdasimple.perl
%attr(755,root,root) /var/lib/pcp/pmdas/simple/pmdasimple.python
/var/lib/pcp/pmdas/simple/domain.h
/var/lib/pcp/pmdas/simple/help
/var/lib/pcp/pmdas/simple/pmns
/var/lib/pcp/pmdas/simple/root
/var/lib/pcp/pmdas/simple/Makefile
/var/lib/pcp/pmdas/simple/simple.c
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/simple/simple.conf
%dir /var/lib/pcp/pmdas/slurm
%attr(755,root,root) /var/lib/pcp/pmdas/slurm/Install
%attr(755,root,root) /var/lib/pcp/pmdas/slurm/Remove
/var/lib/pcp/pmdas/slurm/pmdaslurm.pl
%dir /var/lib/pcp/pmdas/smart
%attr(755,root,root) /var/lib/pcp/pmdas/smart/Install
%attr(755,root,root) /var/lib/pcp/pmdas/smart/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/smart/pmda_smart.so
%attr(755,root,root) /var/lib/pcp/pmdas/smart/pmdasmart
/var/lib/pcp/pmdas/smart/domain.h
/var/lib/pcp/pmdas/smart/help
/var/lib/pcp/pmdas/smart/pmns
/var/lib/pcp/pmdas/smart/root
%dir /var/lib/pcp/pmdas/snmp
%attr(755,root,root) /var/lib/pcp/pmdas/snmp/Install
%attr(755,root,root) /var/lib/pcp/pmdas/snmp/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/snmp/pmdasnmp.pl
/var/lib/pcp/pmdas/snmp/snmp.conf
%dir /var/lib/pcp/pmdas/sockets
%attr(755,root,root) /var/lib/pcp/pmdas/sockets/Install
%attr(755,root,root) /var/lib/pcp/pmdas/sockets/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/sockets/Upgrade
%attr(755,root,root) /var/lib/pcp/pmdas/sockets/pmdasockets
%attr(755,root,root) /var/lib/pcp/pmdas/sockets/pmda_sockets.so
/var/lib/pcp/pmdas/sockets/domain.h
/var/lib/pcp/pmdas/sockets/filter.conf
/var/lib/pcp/pmdas/sockets/help
/var/lib/pcp/pmdas/sockets/pmns
/var/lib/pcp/pmdas/sockets/root
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
%dir /var/lib/pcp/pmdas/systemd
%doc /var/lib/pcp/pmdas/systemd/README
%attr(755,root,root) /var/lib/pcp/pmdas/systemd/Install
%attr(755,root,root) /var/lib/pcp/pmdas/systemd/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/systemd/pmdasystemd
/var/lib/pcp/pmdas/systemd/domain.h
/var/lib/pcp/pmdas/systemd/help
/var/lib/pcp/pmdas/systemd/pmns
/var/lib/pcp/pmdas/systemd/root
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
%attr(755,root,root) /var/lib/pcp/pmdas/trivial/pmdatrivial.perl
%attr(755,root,root) /var/lib/pcp/pmdas/trivial/pmdatrivial.python
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
%attr(755,root,root) /var/lib/pcp/pmdas/txmon/genload
/var/lib/pcp/pmdas/txmon/domain.h
/var/lib/pcp/pmdas/txmon/help
/var/lib/pcp/pmdas/txmon/pmns
/var/lib/pcp/pmdas/txmon/root
/var/lib/pcp/pmdas/txmon/Makefile
/var/lib/pcp/pmdas/txmon/txmon.c
/var/lib/pcp/pmdas/txmon/txmon.h
/var/lib/pcp/pmdas/txmon/txrecord.c
%dir /var/lib/pcp/pmdas/unbound
%attr(755,root,root) /var/lib/pcp/pmdas/unbound/Install
%attr(755,root,root) /var/lib/pcp/pmdas/unbound/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/unbound/pmdaunbound.python
%dir /var/lib/pcp/pmdas/uwsgi
%attr(755,root,root) /var/lib/pcp/pmdas/uwsgi/Install
%attr(755,root,root) /var/lib/pcp/pmdas/uwsgi/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/uwsgi/pmdauwsgi.python
/var/lib/pcp/pmdas/uwsgi/uwsgi.conf
%dir /var/lib/pcp/pmdas/weblog
%doc /var/lib/pcp/pmdas/weblog/README
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/Install
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/check_match
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/pmdaweblog
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/server.sh
%attr(755,root,root) /var/lib/pcp/pmdas/weblog/weblogconv.sh
/var/lib/pcp/pmdas/weblog/domain.h
/var/lib/pcp/pmdas/weblog/help
/var/lib/pcp/pmdas/weblog/pmns
/var/lib/pcp/pmdas/weblog/root
%dir /var/lib/pcp/pmdas/xfs
%attr(755,root,root) /var/lib/pcp/pmdas/xfs/Install
%attr(755,root,root) /var/lib/pcp/pmdas/xfs/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/xfs/pmda_xfs.so
%attr(755,root,root) /var/lib/pcp/pmdas/xfs/pmdaxfs
/var/lib/pcp/pmdas/xfs/domain.h
/var/lib/pcp/pmdas/xfs/help
/var/lib/pcp/pmdas/xfs/help.dir
/var/lib/pcp/pmdas/xfs/help.pag
/var/lib/pcp/pmdas/xfs/root
/var/lib/pcp/pmdas/xfs/root_xfs
%dir /var/lib/pcp/pmdas/zfs
%attr(755,root,root) /var/lib/pcp/pmdas/zfs/Install
%attr(755,root,root) /var/lib/pcp/pmdas/zfs/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/zfs/pmda_zfs.so
%attr(755,root,root) /var/lib/pcp/pmdas/zfs/pmdazfs
/var/lib/pcp/pmdas/zfs/domain.h
/var/lib/pcp/pmdas/zfs/help
/var/lib/pcp/pmdas/zfs/pmns
/var/lib/pcp/pmdas/zfs/root
%dir /var/lib/pcp/pmdas/zimbra
%attr(755,root,root) /var/lib/pcp/pmdas/zimbra/Install
%attr(755,root,root) /var/lib/pcp/pmdas/zimbra/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/zimbra/pmdazimbra.pl
%attr(755,root,root) /var/lib/pcp/pmdas/zimbra/runaszimbra
%attr(755,root,root) /var/lib/pcp/pmdas/zimbra/zimbraprobe
%dir /var/lib/pcp/pmdas/zswap
%attr(755,root,root) /var/lib/pcp/pmdas/zswap/Install
%attr(755,root,root) /var/lib/pcp/pmdas/zswap/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/zswap/pmdazswap.python
%dir /var/lib/pcp/pmns
/var/lib/pcp/pmns/root_root
%attr(775,pcp,pcp) %dir /var/lib/pcp/tmp
%attr(775,pcp,pcp) %dir /var/lib/pcp/tmp/pmie
%attr(775,pcp,pcp) %dir /var/lib/pcp/tmp/pmlogger
%attr(775,pcp,pcp) %dir /var/log/pcp
%dir /var/log/pcp/pmcd
%attr(775,pcp,pcp) %dir /var/log/pcp/pmfind
%attr(775,pcp,pcp) %dir /var/log/pcp/pmie
%attr(775,pcp,pcp) %dir /var/log/pcp/pmlogger
%attr(775,pcp,pcp) %dir /var/log/pcp/pmproxy
%{zsh_compdir}/_pcp
%{_mandir}/man1/KERNEL_PMDAS.1*
%{_mandir}/man1/PCP_KUBE_PODS.1*
%{_mandir}/man1/PCPCompat.1*
%{_mandir}/man1/PCPIntro.1*
%{_mandir}/man1/chkhelp.1*
%{_mandir}/man1/collectl2pcp.1*
%{_mandir}/man1/dbpmda.1*
%{_mandir}/man1/dbprobe.1*
%{_mandir}/man1/find-filter.1*
%{_mandir}/man1/ganglia2pcp.1*
%{_mandir}/man1/genload.1*
%{_mandir}/man1/genpmda.1*
%{_mandir}/man1/indomcachectl.1*
%{_mandir}/man1/iostat2pcp.1*
%{_mandir}/man1/mkaf.1*
%{_mandir}/man1/mrtg2pcp.1*
%{_mandir}/man1/pcp.1*
%{_mandir}/man1/pcp2elasticsearch.1*
%{_mandir}/man1/pcp2graphite.1*
%{_mandir}/man1/pcp2influxdb.1*
%{_mandir}/man1/pcp2json.1*
%{_mandir}/man1/pcp2spark.1*
%{_mandir}/man1/pcp2xml.1*
%{_mandir}/man1/pcp-atop.1*
%{_mandir}/man1/pcp-atopsar.1*
%{_mandir}/man1/pcp-buddyinfo.1*
%{_mandir}/man1/pcp-check.1*
%{_mandir}/man1/pcp-collectl.1*
%{_mandir}/man1/pcp-dmcache.1*
%{_mandir}/man1/pcp-dstat.1*
%{_mandir}/man1/pcp-free.1*
%{_mandir}/man1/pcp-geolocate.1*
%{_mandir}/man1/pcp-htop.1*
%{_mandir}/man1/pcp-iostat.1*
%{_mandir}/man1/pcp-ipcs.1*
%{_mandir}/man1/pcp-kube-pods.1*
%{_mandir}/man1/pcp-lvmcache.1
%{_mandir}/man1/pcp-meminfo.1*
%{_mandir}/man1/pcp-mpstat.1*
%{_mandir}/man1/pcp-netstat.1*
%{_mandir}/man1/pcp-numastat.1*
%{_mandir}/man1/pcp-pidstat.1*
%{_mandir}/man1/pcp-ps.1*
%{_mandir}/man1/pcp-python.1*
%{_mandir}/man1/pcp-reboot-init.1*
%{_mandir}/man1/pcp-shping.1*
%{_mandir}/man1/pcp-slabinfo.1*
%{_mandir}/man1/pcp-ss.1*
%{_mandir}/man1/pcp-summary.1*
%{_mandir}/man1/pcp-tapestat.1*
%{_mandir}/man1/pcp-uptime.1*
%{_mandir}/man1/pcp-verify.1*
%{_mandir}/man1/pcp-vmstat.1*
%{_mandir}/man1/pcp-xsos.1*
%{_mandir}/man1/pcp-zoneinfo.1*
%{_mandir}/man1/pcp2csv.1*
%{_mandir}/man1/pcp2openmetrics.1*
%{_mandir}/man1/pcp2zabbix.1*
%{_mandir}/man1/perfalloc.1*
%{_mandir}/man1/pmafm.1*
%{_mandir}/man1/pmcd.1*
%{_mandir}/man1/pmcd_wait.1*
%{_mandir}/man1/pmclient.1*
%{_mandir}/man1/pmclient_fg.1
%{_mandir}/man1/pmconfig.1*
%{_mandir}/man1/pmdaactivemq.1*
%{_mandir}/man1/pmdaamdgpu.1*
%{_mandir}/man1/pmdaapache.1*
%{_mandir}/man1/pmdabash.1*
%{_mandir}/man1/pmdabcc.1*
%{_mandir}/man1/pmdabind2.1*
%{_mandir}/man1/pmdabonding.1*
%{_mandir}/man1/pmdabpftrace.1*
%{_mandir}/man1/pmdacifs.1*
%{_mandir}/man1/pmdacisco.1*
%{_mandir}/man1/pmdadbping.1*
%{_mandir}/man1/pmdadenki.1*
%{_mandir}/man1/pmdadm.1*
%{_mandir}/man1/pmdadocker.1*
%{_mandir}/man1/pmdads389.1*
%{_mandir}/man1/pmdads389log.1*
%{_mandir}/man1/pmdaelasticsearch.1*
%{_mandir}/man1/pmdafarm.1*
%{_mandir}/man1/pmdagfs2.1*
%{_mandir}/man1/pmdagluster.1*
%{_mandir}/man1/pmdagpfs.1*
%{_mandir}/man1/pmdagpsd.1*
%{_mandir}/man1/pmdahacluster.1*
%{_mandir}/man1/pmdahaproxy.1*
%{_mandir}/man1/pmdaib.1*
%{_mandir}/man1/pmdajbd2.1*
%{_mandir}/man1/pmdajson.1*
%{_mandir}/man1/pmdakernel.1*
%{_mandir}/man1/pmdakvm.1*
%{_mandir}/man1/pmdalibvirt.1*
%{_mandir}/man1/pmdalinux.1*
%{_mandir}/man1/pmdalio.1*
%{_mandir}/man1/pmdalmsensors.1*
%{_mandir}/man1/pmdalogger.1*
%{_mandir}/man1/pmdalustre.1*
%{_mandir}/man1/pmdalustrecomm.1*
%{_mandir}/man1/pmdamailq.1*
%{_mandir}/man1/pmdamemcache.1*
%{_mandir}/man1/pmdamic.1*
%{_mandir}/man1/pmdammv.1*
%{_mandir}/man1/pmdamongodb.1*
%{_mandir}/man1/pmdamounts.1*
%{_mandir}/man1/pmdamssql.1*
%{_mandir}/man1/pmdamysql.1*
%{_mandir}/man1/pmdanamed.1*
%{_mandir}/man1/pmdanetcheck.1*
%{_mandir}/man1/pmdanetfilter.1*
%{_mandir}/man1/pmdanews.1*
%{_mandir}/man1/pmdanfsclient.1*
%{_mandir}/man1/pmdanginx.1*
%{_mandir}/man1/pmdanutcracker.1*
%{_mandir}/man1/pmdanvidia.1*
%{_mandir}/man1/pmdaopenmetrics.1*
%{_mandir}/man1/pmdaopenvswitch.1*
%{_mandir}/man1/pmdaoracle.1*
%{_mandir}/man1/pmdaoverhead.1*
%{_mandir}/man1/pmdapdns.1*
%{_mandir}/man1/pmdaperfevent.1*
%{_mandir}/man1/pmdapipe.1*
%{_mandir}/man1/pmdapodman.1*
%{_mandir}/man1/pmdapostfix.1*
%{_mandir}/man1/pmdapostgresql.1*
%{_mandir}/man1/pmdaproc.1*
%{_mandir}/man1/pmdarabbitmq.1*
%{_mandir}/man1/pmdaredis.1*
%{_mandir}/man1/pmdaresctrl.1*
%{_mandir}/man1/pmdaroomtemp.1*
%{_mandir}/man1/pmdaroot.1*
%{_mandir}/man1/pmdarsyslog.1*
%{_mandir}/man1/pmdasamba.1*
%{_mandir}/man1/pmdasample.1*
%{_mandir}/man1/pmdasendmail.1*
%{_mandir}/man1/pmdashping.1*
%{_mandir}/man1/pmdasimple.1*
%{_mandir}/man1/pmdaslurm.1*
%{_mandir}/man1/pmdasmart.1*
%{_mandir}/man1/pmdasnmp.1*
%{_mandir}/man1/pmdasockets.1*
%{_mandir}/man1/pmdasummary.1*
%{_mandir}/man1/pmdasystemd.1*
%{_mandir}/man1/pmdate.1*
%{_mandir}/man1/pmdatrace.1*
%{_mandir}/man1/pmdatrivial.1*
%{_mandir}/man1/pmdatxmon.1*
%{_mandir}/man1/pmdaunbound.1*
%{_mandir}/man1/pmdauwsgi.1*
%{_mandir}/man1/pmdaweblog.1*
%{_mandir}/man1/pmdaxfs.1*
%{_mandir}/man1/pmdazfs.1*
%{_mandir}/man1/pmdazimbra.1*
%{_mandir}/man1/pmdazswap.1*
%{_mandir}/man1/pmdbg.1*
%{_mandir}/man1/pmdiff.1*
%{_mandir}/man1/pmdumplog.1*
%{_mandir}/man1/pmerr.1*
%{_mandir}/man1/pmevent.1*
%{_mandir}/man1/pmfind.1*
%{_mandir}/man1/pmfind_check.1*
%{_mandir}/man1/pmgenmap.1*
%{_mandir}/man1/pmgetopt.1*
%{_mandir}/man1/pmhostname.1*
%{_mandir}/man1/pmie.1*
%{_mandir}/man1/pmie2col.1*
%{_mandir}/man1/pmie_check.1*
%{_mandir}/man1/pmie_daily.1*
%{_mandir}/man1/pmie_dump_stats.1*
%{_mandir}/man1/pmieconf.1*
%{_mandir}/man1/pmiectl.1*
%{_mandir}/man1/pmiestatus.1*
%{_mandir}/man1/pmiostat.1*
%{_mandir}/man1/pmjson.1*
%{_mandir}/man1/pmlc.1*
%{_mandir}/man1/pmlock.1*
%{_mandir}/man1/pmlogbasename.1*
%{_mandir}/man1/pmlogcheck.1*
%{_mandir}/man1/pmlogcompress.1*
%{_mandir}/man1/pmlogconf.1*
%{_mandir}/man1/pmlogctl.1*
%{_mandir}/man1/pmlogdump.1*
%{_mandir}/man1/pmlogextract.1*
%{_mandir}/man1/pmlogger.1*
%{_mandir}/man1/pmlogger_check.1*
%{_mandir}/man1/pmlogger_daily.1*
%{_mandir}/man1/pmlogger_daily_report.1*
%{_mandir}/man1/pmlogger_merge.1*
%{_mandir}/man1/pmlogger_rewrite.1*
%{_mandir}/man1/pmloglabel.1*
%{_mandir}/man1/pmlogmv.1*
%{_mandir}/man1/pmlogpaste.1*
%{_mandir}/man1/pmlogredact.1*
%{_mandir}/man1/pmlogreduce.1*
%{_mandir}/man1/pmlogrewrite.1*
%{_mandir}/man1/pmlogsize.1*
%{_mandir}/man1/pmlogsummary.1*
%{_mandir}/man1/pmmgr.1*
%{_mandir}/man1/pmnsadd.1*
%{_mandir}/man1/pmnsdel.1*
%{_mandir}/man1/pmpause.1*
%{_mandir}/man1/pmpost.1*
%{_mandir}/man1/pmprobe.1*
%{_mandir}/man1/pmproxy.1*
%{_mandir}/man1/pmpython.1*
%{_mandir}/man1/pmrep.1*
%{_mandir}/man1/pmrepconf.1*
%{_mandir}/man1/pmsearch.1*
%{_mandir}/man1/pmseries.1*
%{_mandir}/man1/pmsignal.1*
%{_mandir}/man1/pmsleep.1*
%{_mandir}/man1/pmsocks.1*
%{_mandir}/man1/pmstat.1*
%{_mandir}/man1/pmstore.1*
%{_mandir}/man1/pmtrace.1*
%{_mandir}/man1/pmval.1*
%{_mandir}/man1/pmwebd.1*
%{_mandir}/man1/runaspcp.1*
%{_mandir}/man1/sar2pcp.1*
%{_mandir}/man1/sheet2pcp.1*
%{_mandir}/man1/telnet-probe.1*
%{_mandir}/man1/txrecord.1*
%{_mandir}/man5/LOGARCHIVE.5*
%{_mandir}/man5/PMNS.5*
%{_mandir}/man5/labels.conf.5*
%{_mandir}/man5/pcp-atoprc.5*
%{_mandir}/man5/pcp-dstat.5*
%{_mandir}/man5/pcp-htop.5*
%{_mandir}/man5/perfevent.conf.5*
%{_mandir}/man5/pmlogger.control.5*
%{_mandir}/man5/pmrep.conf.5*

%if %{with qt}
%files gui
%defattr(644,root,root,755)
%doc html
%attr(755,root,root) %{_bindir}/clustervis
%attr(755,root,root) %{_bindir}/dkvis
%attr(755,root,root) %{_bindir}/mpvis
%attr(755,root,root) %{_bindir}/nfsvis
%attr(755,root,root) %{_bindir}/osvis
%attr(755,root,root) %{_bindir}/pmchart
%attr(755,root,root) %{_bindir}/pmconfirm
%attr(755,root,root) %{_bindir}/pmdumptext
%attr(755,root,root) %{_bindir}/pmmessage
%attr(755,root,root) %{_bindir}/pmquery
%attr(755,root,root) %{_bindir}/pmtime
%attr(755,root,root) %{_bindir}/pmview
%attr(755,root,root) %{_bindir}/weblogvis
%attr(755,root,root) %{_bindir}/webpingvis
%attr(755,root,root) %{_bindir}/webvis
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmsnap
%{_libexecdir}/pcp/lib/pmview-args
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmafm/pcp-gui
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/config.clustervis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/config.dkvis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/config.mpvis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/config.nfsvis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/config.osvis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/config.weblogvis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/config.webpingvis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmlogger/config.webvis
%dir %{_sysconfdir}/pcp/pmsnap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmsnap/Snap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmsnap/control
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmsnap/crontab
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp/pmsnap/summary.html
%{_datadir}/pcp/lib/pmview-args
%{_datadir}/pcp-gui
%{_desktopdir}/pmchart.desktop
%{_iconsdir}/hicolor/*x*/apps/*.png
%{_iconsdir}/hicolor/scalable*/apps/*.svg
%{_mandir}/man1/clustervis.1*
%{_mandir}/man1/dkvis.1*
%{_mandir}/man1/mpvis.1*
%{_mandir}/man1/nfsvis.1*
%{_mandir}/man1/osvis.1*
%{_mandir}/man1/pmchart.1*
%{_mandir}/man1/pmconfirm.1*
%{_mandir}/man1/pmdumptext.1*
%{_mandir}/man1/pmmessage.1*
%{_mandir}/man1/pmquery.1*
%{_mandir}/man1/pmsnap.1*
%{_mandir}/man1/pmtime.1*
%{_mandir}/man1/pmview.1*
%{_mandir}/man1/weblogvis.1*
%{_mandir}/man1/webpingvis.1*
%{_mandir}/man1/webvis.1*
%{_mandir}/man5/pmview.5*
/var/lib/pcp/config/pmafm/pcp-gui
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/CPU
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/ApacheServer
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Disk
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Diskbytes
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/ElasticsearchServer
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Filesystem
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Loadavg
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Memory
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/NFS2
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/NFS3
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Netbytes
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Netpackets
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Overview
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/PMCD
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Paging
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Schemes
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Sockets
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Swap
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/Syscalls
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmchart/vCPU
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.clustervis
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.dkvis
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.mpvis
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.nfsvis
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.osvis
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.weblogvis
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.webpingvis
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmlogger/config.webvis
%dir /var/lib/pcp/config/pmsnap
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmsnap/Snap
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmsnap/crontab
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/config/pmsnap/summary.html
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pminfo
%attr(755,root,root) %{_libdir}/libpcp.so.3
%attr(755,root,root) %{_libdir}/libpcp_archive.so.1
%attr(755,root,root) %{_libdir}/libpcp_fault.so.3
%attr(755,root,root) %{_libdir}/libpcp_gui.so.2
%attr(755,root,root) %{_libdir}/libpcp_import.so.1
%attr(755,root,root) %{_libdir}/libpcp_mmv.so.1
%attr(755,root,root) %{_libdir}/libpcp_pmda.so.3
%attr(755,root,root) %{_libdir}/libpcp_trace.so.2
%attr(755,root,root) %{_libdir}/libpcp_web.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pcp.conf
%{_sysconfdir}/pcp.env
%dir %{_libexecdir}/pcp
%dir %{_libexecdir}/pcp/bin
%attr(755,root,root) %{_libexecdir}/pcp/bin/newhelp
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmcpp
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmlogger_rewrite
%attr(755,root,root) %{_libexecdir}/pcp/bin/pmnsmerge
%dir %{_libexecdir}/pcp/pmns
%attr(755,root,root) %{_libexecdir}/pcp/pmns/Make.stdpmid
%attr(755,root,root) %{_libexecdir}/pcp/pmns/Rebuild
%attr(755,root,root) %{_libexecdir}/pcp/pmns/ReplacePmnsSubtree
%{_libexecdir}/pcp/pmns/Makefile
%attr(755,root,root) %{_libexecdir}/pcp/pmns/lockpmns
%{_libexecdir}/pcp/pmns/root_jbd2
%{_libexecdir}/pcp/pmns/root_kvm
%{_libexecdir}/pcp/pmns/root_linux
%{_libexecdir}/pcp/pmns/root_mmv
%{_libexecdir}/pcp/pmns/root_pmcd
%{_libexecdir}/pcp/pmns/root_pmproxy
%{_libexecdir}/pcp/pmns/root_proc
%{_libexecdir}/pcp/pmns/root_root
%{_libexecdir}/pcp/pmns/root_xfs
%{_libexecdir}/pcp/pmns/stdpmid.pcp
%attr(755,root,root) %{_libexecdir}/pcp/pmns/unlockpmns
%config(noreplace) %verify(not md5 mtime size) %{_libexecdir}/pcp/pmns/stdpmid.local
%dir /var/lib/pcp
%dir /var/lib/pcp/pmns
%attr(755,root,root) /var/lib/pcp/pmns/Make.stdpmid
%attr(755,root,root) /var/lib/pcp/pmns/Rebuild
/var/lib/pcp/pmns/Makefile
/var/lib/pcp/pmns/root_jbd2
/var/lib/pcp/pmns/root_kvm
/var/lib/pcp/pmns/root_linux
/var/lib/pcp/pmns/root_mmv
/var/lib/pcp/pmns/root_pmcd
/var/lib/pcp/pmns/root_pmproxy
/var/lib/pcp/pmns/root_proc
/var/lib/pcp/pmns/root_xfs
/var/lib/pcp/pmns/stdpmid.pcp
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmns/stdpmid.local
%ghost /var/lib/pcp/pmns/stdpmid
%{_prefix}/lib/sysusers.d/pcp.conf
%{systemdtmpfilesdir}/pcp-reboot-init.conf
%{_mandir}/man1/newhelp.1*
%{_mandir}/man1/pmcpp.1*
%{_mandir}/man1/pminfo.1*
%{_mandir}/man1/pmnsmerge.1*
%{_mandir}/man5/mmv.5*
%{_mandir}/man5/pcp.conf.5*
%{_mandir}/man5/pcp.env.5*
%{_mandir}/man5/pmieconf.5*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libpcp.so
%{_libdir}/libpcp_archive.so
%{_libdir}/libpcp_fault.so
%{_libdir}/libpcp_gui.so
%{_libdir}/libpcp_import.so
%{_libdir}/libpcp_mmv.so
%{_libdir}/libpcp_pmda.so
%{_libdir}/libpcp_trace.so
%{_libdir}/libpcp_web.so
%{_includedir}/pcp
%{_mandir}/man3/LOGIMPORT.3*
%{_mandir}/man3/PCPIntro.3*
%{_mandir}/man3/PMAPI.3*
%{_mandir}/man3/PMAPI_INTERNAL.3*
%{_mandir}/man3/PMDA.3*
%{_mandir}/man3/PMWEBAPI.3*
%{_mandir}/man3/PM_FAULT_*.3*
%{_mandir}/man3/Qmc*.3*
%{_mandir}/man3/QMC.3*
%{_mandir}/man3/__pm*.3*
%{_mandir}/man3/mmv_*.3*
%{_mandir}/man3/pm*.3*
%{_pkgconfigdir}/libpcp.pc
%{_pkgconfigdir}/libpcp_archive.pc
%{_pkgconfigdir}/libpcp_import.pc
%{_pkgconfigdir}/libpcp_pmda.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpcp.a
%{_libdir}/libpcp_archive.a
%{_libdir}/libpcp_fault.a
%{_libdir}/libpcp_gui.a
%{_libdir}/libpcp_import.a
%{_libdir}/libpcp_mmv.a
%{_libdir}/libpcp_pmda.a
%{_libdir}/libpcp_trace.a
%{_libdir}/libpcp_web.a

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
%attr(755,root,root) %{py_sitedir}/cmmv.so
%attr(755,root,root) %{py_sitedir}/cpmapi.so
%attr(755,root,root) %{py_sitedir}/cpmda.so
%attr(755,root,root) %{py_sitedir}/cpmgui.so
%attr(755,root,root) %{py_sitedir}/cpmi.so
%dir %{py_sitedir}/pcp
%{py_sitedir}/pcp/*.py[co]
%{py_sitedir}/pcp-*-py*.egg-info

%files -n python3-pcp
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/cmmv.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/cpmapi.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/cpmda.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/cpmgui.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/cpmi.cpython-*.so
%dir %{py3_sitedir}/pcp
%{py3_sitedir}/pcp/*.py
%{py3_sitedir}/pcp/__pycache__
%{py3_sitedir}/pcp-*-py*.egg-info

%files -n bash-completion-pcp
%defattr(644,root,root,755)
/etc/bash_completion.d/pcp

%if %{with systemtap}
%files -n systemtap-pcp
%defattr(644,root,root,755)
%{_datadir}/systemtap/tapset/pmcd.stp
%endif

# TODO: zabbix-???-pcp
#%attr(755,root,root) %{_libdir}/zabbix/agent/zbxpcp.so
#%attr(755,root,root) %{_libdir}/zabbix/modules/zbxpcp.so
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix/zabbix_agentd.d/zbxpcp.conf
#%{_mandir}/man3/zbxpcp.3*
