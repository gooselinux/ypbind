Summary: The NIS daemon which binds NIS clients to an NIS domain
Name: ypbind
Version: 1.20.4
Release: 29%{?dist}
License: GPLv2
Group: System Environment/Daemons
Source0: ftp://ftp.us.kernel.org/pub/linux/utils/net/NIS/ypbind-mt-%{version}.tar.bz2
Url: http://www.linux-nis.org/nis/ypbind-mt/index.html
Source1: ypbind.init
Source2: nis.sh
Patch1: ypbind-1.11-broadcast.patch
Patch2: ypbind-1.11-gettextdomain.patch
Patch3: ypbind-mt-1.19-port-leak.patch
Patch4: ypbind-mt-1.20.4-log-binds.patch
Patch5: ypbind-mt-1.20.4-smartwrite.patch
Patch6: ypbind-mt-1.20.4-man-port.patch
Patch7: ypbind-mt-1.20.4-nm.patch
Patch8: ypbind-mt-1.20.4-network.patch
# Response from upstream: the patch will be a part of next release.
# Fixes bug #537064.
Patch9: ypbind-mt-1.20.4-signalstate.patch
# Backported from newer ypbind release.
# serv_list.c:912: warning: dereferencing type-punned
# pointer will break strict-aliasing rules
Patch10: ypbind-mt-1.20.4-strict-aliasing.patch
# Backported from newer ypbind release.
Patch11: ypbind-mt-1.20.4-add-server.patch
# Sent to upstream.
Patch12: ypbind-mt-1.20.4-matches.patch

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
Requires: rpcbind, yp-tools
Epoch: 3
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: dbus-glib-devel, docbook-style-xsl

%description
The Network Information Service (NIS) is a system that provides
network information (login names, passwords, home directories, group
information) to all of the machines on a network. NIS can allow users
to log in on any machine on the network, as long as the machine has
the NIS client programs running and the user's password is recorded in
the NIS passwd database. NIS was formerly known as Sun Yellow Pages
(YP).

This package provides the ypbind daemon. The ypbind daemon binds NIS
clients to an NIS domain. Ypbind must be running on any machines
running NIS client programs.

Install the ypbind package on any machines running NIS client programs
(included in the yp-tools package). If you need an NIS server, you
also need to install the ypserv package to a machine on your network.

%prep
%setup -q -n ypbind-mt-%{version}
%patch1 -p1 -b .broadcast
%patch2 -p1 -b .gettextdomain
%patch3 -p1 -b .port-leak
%patch4 -p1 -b .log-binds
%patch5 -p1 -b .smartwrite
%patch6 -p1 -b .man-port
%patch7 -p1 -b .nm
%patch8 -p1 -b .network
%patch9 -p1 -b .signalstate
%patch10 -p1 -b .strict-aliasing
%patch11 -p1 -b .add-server
%patch12 -p1 -b .matches

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_initrddir} $RPM_BUILD_ROOT/var/yp/binding $RPM_BUILD_ROOT/etc/dhcp/dhclient.d/
install -m 644 etc/yp.conf $RPM_BUILD_ROOT/etc/yp.conf
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/ypbind
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/etc/dhcp/dhclient.d/nis.sh

%{find_lang} %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ypbind

%preun
if [ $1 = 0 ] ; then
    /sbin/service ypbind stop >/dev/null 2>&1
    /sbin/chkconfig --del ypbind
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service ypbind condrestart >/dev/null 2>&1 || :
fi

