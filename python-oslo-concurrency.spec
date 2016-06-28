%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name oslo.concurrency
%global pkg_name oslo-concurrency

Name:           python-oslo-concurrency
Version:        2.6.1
Release:        3%{?dist}
Summary:        OpenStack Oslo concurrency library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

# %{?python_provide:%python_provide python2-%{pkg_name}}
# TEMP reverse python/python2 subpackage/provides to avoid upgrade issues
# with yum priorities
Provides: python2-%{pkg_name} = %{version}-%{release}
Obsoletes: python2-%{pkg_name} < %{version}-%{release}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
# Required for tests
BuildRequires:  python-hacking
BuildRequires:  python-oslotest
BuildRequires:  python-coverage
BuildRequires:  python-futures
BuildRequires:  python-fixtures
BuildRequires:  python-enum34
BuildRequires:  python-eventlet

Requires:       python-babel
Requires:       python-iso8601
Requires:       python-fixtures
Requires:       python-oslo-config
Requires:       python-oslo-i18n
Requires:       python-oslo-utils
Requires:       python-retrying
Requires:       python-six
Requires:       python-fasteners
Requires:       python-enum34

%package  -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo concurrency library
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-fixtures
BuildRequires:  python-oslo-utils
BuildRequires:  python-fasteners

%description -n python-%{pkg_name}-doc
Documentation for the Oslo concurrency library.

%package  -n python-%{pkg_name}-tests
Summary:    Tests for the Oslo concurrency library

Requires:  python-%{pkg_name} = %{version}-%{release}
Requires:  python-hacking
Requires:  python-oslotest
Requires:  python-coverage
Requires:  python-futures
Requires:  python-fixtures

%description -n python-%{pkg_name}-tests
Tests for the Oslo concurrency library.

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo concurrency library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# Required for tests
BuildRequires:  python3-hacking
BuildRequires:  python3-oslotest
BuildRequires:  python3-coverage
BuildRequires:  python3-fixtures
BuildRequires:  python3-eventlet

Requires:       python3-babel
Requires:       python3-iso8601
Requires:       python3-fixtures
Requires:       python3-oslo-config
Requires:       python3-oslo-i18n
Requires:       python3-oslo-utils
Requires:       python3-posix_ipc
Requires:       python3-retrying
Requires:       python3-six
Requires:       python3-fasteners

%description -n python3-%{pkg_name}
Oslo concurrency library has utilities for safely running multi-thread,
multi-process applications using locking mechanisms and for running
external processes.
%endif

%description
Oslo concurrency library has utilities for safely running multi-thread,
multi-process applications using locking mechanisms and for running
external processes.

%prep
%setup -q -n %{pypi_name}-%{version}
# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/lockutils-wrapper
%{python2_sitelib}/oslo_concurrency
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_concurrency/tests

%files -n python-%{pkg_name}-doc
%license LICENSE
%doc html

%files -n python-%{pkg_name}-tests
%{python2_sitelib}/oslo_concurrency/tests

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_concurrency
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_concurrency/tests
%endif

%changelog
* Wed Jun 29 2016 Alan Pevec <apevec AT redhat.com> - 2.6.1-3
- Rebuild python subpackage with python2 provides to avoid upgrade issues

* Fri Jun 24 2016 Alan Pevec <apevec AT redhat.com> - 2.6.1-2
- Rebuild python2 subpackage to avoid upgrade issues

* Thu Jun 23 2016 Haikel Guemar <hguemar@fedoraproject.org> 2.6.1-1
- Update to 2.6.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 18 2015 Alan Pevec <alan.pevec@redhat.com> 2.6.0-1
- Update to upstream 2.6.0

* Thu Sep 03 2015 Alan Pevec <alan.pevec@redhat.com> 2.5.0-1
- Update to upstream 2.5.0

* Mon Aug 17 2015 Alan Pevec <alan.pevec@redhat.com> 2.4.0-1
- Update to upstream 2.4.0

* Fri Jun 26 2015 Alan Pevec <alan.pevec@redhat.com> 2.1.0-1
- Update to upstream 2.1.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 01 2015 Alan Pevec <apevec@redhat.com> - 1.8.0-1
- update to 1.8.0

* Wed Mar 11 2015 Matthias Runge <mrunge@redhat.com> - 1.6.0-1
- upgrade to 1.6.0

* Fri Feb 20 2015 Matthias Runge <mrunge@redhat.com> - 1.4.1-2
- added openstack/common/fileutils.py
- added dependencies

* Wed Jan 28 2015 Matthias Runge <mrunge@redhat.com> - 1.4.1-1
- Initial package (rhbz#1186826)
