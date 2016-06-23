%global pypi_name oslo.concurrency
%global pkg_name oslo-concurrency

Name:           python-oslo-concurrency
Version:        2.6.1
Release:        1%{?dist}
Summary:        OpenStack Oslo concurrency library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires:       python-babel
Requires:       python-iso8601
Requires:       python-fixtures
Requires:       python-oslo-config
Requires:       python-oslo-i18n
Requires:       python-oslo-utils
Requires:       python-retrying
Requires:       python-six
Requires:       python-fasteners

%description
Oslo concurrency library has utilities for safely running multi-thread,
multi-process applications using locking mechanisms and for running
external processes.

%package doc
Summary:    Documentation for the Oslo concurrency library
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-fixtures
BuildRequires:  python-oslo-utils
BuildRequires:  python-fasteners

%description doc
Documentation for the Oslo concurrency library.

%prep
%setup -q -n %{pypi_name}-%{version}
# Let RPM handle the dependencies
rm -f requirements.txt

%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

#delete tests
rm -fr %{buildroot}%{python2_sitelib}/%{pypi_name}/tests/

%files
%doc README.rst
%license LICENSE
%{_bindir}/lockutils-wrapper
%{python2_sitelib}/oslo_concurrency
%{python2_sitelib}/*.egg-info

%files doc
%license LICENSE
%doc html

%changelog
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
