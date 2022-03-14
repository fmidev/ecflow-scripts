%define distnum %(/usr/lib/rpm/redhat/dist.sh --distnum)

%define PACKAGENAME ecflow-scripts
Name:           %{PACKAGENAME}
Version:        22.3.14
Release:        1%{dist}.fmi
Summary:        Helper scripts needed for ecFlow production
Group:          Applications/System
License:        MIT
URL:            http://www.fmi.fi
Source0: 	%{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       python3
Requires:	openshift-origin-client-tools
Requires:	bash
Requires:	coreutils
Requires:	python3-psycopg2

%if %{defined el8}
Requires:	python3-pytz
%else if %{defined el7}
Requires:	python36-pytz
%endif

Provides:	oc-wait.sh
Provides:	qdserverfunction.linux
Provides:	remoterun.cluster
Provides:	remoterun.cluster.cluster
Provides:	update_ss_forecast_status.py

AutoReqProv: no

%global debug_package %{nil}

%description
A collection of small but important scripts that keeps the
good ol' wheels of production running.

%prep
%setup -q -n "%{PACKAGENAME}"

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_bindir}
cp -a bin/oc-wait.sh %{buildroot}/%{_bindir}/
cp -a bin/qdserverfunction.linux %{buildroot}/%{_bindir}/
cp -a bin/remoterun.cluster* %{buildroot}/%{_bindir}/
cp -a bin/update_ss_forecast_status.py %{buildroot}/%{_bindir}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%{_bindir}/*

%changelog
* Thu Jan 20 2022 Mikko Partio <mikko.partio@fmi.fi> - 22.1.20-1.fmi
- Initial build
