#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Open source implementation of ZRTP keys exchange protocol
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja protokołu wymiany kluczy ZRTP
Name:		bzrtp
Version:	5.3.26
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bzrtp/tags
Source0:	https://gitlab.linphone.org/BC/public/bzrtp/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	22a3fd39362fce8ebf595a581bd633b6
Patch0:		%{name}-resetBzrtpContext.patch
URL:		http://www.linphone.org/
BuildRequires:	bctoolbox-devel >= 5.3.0
BuildRequires:	cmake >= 3.22
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.748
BuildRequires:	sqlite3-devel >= 3.6.0
Requires:	bctoolbox >= 5.3.0
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
Requires:	bctoolbox-devel >= 5.3.0

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
%if %{with static_libs}
%cmake -B builddir-static \
	-DBUILD_SHARED_LIBS=OFF

%{__make} -C builddir-static
%endif

%cmake -B builddir

%{__make} -C builddir

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

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
%dir %{_datadir}/BZRTP
%{_datadir}/BZRTP/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbzrtp.a
%endif
