Summary: smeserver specific mysql55 configuration and templates.
%define name smeserver-mysql55
Name: %{name}
%define version 1.0.0
%define release 4
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
BuildArchitectures: noarch
Requires: mysql55-mysql-server
Requires: mysql55-mysql
Requires: mysql55-runtime
Requires: mysql55-mysql-libs
Requires: mysql55
Requires: e-smith-base
Requires: e-smith-lib >= 1.15.1-19
BuildRequires: e-smith-devtools >= 1.13.1-03
AutoReqProv: no

%changelog
* Mon May  19 2014 JP Pialasse <tests@pialasse.com> 1.0.0-4.sme
- initial release from e-smith-mysql 2.0.0-4

%description
This package adds necessary startup and configuration items for
mysql55.

%prep
%setup

%build
mkdir -p root/etc/e-smith/sql/init55
perl createlinks

# add this for mysql.com rpm compatibility 
#mkdir -p root/var/run/mysql55-mysqld
# we hould we rather link to the actual dir in opt , done in createlinks

mkdir -p root/etc/rc.d/init.d/supervise
ln -s ../daemontools root/etc/rc.d/init.d/supervise/mysql55-mysqld

mkdir -p root/etc/rc.d/rc7.d
ln -s /etc/rc.d/init.d/e-smith-service root/etc/rc.d/rc7.d/S50mysql55-mysqld
ln -s /etc/rc.d/init.d/e-smith-service root/etc/rc.d/rc7.d/S99mysql55-mysql.init

mkdir -p root/service
ln -s /var/service/mysql55-mysqld root/service
touch root/var/service/mysql55-mysqld/down

mkdir -p root/var/log/mysql55-mysqld
mkdir -p root/home/e-smith/db/mysql55


%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
    --dir /var/run/mysql55-mysqld 'attr(0755,mysql,mysql)' \
    --file /var/service/mysql55-mysqld/run 'attr(0755,root,root)' \
    --file /var/service/mysql55-mysqld/control/t 'attr(0750,root,root)' \
    --file /var/service/mysql55-mysqld/control/d 'attr(0750,root,root)' \
    --file /var/service/mysql55-mysqld/control/i 'attr(0750,root,root)' \
    --file /var/service/mysql55-mysqld/control/q 'attr(0750,root,root)' \
    --file /var/service/mysql55-mysqld/log/run 'attr(0755,root,root)' \
    --dir '/var/log/mysql55-mysqld' 'attr(2750,smelog,smelog)' \
    --dir '/home/e-smith/db/mysql55' 'attr(0750,root,root)' \
    > %{name}-%{version}-filelist
echo "%doc COPYING"          >> %{name}-%{version}-filelist

%clean 
rm -rf $RPM_BUILD_ROOT

%pre
%preun

%post
## mysql.com compatibility
#[ -e /etc/rc.d/init.d/mysql55-mysqld ] || ln -s ./mysql /etc/rc.d/init.d/mysql55-mysqld

%postun
#if [ "$1" == 0 ]; then
#  [ -L /etc/rc.d/init.d/mysql55-mysqld ] && rm /etc/rc.d/init.d/mysql55-mysqld || :
#fi

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
