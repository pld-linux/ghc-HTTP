#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	HTTP
Summary:	A library for client-side HTTP
Summary(pl.UTF-8):	Biblioteka kliencka HTTP
Name:		ghc-%{pkgname}
Version:	4000.3.14
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/HTTP
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	a2e340760c318658313f1548c91e2692
Patch0:		ghc-8.10.patch
URL:		http://hackage.haskell.org/package/HTTP
BuildRequires:	ghc >= 7.0.1
BuildRequires:	ghc-array >= 0.3.0.2
BuildRequires:	ghc-array < 0.6
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-bytestring >= 0.9.1.5
BuildRequires:	ghc-bytestring < 0.11
BuildRequires:	ghc-mtl >= 2.0
BuildRequires:	ghc-mtl < 2.3
BuildRequires:	ghc-network >= 2.6
BuildRequires:	ghc-network < 3.2
BuildRequires:	ghc-network-uri >= 2.6
BuildRequires:	ghc-network-uri < 2.7
BuildRequires:	ghc-parsec >= 2.0
BuildRequires:	ghc-parsec < 3.2
BuildRequires:	ghc-time >= 1.1.2.3
BuildRequires:	ghc-time < 1.10
%if %{with prof}
BuildRequires:	ghc-prof >= 7.0.1
BuildRequires:	ghc-array-prof >= 0.3.0.2
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-bytestring-prof >= 0.9.1.5
BuildRequires:	ghc-mtl-prof >= 2.0
BuildRequires:	ghc-network-prof
BuildRequires:	ghc-network-uri-prof
BuildRequires:	ghc-parsec-prof >= 2.0
BuildRequires:	ghc-time-prof >= 1.1.2.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-array >= 0.3.0.2
Requires:	ghc-base >= 4.3
Requires:	ghc-bytestring >= 0.9.1.5
Requires:	ghc-mtl >= 2.0
Requires:	ghc-network >= 2.6
Requires:	ghc-network-uri >= 2.6
Requires:	ghc-parsec >= 2.0
Requires:	ghc-time >= 1.1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The HTTP package supports client-side web programming in Haskell. It
lets you set up HTTP connections, transmitting requests and processing
the responses coming back, all from within the comforts of Haskell.
It's dependent on the network package to operate, but other than that,
the implementation is all written in Haskell.

%description -l pl.UTF-8
Pakiet HTTP wspiera programowanie strony klienckiej WWW w Haskellu.
Pozwala na ustanawianie połączeń HTTP, transmisję żądań i
przetwarzanie nadchodzących odpowiedzi - wszystko z poziomu komfortu
Haskella. Do operacji sieciowych używa pakietu network, ale cała
reszta jest zaimplementowana w Haskellu.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof >= 0.3.0.2
Requires:	ghc-base-prof >= 4.3
Requires:	ghc-bytestring-prof >= 0.9.1.5
Requires:	ghc-mtl-prof >= 2.0
Requires:	ghc-network-prof >= 2.6
Requires:	ghc-network-uri-prof >= 2.6
Requires:	ghc-parsec-prof >= 2.0
Requires:	ghc-time-prof >= 1.1.2.3

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch -P0 -p1

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSHTTP-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSHTTP-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSHTTP-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/HTTP
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/HTTP/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/HTTP/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSHTTP-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/HTTP/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
