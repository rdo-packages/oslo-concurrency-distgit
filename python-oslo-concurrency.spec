
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
Version:        4.3.0
Release:        1%{?dist}
Summary:        OpenStack Oslo concurrency library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo concurrency library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  git
# Required for tests
BuildRequires:  python3-hacking
BuildRequires:  python3-oslotest
BuildRequires:  python3-fixtures
BuildRequires:  python3-eventlet
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-fasteners
# Required to compile translation files
BuildRequires:  python3-babel

Requires:       python3-pbr
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-fasteners

Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}

%package  -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo concurrency library
Group:      Documentation
BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinxcontrib-apidoc

%description -n python-%{pkg_name}-doc
Documentation for the Oslo concurrency library.

%endif

%package  -n python3-%{pkg_name}-tests
Summary:    Tests for the Oslo concurrency library
%{?python_provide:%python_provide python3-%{pkg_name}-tests}

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-hacking
Requires:  python3-oslotest
Requires:  python3-fixtures

%description -n python3-%{pkg_name}-tests
%{common_desc2}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo concurrency library

%description -n python-%{pkg_name}-lang
Translation files for Oslo concurrency library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
%{py3_build}

# Generate i18n files
python3 setup.py compile_catalog -d build/lib/oslo_concurrency/locale --domain oslo_concurrency

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}
ln -s ./lockutils-wrapper %{buildroot}%{_bindir}/lockutils-wrapper-3

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_concurrency/locale/*/LC_*/oslo_concurrency*po
rm -f %{buildroot}%{python3_sitelib}/oslo_concurrency/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_concurrency/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_concurrency --all-name

%check
export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0
python3 setup.py test

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/lockutils-wrapper
%{_bindir}/lockutils-wrapper-3
%{python3_sitelib}/oslo_concurrency
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_concurrency/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_concurrency/tests

%files -n python-%{pkg_name}-lang -f oslo_concurrency.lang
%license LICENSE

%changelog
* Thu Sep 17 2020 RDO <dev@lists.rdoproject.org> 4.3.0-1
- Update to 4.3.0