%files -f %{name}.lang
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/*/*
%{_initrddir}/*
/etc/dhcp/dhclient.d/*
%config(noreplace) /etc/yp.conf
%dir /var/yp/binding
%doc README NEWS COPYING

%changelog
* Tue Jun 22 2010 Karel Klic <kklic@redhat.com> - 3:1.20.4-29
- Remove matches when dereferencing DBus connection.
  Resolves: #597407

* Wed Jun  9 2010 Karel Klic <kklic@redhat.com> - 3:1.20.4-28
- ypbind.init: take the first domainname in yp.conf and use
  only that
  Resolves: #601615

* Fri Jun  4 2010 Karel Klic <kklic@redhat.com> - 3:1.20.4-27
- Fix "serv_list.c:487: array subscript above array bounds"
  Resolves: #598552

* Thu Jun  3 2010 Karel Klic <kklic@redhat.com> - 3:1.20.4-26
- Fix "dereferencing type-punned pointer will break strict-aliasing rules"
  GCC warning
  Resolves #596221

* Fri May 28 2010 Karel Klic <kklic@redhat.com> - 3:1.20.4-25
- Moved /sbin/ypbind to /usr/sbin/ypbind, as the package
  depends on several utilities from /usr (selinuxenabled,
  rpcinfo, ypwhich), and /usr/lib/libdbus-glib-1.so
  Resolves: #593271
- Fixed previous ChangeLog entry header

* Fri May 28 2010  Karel Klic <kklic@redhat.com> - 3:1.20.4-24
- Removed ping interval change from ypbind-mt-1.20.4-log-binds.patch
  Resolves #594693

* Wed Feb 24 2010 Karel Klic <kklic@redhat.com> - 3:1.20.4-23
- Added COPYING file to the package

* Thu Jan 21 2010 Karel Klic <kklic@redhat.com> - 3:1.20.4-22
- Rewrote initscript to become closer to Packaging:SysVInitScript
  Fedora guildeline. The change also fixes bug 523913

* Fri Nov 13 2009 Karel Klic <kklic@redhat.com> - 3:1.20.4-21
- Added signalstate patch, which fixes compilation with
  NetworkManaged-devel headers installed. Resolves 537064.
  Related: rhbz#543948

* Thu Oct 29 2009 Karel Klic <kklic@redhat.com> - 3:1.20.4-20
- Bind to domain even if not using NetworkManager
  The fix uses  only the code from upstream ypbind-mt-1.29.91
  Resolves: #531398

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.20.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr  8 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-18
- Remove LSB Header from init script
  Resolves: #494827

* Wed Mar 18 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-17
- Fix nis.sh SELinux issue
  Resolves: #488865

* Thu Feb 26 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-16
- Fix ypbind script in dos format - bash syntax errors
  Resolves: #486722

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.20.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-14
- Update helper script for dhclient

* Mon Jan 26 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-13
- Fix ypbind can fail to bind if started soon after NetworkManager
  Resolves: #480096

* Mon Jan  5 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-12
- Ship helper script for dhclient

* Wed Dec  3 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-11
- Fix verbose option man page entry
- Add description of port option to man page
  Resolves: #474184

* Mon Nov 24 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-10
- Last few Merge Review related changes
- Fix init script arguments and return values
  Resolves: #247104, #467861

* Tue Oct 21 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-9
- Merge Review - remove dot from end of the summary, convert all tags
  in %%changelog to utf-8, escape %% character in changelog, fix
  requires and scriptlets, remove %%makeinstall, do not mark init
  script file as config, remove unused patches
  Resolves: #226663

* Tue Oct 21 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-8
- Rewrite binding files only when they are changed
  Resolves: #454581

* Mon Aug 11 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 3:1.20.4-7
- Fix license tag.

* Tue Jun 10 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-6
- Don't disable allow_ypbind SELinux boolean on service shutdown
  Resolves: #448240

* Wed May 21 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-5
- Fix init script timing again

* Tue Feb 12 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-4
- Fix Buildroot

* Fri Jan 11 2008 Steve Dickson <steved@redhat.com> - 3:1.20.4-3
- Fixed init script to wait for ypbind to come up. (bz 322101)

* Mon Sep 17 2007 Steve Dickson <steved@redhat.com> - 3:1.20.4-2
- Fixed a couple of typos in initscript (bz 281951)

* Wed May  3 2007 Steve Dickson <steved@redhat.com> - 3:1.20.4-1
- updated to latest upstream version ypbind-mt-1.20.4

* Tue Apr 17 2007 Steve Dickson <steved@redhat.com> - 3:1.19-9
- Fixed typo in init script (bz 233459)
- Changed init script to look in /etc/yp.conf for the
  domain name when not already set. (bz 113386)
- Reworked init script to eliminate unreasonable
  hangs when ypbind cannot bind to nis server. (bz 112770)

* Tue Apr  3 2007 Steve Dickson <steved@redhat.com> - 3:1.19-8
- Replace portmap dependency with an rpcbind dependency (bz 228894)

* Fri Dec  1 2006 Steve Dickson <steved@redhat.com> - 3:1.19-7
- Fixed leaking ports (bz 217874)
- Log all server bindings (bz 217782)
- Added better quoting to init script (bz 216739)

* Mon Nov 27 2006 Dan Walsh <dwalsh@redhat.com> - 3:1.19-6
- Correct ordering of turning off SELinux boolean

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 3:1.19-5
- Change init script to automatically turn on/off allow_ypbind boolean

* Wed Aug 23 2006 Steve Dickson <steved@redhat.com> - 3:1.19-4
- Remove the -s from install process making the -debuginfo
  package useful (bz 203851)
- Added the sourcing of /etc/sysconfig/ypbind (bz 199448)

* Fri Aug 11 2006 Steve Dickson <steved@redhat.com> - 3:1.19-2
- rebuild

* Tue Jul 25 2006 Steve Dickson <steved@redhat.com> - 3:1.19-0.3
- rebuild

* Tue Jul 18 2006 Steve Dickson <steved@redhat.com> - 3:1.19-0.2
- Added NISTIMEOUT variable to init scrip (bz 196078)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3:1.19-0.1
- rebuild

* Mon Feb 13 2006 Chris Feist <cfeist@redhat.com> - 3:1.19
- Build for latest version of ypbind-mt

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3:1.17.2-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3:1.17.2-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Jan 24 2005 Steve Dickson <SteveD@RedHat.com> 1.17.2-4
- Changed the initscript to use the logger command instead
  of initlog script, since the initlog script has gone away.

* Fri Oct 15 2004 Steve Dickson <SteveD@RedHat.com> 1.17.2-3
- Sped up the ypbind initscript by using fgrep
  instead of grep (bz# 81247)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Phil Knirsch <pknirsch@redhat.com> 1.17.2-1
- Another updated to latest upstream version.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 19 2004 Phil Knirsch <pknirsch@redhat.com> 1.16-1
- Updated to latest upstream version.

* Thu Nov 20 2003 Steve Dickson <SteveD@RedHat.com>
- Added a NULL check to test_bindings() to make sure
  clnt_call() is not called with a NULL pointer.

* Sat Oct  4 2003 Steve Dickson <SteveD@RedHat.com>
- Updated Release number for RHEL3 QU1

* Tue Sep  9 2003 Steve Dickson <SteveD@RedHat.com>
- Fixed a binding race where the wrong results were being returned.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Bill Nottingham <notting@redhat.com> 1.12-1.10
- make yp.conf %%config(noreplace)

* Thu Apr 24 2003 Steve Dickson <SteveD@RedHat.com>
- Updated to 1.12 from upstream.
- Removed ypbind-1.8-dos.patch since it
  was already commented out
- Updated broadcast patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- build on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 11 2002 Alex Larsson <alexl@redhat.com> 1.11-1
- Updated to 1.11 from upstream.
- Removed patche that went in upstream.
- Updated broadcast patch

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar 25 2002 Alex Larsson <alexl@redhat.com> 1.10-7
- Get failure message right in init script (#37463 again)

* Mon Mar 25 2002 Alex Larsson <alexl@redhat.com> 1.10-6
- Fix bugs in initscript. Should fix #37463 and #61857

* Mon Mar 25 2002 Alex Larsson <alexl@redhat.com> 1.10-5
- New config patch that handles failing gethostbynames even better

* Thu Mar 21 2002 Alex Larsson <alexl@redhat.com> 1.10-4
- Added patch to avoid hanging if gethostbyname fails. (#56322)

* Sun Mar 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fixed #57393

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Nov 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to version 1.10

* Mon Aug 13 2001 Preston Brown <pbrown@redhat.com>
- eliminate potential DOS attack via ypwhich (#38637)
- install PO files

* Tue Jul 17 2001 Karsten Hopp <karsten@redhat.de>
- own /var/yp

* Fri Jun 29 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Jun  4 2001 Preston Brown <pbrown@redhat.com>
- small fixes for initscript. Sometimes had trouble on slower systems (#37463)

* Sat Mar  3 2001 Preston Brown <pbrown@redhat.com>
- much more sane ypbind init script for when networking is down.

* Wed Feb  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- fix "usage" string (use $0)

* Wed Jan 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- prepare for initscript translation
- do not prereq /etc/init.d

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Start after netfs (#23526)

* Wed Nov 29 2000 Bill Nottingham <notting@redhat.com>
- set NIS domain name if it's not already set

* Mon Oct 02 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.7

* Thu Aug 31 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add again automatic fallback to broadcast

* Sun Aug 20 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- fix condrestart #16615
- security fix for syslog() call

* Sun Aug  6 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- do not include broadcast fallback until it is more tested

* Sun Aug  6 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add automatic fallback to broadcast
- add "exit 0" to the scripts

* Wed Aug  2 2000 Bill Nottingham <notting@redhat.com>
- turn off broadcast; authconfig will enable this...
- put the pid that's actually listening to signals in the pidfile

* Thu Jul 20 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- prereq init.d

* Wed Jul  5 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- re-enable broadcasts

* Tue Jul  4 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix scripts

* Mon Jul  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- bump epoch

* Mon Jul  3 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- switch from ypbind to ypbind-mt
