Summary:	Lynx-like text WWW browser
Name:		elinks
Version:	0.20.0
Release:	1
License:	GPLv2+
Group:		Networking/WWW
Url:		https://github.com/rkd77/elinks
Source0:	https://github.com/rkd77/elinks/releases/download/v%{version}/elinks-%{version}.tar.xz
Source1:	elinks.conf

# dropped (no longer applies): Patch1:		elinks-0.10.1-utf_8_io-default.patch
# dropped (no longer applies): Patch2:		http://data.gpo.zugaina.org/gentoo/www-client/elinks/files/elinks-0.11.5-makefile.patch
Patch3:		elinks-0.11.0-getaddrinfo.patch
Patch5:		elinks-0.10.1-xterm.patch
Patch15:	elinks-0.12pre6-list_is_singleton.patch

BuildRequires:	meson
BuildSystem:	meson
BuildOption:	-D256-colors=true
BuildOption:	-D88-colors=true
BuildOption:	-Dtrue-color=true
BuildOption:	-Dbrotli=true
BuildOption:	-Dbzlib=true
BuildOption:	-Dcgi=true
BuildOption:	-Ddocdir=%{_docdir}/%{name}
BuildOption:	-Dgssapi=true
BuildOption:	-Dlibavif=false
BuildOption:	-Dlzma=true
BuildOption:	-Dzstd=true
BuildOption:	-Dlibcss=false
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libbrotlidec)
BuildRequires:	pkgconfig(tre)
BuildRequires:	gpm-devel
BuildRequires:	krb5-devel
BuildRequires:	lua-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libzstd)
Provides:	webclient
Provides:	links
Requires(post,preun,postun):	rpm-helper

%description
ELinks is an advanced and well-established feature-rich text mode web
(HTTP/FTP/..) browser. ELinks can render both frames and tables, is highly
customizable and can be extended via scripts. Its features include:

- renders tables and frames
- displays colors as specified in current HTML page
- uses drop-down menu (like in Midnight Commander)
- can download files in background
- HTTP authentication

%files -f %{name}.lang
%{_bindir}/elinks
%doc %{_docdir}/%{name}
%config(noreplace) %{_sysconfdir}/elinks.conf
%{_mandir}/man1/elinks.1*
%{_mandir}/man5/*

%install -a
mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/elinks.conf

%find_lang %{name} --all-name --with-man
