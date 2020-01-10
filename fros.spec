Name:           fros
Version:        1.0
Release:        5%{?dist}
Summary:        Universal screencasting frontend with pluggable support for various backends

%global commit 60d9d1c5578cd32f29ce85afbe4f6c543a97b313
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/mozeq/fros
# this url is wrong, because github doesn't offer a space for downloadable archives :(
Source:         https://github.com/mozeq/fros/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0005:      0005-Ensure-that-the-right-version-of-Gtk-gets-loaded.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Obsoletes:      fros-recordmydesktop < 1.0-3

%description
Universal screencasting frontend with pluggable support for various backends.
The goal is to provide an unified access to as many screencasting backends as
possible while still keeping the same user interface so the user experience
while across various desktops and screencasting programs is seamless.

%package gnome
Summary: fros plugin for screencasting using Gnome3 integrated screencaster
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description gnome
fros plugin for screencasting using Gnome3 integrated screencaster

%prep
%setup -qn %{name}-%{commit}

%patch5 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
%{__python} setup.py test


%files
%doc README COPYING
%dir %{python_sitelib}/pyfros
%{python_sitelib}/pyfros/*.py*
%dir %{python_sitelib}/pyfros/plugins
%{python_sitelib}/pyfros/plugins/__init__.*
%{python_sitelib}/pyfros/plugins/const.*
%exclude %{python_sitelib}/pyfros/plugins/*recordmydesktop.*
# fros-1.0-py2.7.egg-info
%dir %{python_sitelib}/%{name}-%{version}-py2.7.egg-info
%{python_sitelib}/%{name}-%{version}-py2.7.egg-info/*
%{_bindir}/fros
%{_mandir}/man1/%{name}.1*

%files gnome
%{python_sitelib}/pyfros/plugins/*gnome.*

%changelog
* Tue Jan 15 2019 Ernestas Kulik <ekulik@rehdat.com> - 1.0-5
- Fix Obsoletes line

* Tue Dec 18 2018 Ernestas Kulik <ekulik@redhat.com> - 1.0-4
- Add Obsoletes line to fix installation problems when upgrading

* Mon Nov 19 2018 Ernestas Kulik <ekulik@redhat.com> - 1.0-3
- Drop recordmydesktop sub-package (rhbz#1647170)
- Load version 3.0 of Gtk namespace, silence a PyGObject warning (rhbz#1647170)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0-2
- Mass rebuild 2013-12-27

* Fri May 31 2013 Jiri Moskovcak <jmoskovc@redhat.com> 1.0-1
- initial rpm
