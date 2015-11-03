%global modname neural
# https://github.com/azraq27/neural/issues/1
# Levenshtein is not available for python3
%global with_python3 0

Name:           python-%{modname}
Version:        1.1.1
Release:        1%{?dist}
Summary:        Neuroimaging analysis library

License:        GPLv2
URL:            https://github.com/azraq27/neural
Source0:        https://github.com/azraq27/neural/archive/%{version}/%{modname}-%{version}.tar.gz
# Do not check for updates every import
Patch0:         neural-disable-update-check.patch
BuildRequires:  git-core
BuildArch:      noarch

%description
This library contains helper functions for doing analyses on fMRI data in
Python.

In comparison to other Python libraries designed to interact with fMRI data
(e.g., NIPY and PyNIfTI), this library is not intended to interact directly
with the data in any way, just to provide helpful wrapper functions and
shortcut methods to make your life easier.

Since the author uses primarily AFNI, most of the functions are written that
way, but don't specifically have to be that way...

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  python-sphinx
BuildRequires:  python-fuzzywuzzy python-Levenshtein python-chardet python2-nibabel python2-pydicom
Requires:       python2-pydicom
Requires:       python-fuzzywuzzy python-Levenshtein
Requires:       python2-nibabel
Requires:       numpy
Requires:       python-chardet
Recommends:     python2-zmq

%description -n python2-%{modname}
This library contains helper functions for doing analyses on fMRI data in
Python.

In comparison to other Python libraries designed to interact with fMRI data
(e.g., NIPY and PyNIfTI), this library is not intended to interact directly
with the data in any way, just to provide helpful wrapper functions and
shortcut methods to make your life easier.

Since the author uses primarily AFNI, most of the functions are written that
way, but don't specifically have to be that way...

Python 2 version.

%if 0%{?with_python3}
%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-fuzzywuzzy python3-Levenshtein python3-chardet python3-nibabel python3-pydicom
Requires:       python3-pydicom
Requires:       python3-fuzzywuzzy python3-Levenshtein
Requires:       python3-nibabel
Requires:       python3-numpy
Requires:       python3-chardet
Recommends:     python3-zmq

%description -n python3-%{modname}
This library contains helper functions for doing analyses on fMRI data in
Python.

In comparison to other Python libraries designed to interact with fMRI data
(e.g., NIPY and PyNIfTI), this library is not intended to interact directly
with the data in any way, just to provide helpful wrapper functions and
shortcut methods to make your life easier.

Since the author uses primarily AFNI, most of the functions are written that
way, but don't specifically have to be that way...

Python 3 version.
%endif

%prep
%autosetup -n %{modname}-%{version} -S git
sed -i -e 's/import dicom as pydicom/import pydicom/' neural/dicom.py

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

pushd docs
  sed -i -e "/git/d" Makefile
  export PYTHONPATH=../
  make html SPHINXBUILD=sphinx-build BUILDDIR=_build-2
  %if 0%{?with_python3}
  make html SPHINXBUILD=sphinx-build-%{python3_version} BUILDDIR=_build-3
  %endif
  find -name '.buildinfo' -delete
popd

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%files -n python2-%{modname}
%license LICENSE.txt
%doc docs/_build-2/html
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/%{modname}_fmri*.egg-info

%if 0%{?with_python3}
%files -n python3-%{modname}
%license LICENSE.txt
%doc docs-3/_build-3/html
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}_fmri*.egg-info
%endif

%changelog
* Tue Nov 03 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.1.1-1
- Initial package
