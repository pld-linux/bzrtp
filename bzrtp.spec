#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Open source implementation of ZRTP keys exchange protocol
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja protokołu wymiany kluczy ZRTP
Name:		bzrtp
Version:	4.4.0
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bzrtp/tags
Source0:	https://gitlab.linphone.org/BC/public/bzrtp/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	981738ec9161c2a4c5220605ed4cbb71
URL:		http://www.linphone.org/
BuildRequires:	CUnit
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	bctoolbox-devel >= 4.4.0
BuildRequires:	libtool >= 2:2
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

%build
# rebuild ac/am/lt for as-needed to work
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%if %{_ver_ge "%{cc_version}" "8.0"}
CPPFLAGS="%{rpmcppflags} -Wno-error=cast-function-type"
%endif
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbzrtp.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_libdir}/libbzrtp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbzrtp.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbzrtp.so
%{_includedir}/bzrtp
%{_pkgconfigdir}/libbzrtp.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbzrtp.a
%endif
