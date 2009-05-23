%define SourceName 2009_0520_RT3070_Linux_STA_v2.1.1.0

Name:		rt3070
Version:	2.1.1.0
Release:	1%{?dist}
Summary:	Common files for RaLink rt3070 kernel driver
Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/ralink/Home/Support/Linux.html
Source0:	http://www.ralinktech.com.tw/data/drivers/%{SourceName}.tar.gz
Source1:	http://www.ralinktech.com.tw/data/drivers/ReleaseNote-RT3070.txt
Source2:	suspend.sh
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
Provides:	%{name}-kmod-common = %{version}
Requires:	%{name}-kmod >= %{version}

%description
This package contains the linux kernel module files for the Ralink rt3070
driver for WiFi, a linux device driver for USB 802.11a/b/g universal NIC cards
that use Ralink rt307x chipsets.

%prep
%setup -q -n %{SourceName}

# Fix bunch of encoding issues
cp -a %{SOURCE1} .
for file in ReleaseNote* sta_ate_iwpriv_usage.txt README_STA*; do
	iconv -f JOHAB -t UTF8 $file -o $file.tmp
	sed 's/\r//' $file.tmp > $file.tmp2
	mv -f $file.tmp2 $file
done

# To avoid possible conflict with rt2870 driver:
for sta in include/os/rt_linux.h os/linux/Makefile.6 README_STA* RT2870STACard.dat ; do
 sed 's|RT2870STA|RT3070STA|g' $sta > tmp.sta
 touch -r $sta tmp.sta
 mv tmp.sta $sta
done

%build
echo "Nothing to build."
sleep 1m

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/
install -pm 0644 RT2870STA.dat $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/RT3070STA.dat
install -pm 0644 RT2870STACard.dat $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/RT3070STACard.dat

cp -a %{SOURCE2} .

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README_STA* *.txt suspend.sh
%dir %{_sysconfdir}/Wireless
%dir %{_sysconfdir}/Wireless/RT3070STA
%config(noreplace) %{_sysconfdir}/Wireless/RT3070STA/RT3070STA*.dat

%changelog
* Fri May 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-1
- update to 2.1.1.0

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1.0-3
- rebuild for new F11 features

* Tue Mar 10 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 2.0.1.0-2
- Add suspend script (RPMFusion BZ#199)

* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.0.1.0-1
- Initial build
