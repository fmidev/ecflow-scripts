%define distnum %(/usr/lib/rpm/redhat/dist.sh --distnum)

%define PACKAGENAME ecflow-scripts
Name:           %{PACKAGENAME}
Version:        24.10.16
Release:        1%{dist}.fmi
Summary:        Helper scripts needed for ecFlow production
Group:          Applications/System
License:        MIT
URL:            http://www.fmi.fi
Source0: 	%{name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       python3
Requires:	openshift-origin-client-tools
Requires:	kubeprompt
Requires:	bash
Requires:	coreutils
Requires:	python3-psycopg2
Requires:	postgresql14

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
Provides:	huruakka_storetime.sh
Provides:	tail.h
Provides:	head.h

AutoReqProv: no

%global debug_package %{nil}

%description
A collection of small but important scripts that keep the
good ol' wheels of production running.

%prep
%setup -q -n "%{PACKAGENAME}"

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/etc/ecflow5
cp -a bin/oc-wait.sh %{buildroot}/%{_bindir}/
cp -a bin/qdserverfunction.linux %{buildroot}/%{_bindir}/
cp -a bin/remoterun.cluster* %{buildroot}/%{_bindir}/
cp -a bin/update_ss_forecast_status.py %{buildroot}/%{_bindir}/
cp -a bin/huruakka_storetime.sh %{buildroot}/%{_bindir}/
cp -a etc/tail.h %{buildroot}/etc/ecflow5/
cp -a etc/head.h %{buildroot}/etc/ecflow5/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%{_bindir}/oc-wait.sh
%{_bindir}/qdserverfunction.linux
%{_bindir}/remoterun.cluster
%{_bindir}/remoterun.cluster.exec
%{_bindir}/update_ss_forecast_status.py
%{_bindir}/huruakka_storetime.sh
%{_sysconfdir}/ecflow5/*.h

%changelog
* Wed Oct 16 2024 Mikko Partio <mikko.partio@fmi.fi> - 24.10.16-1.fmi
- Remove systemd service file which is now a part of ecflow5-http package
* Thu Mar 23 2023 Mikko Partio <mikko.partio@fmi.fi> - 23.3.23-1.fmi
- Fix typo in systemd service file
* Wed Mar 22 2023 Mikko Partio <mikko.partio@fmi.fi> - 23.3.22-1.fmi
- Bugfix for update_ss_forecast_status.py
* Wed Feb 22 2023 Mikko Partio <mikko.partio@fmi.fi> - 23.2.22-1.fmi
- Create systemd service file for ecflow http
* Thu Feb 16 2023 Mikko Partio <mikko.partio@fmi.fi> - 23.2.16-1.fmi
- Set USE_OC=1 by default
* Mon Feb 13 2023 Mikko Aalto <mikko.aalto@fmi.fi> - 23.2.13-1.fmi
- Add head.h and tail.h
* Thu Feb 9 2023 Mikko Aalto <mikko.aalto@fmi.fi> - 23.2.9-1.fmi
- Changes to qdserverfunction.linux
* Mon Jan 16 2023 Mikko Partio <mikko.partio@fmi.fi> - 23.1.16-1.fmi
- Change to qdserverfunction.linux oc jobname
* Thu Jan 12 2023 Mikko Partio <mikko.partio@fmi.fi> - 23.1.12-1.fmi
- Allow oc wait to be specified with a ecflow variable
* Wed Jan 11 2023 Mikko Partio <mikko.partio@fmi.fi> - 23.1.11-1.fmi
- Minor change to huruakka_storetime.sh
* Tue Jan 10 2023 Mikko Partio <mikko.partio@fmi.fi> - 23.1.10-1.fmi
- Add huruakka_storetime.sh
* Thu Mar 31 2022 Mikko Aalto <mikko.aalto@fmi.fi> - 22.3.31-1.fmi
- Increase oc-wait timeout
* Thu Jan 20 2022 Mikko Partio <mikko.partio@fmi.fi> - 22.1.20-1.fmi
- Initial build
