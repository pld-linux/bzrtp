#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Open source implementation of ZRTP keys exchange protocol
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja protokołu wymiany kluczy ZRTP
Name:		bzrtp
Version:	4.5.20
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bzrtp/tags
Source0:	https://gitlab.linphone.org/BC/public/bzrtp/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	a702edc1182579acb82d9456f6e35e88
Patch0:		%{name}-static.patch
URL:		http://www.linphone.org/
BuildRequires:	CUnit
BuildRequires:	bctoolbox-devel >= 4.4.0
BuildRequires:	cmake >= 3.1
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.748
BuildRequires:	sqlite3-devel >= 3.6.0
Requires:	bctoolbox >= 4.4.0
Requires:	sqlite3 >= 3.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bzrtp is an opensource implementation of ZRTP keys exchange protocol. 
The library written in C 89 is fully portable and can be executed on
many platforms including both ARM processor and x86. 

%description -l pl.UTF-8
bzrtp to mająca otwarte źródła implementacja protokołu wymiany kluczy
ZRTP. Napisana w C 89 biblioteka jest w pełni przenośna i może być
wykonywana na wielu platformach, w tym ARM oraz x86.

%package devel
Summary:	Header file for bzrtp library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki bzrtp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for bzrtp library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki bzrtp.

%package static
Summary:	Static bzrtp library
Summary(pl.UTF-8):	Statyczna biblioteka bzrtp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static bzrtp library.

%description static -l pl.UTF-8
Statyczna biblioteka bzrtp.

%prep
%setup -q
%patch0 -p1

%build
install -d builddir
cd builddir
%cmake .. \
	%{!?with_static_libs:-DENABLE_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_datadir}/bzrtp/cmake/bzrtpTargets.cmake

# missing from cmake
test ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/libbzrtp.pc
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__sed} -e 's,@prefix@,%{_prefix},' \
	-e 's,@exec_prefix@,%{_exec_prefix},' \
	-e 's,@includedir@,%{_includedir},' \
	-e 's,@PACKAGE_VERSION@,%{version},' \
	-e 's,@libdir@,%{_libdir},' libbzrtp.pc.in >$RPM_BUILD_ROOT%{_pkgconfigdir}/libbzrtp.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_libdir}/libbzrtp.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbzrtp.so
%{_includedir}/bzrtp
%{_pkgconfigdir}/libbzrtp.pc
%dir %{_datadir}/bzrtp
%{_datadir}/bzrtp/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbzrtp.a
%endif
