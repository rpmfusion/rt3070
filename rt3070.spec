%define SourceName 2009_0525_RT3070_Linux_STA_v2.1.1.0

Name:		rt3070
Version:	2.1.1.0
Release:	3%{?dist}.1
Summary:	Common files for RaLink rt3070 kernel driver
Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/ralink/Home/Support/Linux.html
Source0:	http://www.ralinktech.com.tw/data/drivers/%{SourceName}.bz2
Source1:	http://www.ralinktech.com.tw/data/drivers/ReleaseNote-RT3070.txt
# Alternative suspend script. Might not be necessary anymore.
# Kept for historical reasons.
Source2:	suspend.sh
# Blacklist the module shipped with kernel
Source3:	blacklist-rt2800usb.conf
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
# Needed for WPA2 support (RFBZ #664)
sed -i 's|HT_DisallowTKIP=1|HT_DisallowTKIP=0|' RT2870STA.dat
sleep 1m

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/
install -pm 0644 RT2870STA.dat $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/RT3070STA.dat
install -pm 0644 RT2870STACard.dat $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/RT3070STACard.dat

cp -a %{SOURCE2} .

install -dm 755 $RPM_BUILD_ROOT/%{_sysconfdir}/modprobe.d/
cp -a %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/modprobe.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README_STA_usb *.txt suspend.sh
%dir %{_sysconfdir}/Wireless
%dir %{_sysconfdir}/Wireless/RT3070STA
%config(noreplace) %{_sysconfdir}/Wireless/RT3070STA/RT3070STA*.dat
%config(noreplace) %{_sysconfdir}/modprobe.d/blacklist-rt2800usb.conf

%changelog
* Fri Dec 04 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-3.1
- Blacklist kernel's rt2800usb module

* Tue Aug 04 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-3
- *sigh* Upstream made a release without bumping the version

* Wed Jun 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-2
- Modify RT3070STA.dat to support WPA2 (RFBZ #664)

* Fri May 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-1
- update to 2.1.1.0

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1.0-3
- rebuild for new F11 features

* Tue Mar 10 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 2.0.1.0-2
- Add suspend script (RPMFusion BZ#199)

* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.0.1.0-1
- Initial build
