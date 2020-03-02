%define debug_package %{nil}

%if 0%{?centos_version} >= 800 || 0%{?fedora_version} >= 29
%bcond_without py3
%else
%bcond_with py3
%endif

%if 0%{?centos_version} >= 800 || 0%{?fedora_version} >= 29
%define py2 python2
%else
%define py2 python
%{!?__python2: %global __python2 %{_bindir}/python}
%endif

%if 0%{?__jcns}
%define fixedversion %{version}
Name:          python-gr-local
%else
# use fixedversion for builds on build.opensuse.org - needed for deb builds.
%if 0%{?mlz}
%define fixedversion %{version}
%else
%define fixedversion fixed
%define compression gz
%endif
Name:          python-gr
%endif

Summary:       GR, a universal framework for visualization applications
Version:       1.12.1
Release:       2%{?dist}
License:       MIT
Group:         Development/Libraries
Source:        python-gr-%{fixedversion}.tar%{?compression:.%{compression}}
# for vcversioner
BuildRequires: git
BuildRequires: gr
Requires:      gr

# wxWidgets BuildRequires / Requires
%if 0%{?suse_version}
BuildRequires: libwx_baseu-2_8-0-stl
BuildRequires: libwx_gtk2u_core-2_8-0-stl
BuildRequires: libwx_baseu-2_8-0-compat-lib-stl
BuildRequires: libwx_gtk2u_core-2_8-0-compat-lib-stl
BuildRequires: wxWidgets-devel
%endif

%if 0%{?__jcns}
BuildRequires: python-local
BuildRequires: python-setuptools-local
Requires:      python-local
Requires:      numpy-local
%else
BuildRequires: %{py2}-devel
BuildRequires: %{py2}-setuptools
Requires:      python
Requires:      numpy
%endif

%if %{with py3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif

%description
GR, a universal framework for visualization applications

%prep
%setup -n python-gr-%{fixedversion}

%build
%{__python2} setup.py build
%if %{with py3}
%{__python3} setup.py build
%endif

%install
%{__python2} setup.py install --root=$RPM_BUILD_ROOT
%if %{with py3}
%{__python3} setup.py install --root=$RPM_BUILD_ROOT
%endif

%files
%defattr(-,root,root)
%{_prefix}/lib*/python2*/site-packages/gr-*.egg-info
%{_prefix}/lib*/python2*/site-packages/gr
%{_prefix}/lib*/python2*/site-packages/gr3
%{_prefix}/lib*/python2*/site-packages/qtgr


# Python 3 version:

%if %{with py3}

%package -n python3-gr
Summary:       GR, a universal framework for visualization applications (Python 3 bindings)
Requires:      python3
Requires:      python3-numpy

%description -n python3-gr
%{summary}

%files -n python3-gr
%{_prefix}/lib*/python3*/site-packages/gr-*.egg-info
%{_prefix}/lib*/python3*/site-packages/gr
%{_prefix}/lib*/python3*/site-packages/gr3
%{_prefix}/lib*/python3*/site-packages/qtgr

%endif
