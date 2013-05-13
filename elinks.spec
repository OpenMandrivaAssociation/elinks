%define pre     %{nil}

Summary:	Lynx-like text WWW browser
Name:		elinks
Version:	0.11.7
Release:        6
License:	GPLv2
Group:		Networking/WWW
Epoch:		0
URL:		http://elinks.or.cz/
Source0:	http://elinks.or.cz/download/%{name}-%{version}%{pre}.tar.bz2
Patch0:		elinks-libjs_includes_fix.diff
BuildRequires:	pkgconfig(x11)
BuildRequires:	openssl-devel
BuildRequires:	bzip2-devel
BuildRequires:	idn-devel
BuildRequires:	js-devel
BuildRequires:	gpm-devel
BuildRequires:	expat-devel
Provides:	webclient links

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
        --enable-bittorrent \
        --without-zlib
# as for 0.11.7, zlib encoding support is broken, seems related to 
# http://bugzilla.elinks.cz/show_bug.cgi?id=1034 but the patch doesn't
# apply anymore

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


%changelog
* Wed May 04 2011 Bogdano Arendartchuk <bogdano@mandriva.com> 0:0.11.7-5
+ Revision: 666834
- disabled zlib encoding support, as it results in an empty page, upstream
  issue #1034 does not seem to provide a valid fix for current version

  + Sandro Cazzaniga <kharec@mandriva.org>
    - clean specfile

* Wed Feb 02 2011 Funda Wang <fwang@mandriva.org> 0:0.11.7-4
+ Revision: 635335
- simplify BR

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.11.7-3mdv2011.0
+ Revision: 610352
- rebuild

* Thu Apr 08 2010 Rémy Clouard <shikamaru@mandriva.org> 0:0.11.7-2mdv2010.1
+ Revision: 533230
- Rebuild for new openssl

* Tue Sep 15 2009 Frederik Himpe <fhimpe@mandriva.org> 0:0.11.7-1mdv2010.0
+ Revision: 443218
- update to new version 0.11.7

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0:0.11.5-2mdv2010.0
+ Revision: 437411
- rebuild

* Sat Oct 11 2008 Frederik Himpe <fhimpe@mandriva.org> 0:0.11.5-1mdv2009.1
+ Revision: 291683
- update to new version 0.11.5

* Tue Jun 24 2008 Oden Eriksson <oeriksson@mandriva.com> 0:0.11.4-2mdv2009.0
+ Revision: 228612
- fix libjs stuff

  + Frederik Himpe <fhimpe@mandriva.org>
    - New version 0.11.4
    - New license policy

* Tue Feb 05 2008 Frederik Himpe <fhimpe@mandriva.org> 0:0.11.4-1mdv2008.1
+ Revision: 162812
- New stable version 0.11.4rc0 (fixes security problem CVE-2007-2027)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Jul 09 2007 Funda Wang <fwang@mandriva.org> 0:0.11.3-1mdv2008.0
+ Revision: 50444
- New version


* Mon Nov 20 2006 Lenny Cartier <lenny@mandriva.com> 0.11.2-1mdv2007.0
+ Revision: 85504
- Update to 0.11.2
- Import elinks

* Mon Jun 12 2006 Charles A Edwards <eslrahc@mandriva.org> 0.11.1-1mdv2007.1
- 0.11.1
- mkrel
- enable bittorrent support
- update doc listing

* Mon May 08 2006 Jerome Soyer <saispo@mandriva.org> 0.10.6-1mdk
- New release 0.10.6

* Fri Mar 24 2006 Pixel <pixel@mandriva.com> 0.10.5-3mdk
- add BuildRequires X11-devel
- rebuild (for crypto deps)

* Tue Aug 09 2005 Abel Cheung <deaddog@mandriva.org> 0:0.10.5-2mdk
- Rebuild, to get back rpms

* Tue Aug 09 2005 Abel Cheung <deaddog@mandriva.org> 0:0.10.5-1mdk
- 0.10.5
- Remove menu again
- Elinks only reads per-user config, attempt to place global config
  randomly is useless
- Take description from elinks itself
- Remove message during install, which was related to around 0.4 days
- Fix scriptlets
- Tune up alt priority, because if people pick up this non-default
  links, that means people really want to try it

* Sat Apr 09 2005 Charles A Edwards <eslrahc@mandrake.org> 0:0.10.4-1mdk
- 0.10.4

* Tue Mar 01 2005 Lenny Cartier <lenny@mandrakesoft.com> 0:0.10.3-1mdk
- 0.10.3

* Thu Feb 03 2005 Charles A Edwards <eslrahc@mandrake.org> 0:0.10.2-1mdk
- 0.10.2

* Wed Jan 05 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.10.1-1mdk
- 0.10.1

* Mon Dec 27 2004 Charles A Edwards <eslrahc@mandrake.org> 0.10.0-1mdk
- 0.10.0
- put back menu entry

* Wed Aug 04 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.9.2-0.rc4.1mdk
- 0.9.2rc4

* Fri Jul 23 2004 Charles A Edwards <eslrahc@mandrake.org> 0.9.2-0.rc3.1mdk
- 0.9.2rc3

* Wed Jun 30 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.9.2-0.rc2.1mdk
* Tue Jun 23 2004 Charles A Edwards <eslrahc@mandrake.org> 0.9.2-0.rc1.1mdk
- 0.9.2rc1

* Mon Feb 09 2004 Abel Cheung <deaddog@deaddog.org> 0.9.1-2mdk
- Remove files provided by glibc
- BuildRequires smbclient (for smb:// support)
- Remove menu entry (people won't expect text mode browsers appear in menu)

