%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
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
Version:        5.3.0
Release:        1%{?dist}
Summary:        OpenStack Oslo concurrency library

License:        Apache-2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo concurrency library

BuildRequires:  python3-devel
BuildRequires:  git-core
BuildRequires:  pyproject-rpm-macros
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}

%package  -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo concurrency library
Group:      Documentation
%description -n python-%{pkg_name}-doc
Documentation for the Oslo concurrency library.

%endif

%package  -n python3-%{pkg_name}-tests
Summary:    Tests for the Oslo concurrency library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-hacking
Requires:  python3-oslotest
Requires:  python3-fixtures
Requires:  python3-stestr

%description -n python3-%{pkg_name}-tests
%{common_desc2}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo concurrency library

%description -n python-%{pkg_name}-lang
Translation files for Oslo concurrency library

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel


%install
%pyproject_install

# Generate i18n files
python3 setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/oslo_concurrency/locale --domain oslo_concurrency

%if 0%{?with_doc}
# generate html docs
PYTHONPATH="%{buildroot}/%{python3_sitelib}"
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

ln -s ./lockutils-wrapper %{buildroot}%{_bindir}/lockutils-wrapper-3

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_concurrency/locale/*/LC_*/oslo_concurrency*po
rm -f %{buildroot}%{python3_sitelib}/oslo_concurrency/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_concurrency/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_concurrency --all-name

%check
%tox -e %{default_toxenv}

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/lockutils-wrapper
%{_bindir}/lockutils-wrapper-3
%{python3_sitelib}/oslo_concurrency
%{python3_sitelib}/*.dist-info
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
* Thu Mar 14 2024 RDO <dev@lists.rdoproject.org> 5.3.0-1
- Update to 5.3.0

