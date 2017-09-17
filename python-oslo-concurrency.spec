%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global pypi_name oslo.concurrency
%global pkg_name oslo-concurrency

%global common_desc \
Oslo concurrency library has utilities for safely running multi-thread, \
multi-process applications using locking mechanisms and for running \
external processes.

%global common_desc2 \
Tests for the Oslo concurrency library.

Name:           python-oslo-concurrency
Version:        XXX
Release:        XXX
Summary:        OpenStack Oslo concurrency library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n python2-%{pkg_name}
Summary:        OpenStack Oslo concurrency library
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  git
# Required for tests
BuildRequires:  python-hacking
BuildRequires:  python-oslotest
BuildRequires:  python-futures
BuildRequires:  python-fixtures
BuildRequires:  python-enum34
BuildRequires:  python-eventlet
# Required to compile translation files
BuildRequires:  python-babel

Requires:       python-fixtures
Requires:       python-oslo-config >= 2:4.0.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-six
Requires:       python-fasteners
Requires:       python-enum34
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}

%package  -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo concurrency library
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-fixtures
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-utils
BuildRequires:  python-fasteners
BuildRequires:  openstack-macros

%description -n python-%{pkg_name}-doc
Documentation for the Oslo concurrency library.

%endif

%package  -n python2-%{pkg_name}-tests
Summary:    Tests for the Oslo concurrency library
%{?python_provide:%python_provide python2-%{pkg_name}-tests}

Requires:  python2-%{pkg_name} = %{version}-%{release}
Requires:  python-hacking
Requires:  python-oslotest
Requires:  python-futures
Requires:  python-fixtures


%description -n python2-%{pkg_name}-tests
%{common_desc2}

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo concurrency library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# Required for tests
BuildRequires:  python3-hacking
BuildRequires:  python3-oslotest
BuildRequires:  python3-fixtures
BuildRequires:  python3-eventlet

Requires:       python3-fixtures
Requires:       python3-oslo-config >= 2:4.0.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-utils >= 3.20.0
Requires:       python3-six
Requires:       python3-fasteners
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%package  -n python3-%{pkg_name}-tests
Summary:    Tests for the Oslo concurrency library
%{?python_provide:%python_provide python3-%{pkg_name}-tests}

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-hacking
Requires:  python3-oslotest
Requires:  python3-fixtures

%description -n python3-%{pkg_name}-tests
%{common_desc2}
%endif

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo concurrency library

%description -n python-%{pkg_name}-lang
Translation files for Oslo concurrency library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_concurrency/locale

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/lockutils-wrapper %{buildroot}%{_bindir}/lockutils-wrapper-%{python3_version}
ln -s ./lockutils-wrapper-%{python3_version} %{buildroot}%{_bindir}/lockutils-wrapper-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/lockutils-wrapper %{buildroot}%{_bindir}/lockutils-wrapper-%{python2_version}
ln -s ./lockutils-wrapper-%{python2_version} %{buildroot}%{_bindir}/lockutils-wrapper-2

ln -s ./lockutils-wrapper-%{python2_version} %{buildroot}%{_bindir}/lockutils-wrapper

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_concurrency/locale/*/LC_*/oslo_concurrency*po
rm -f %{buildroot}%{python2_sitelib}/oslo_concurrency/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_concurrency/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_concurrency/locale
%endif

# Find language files
%find_lang oslo_concurrency --all-name

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/lockutils-wrapper
%{_bindir}/lockutils-wrapper-2
%{_bindir}/lockutils-wrapper-%{python2_version}
%{python2_sitelib}/oslo_concurrency
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_concurrency/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_concurrency/tests

%files -n python-%{pkg_name}-lang -f oslo_concurrency.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/lockutils-wrapper-3
%{_bindir}/lockutils-wrapper-%{python3_version}
%{python3_sitelib}/oslo_concurrency
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_concurrency/tests

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_concurrency/tests
%endif


%changelog
