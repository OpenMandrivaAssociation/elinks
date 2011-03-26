%define pre     %{nil}

Summary:	Lynx-like text WWW browser
Name:		elinks
Version:	0.11.7
Release:        %mkrel 2
License:	GPLv2
Group:		Networking/WWW
Epoch:		0
URL:		http://elinks.or.cz/
Source0:	http://elinks.or.cz/download/%{name}-%{version}%{pre}.tar.bz2
Patch0:		elinks-libjs_includes_fix.diff
BuildRequires:	libx11-devel
BuildRequires:	openssl-devel
BuildRequires:	bzip2-devel
BuildRequires:	idn-devel
BuildRequires:	js-devel
BuildRequires:	gpm-devel
BuildRequires:	zlib-devel
BuildRequires:	expat-devel
Provides:	webclient links
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
ELinks is an advanced and well-established feature-rich text mode web
(HTTP/FTP/..) browser. ELinks can render both frames and tables, is highly
customizable and can be extended via scripts. Its features include:

- renders tables and frames
- displays colors as specified in current HTML page
- uses drop-down menu (like in Midnight Commander)
- can download files in background
- HTTP authentification

%prep
%setup -q -n %{name}-%{version}%{pre}
%patch0 -p0

%build
autoreconf -fi
%configure2_5x \
        --enable-256-colors \
        --enable-bittorrent

%make
 
%post
update-alternatives --install %{_bindir}/links links %{_bindir}/elinks 50

%preun
if [ "$1" = "0" ]; then
  update-alternatives --remove links %{_bindir}/elinks
fi

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

rm -f $RPM_BUILD_ROOT/%{_datadir}/locale/locale.alias
rm -f doc/html/*.gz

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING ChangeLog README SITES THANKS TODO 
%doc doc/*.txt
%doc doc/html
%{_bindir}/*
%{_mandir}/man?/*
