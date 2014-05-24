%define pre pre6

Summary:	Lynx-like text WWW browser
Name:		elinks
Version:	0.12
Release:	0.%{pre}.2
License:	GPLv2+
Group:		Networking/WWW
Url:		http://elinks.or.cz/
Source0:	http://elinks.or.cz/download/%{name}-%{version}%{pre}.tar.bz2
Source1:	elinks.conf

# stella6.4/centos patches thx to Nux
Patch0:		elinks-0.11.0-ssl-noegd.patch
Patch1:		elinks-0.10.1-utf_8_io-default.patch
Patch2:		http://data.gpo.zugaina.org/gentoo/www-client/elinks/files/elinks-0.11.5-makefile.patch
Patch3:		elinks-0.11.0-getaddrinfo.patch
Patch4:		elinks-0.11.0-sysname.patch
Patch5:		elinks-0.10.1-xterm.patch
Patch7:		elinks-0.11.3-macropen.patch
Patch8:		elinks-scroll.patch
#Patch9:	elinks-nss.patch
#Patch10:	elinks-nss-inc.patch
Patch11:	elinks-0.12pre5-js185.patch
Patch12:	elinks-0.12pre5-ddg-search.patch
Patch13:	elinks-0.12pre6-autoconf.patch
#Patch14:	elinks-0.12pre6-ssl-hostname.patch
Patch15:	elinks-0.12pre6-list_is_singleton.patch
Patch16:	elinks-0.12pre6-lua51.patch

BuildRequires:	bzip2-devel
BuildRequires:	gpm-devel
BuildRequires:	krb5-devel
BuildRequires:	lua-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libidn)
BuildRequires:	pkgconfig(mozjs185)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
Provides:	webclient
Provides:	links

%description
ELinks is an advanced and well-established feature-rich text mode web
(HTTP/FTP/..) browser. ELinks can render both frames and tables, is highly
customizable and can be extended via scripts. Its features include:

- renders tables and frames
- displays colors as specified in current HTML page
- uses drop-down menu (like in Midnight Commander)
- can download files in background
- HTTP authentication

%files -f elinks.lang
%{_bindir}/elinks
%doc README SITES TODO COPYING
%ghost %verify(not md5 size mtime) %{_bindir}/links
%ghost %verify(not md5 size mtime) %{_mandir}/man1/links*
%config(noreplace) %{_sysconfdir}/elinks.conf
%{_mandir}/man1/elinks.1*
%{_mandir}/man5/*

%postun
if [ "$1" -ge "1" ]; then
	links=`readlink %{_sysconfdir}/alternatives/links`
	if [ "$links" == "%{_bindir}/elinks" ]; then
		%{_sbindir}/alternatives --set links %{_bindir}/elinks
	fi
fi
exit 0

%post
#Set up alternatives files for links
%{_sbindir}/alternatives --install %{_bindir}/links links %{_bindir}/elinks 90 \
  --slave %{_mandir}/man1/links.1.gz links-man %{_mandir}/man1/elinks.1.gz
links=`readlink %{_sysconfdir}/alternatives/links`
if [ "$links" == "%{_bindir}/elinks" ]; then
	%{_sbindir}/alternatives --set links %{_bindir}/elinks
fi

%preun
if [ $1 = 0 ]; then
	%{_sbindir}/alternatives --remove links %{_bindir}/elinks
fi
exit 0

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}%{pre}
%apply_patches

find . -name "Makefile*" -o -name "*.m4" |xargs sed -i -e 's,configure.in,configure.ac,g'
sed -i 's/^# *serial [AM0-9]*$//' acinclude.m4 config/m4/*.m4
aclocal -I config/m4
autoreconf

%build
export CFLAGS="%{optflags} $(getconf LFS_CFLAGS) -D_GNU_SOURCE"
%configure2_5x \
	%{?rescue:--without-gpm} \
	--without-x \
	--with-gssapi \
	--enable-bittorrent \
	--without-nss_compat_ossl \
	--enable-256-colors \
	--with-openssl \
	--without-gnutls \
	--with-lua

MOPTS="V=1"
if tty >/dev/null 2>&1; then
    # turn on fancy colorized output only when we have a TTY device
    MOPTS=
fi
%make $MOPTS

%install
%makeinstall_std
rm -f %{buildroot}%{_datadir}/locale/locale.alias
mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/elinks.conf
touch %{buildroot}%{_bindir}/links
true | gzip -c > %{buildroot}%{_mandir}/man1/links.1.gz

%find_lang elinks

