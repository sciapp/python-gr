%define debug_package %{nil}

# use fixedversion for builds on build.opensuse.org - needed for deb builds.
%if 0%{?mlz}
%define fixedversion %{version}
%else
%define fixedversion fixed
%define compression gz
%endif

Name:          python3-gr
Summary:       GR, a universal framework for visualization applications
Version:       1.16.1
Release:       3%{?dist}
License:       MIT
Group:         Development/Libraries
Source:        python-gr-%{fixedversion}.tar%{?compression:.%{compression}}
# for vcversioner
BuildRequires: git
BuildRequires: gr
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires:      gr
Requires:      python3
Requires:      python3-numpy

# wxWidgets BuildRequires / Requires
%if 0%{?suse_version}
BuildRequires: wxWidgets-devel
%endif

%description
GR, a universal framework for visualization applications

%prep
%setup -n python-gr-%{fixedversion}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root)
%{python3_sitelib}/gr-*.egg-info
%{python3_sitelib}/gr
%{python3_sitelib}/gr3
%{python3_sitelib}/grm
%{python3_sitelib}/qtgr
