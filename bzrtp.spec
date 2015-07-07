#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Open source implementation of ZRTP keys exchange protocol
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja protokołu wymiany kluczy ZRTP
Name:		bzrtp
Version:	1.0.2
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://linphone.org/releases/sources/bzrtp/%{name}-%{version}.tar.gz
# Source0-md5:	b52fa670fb319022166cb10d641da4e6
URL:		http://www.linphone.org/
BuildRequires:	CUnit
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	polarssl-devel
BuildRequires:	pkgconfig
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
%doc AUTHORS NEWS README
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
