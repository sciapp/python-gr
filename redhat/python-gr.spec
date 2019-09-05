%define debug_package %{nil}
%if 0%{?fedora_version} >= 29
%{?__python2: %global __python %{__python2}}
%else
%{!?__python: %global __python %{_bindir}/python}
%endif

%if 0%{?__jcns}
%define fixedversion %{version}
Name:          python-gr-local
%else
# use fixedversion for builds on build.opensuse.org - needed for deb builds.
%define fixedversion fixed
%define compression gz
Name:          python-gr
%endif

Summary:       GR, a universal framework for visualization applications
Version:       1.0.1
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
BuildRequires: python-devel
BuildRequires: python-setuptools
Requires:      python
Requires:      numpy
%endif

%description
GR, a universal framework for visualization applications

%prep
%setup -n python-gr-%{fixedversion}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT

%clean
%{__python} setup.py clean --all

%files
%defattr(-,root,root)
%{_prefix}
