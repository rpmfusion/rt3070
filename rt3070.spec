%define SourceName DPO_RT3070_LinuxSTA_V2.3.0.4_20100604

Name:		rt3070
Version:	2.3.0.4
Release:	2%{?dist}
Summary:	Common files for RaLink rt3070 kernel driver
Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/support.php?s=2
# No more direct link. The file is downloaded from the above page.
Source0:	%{SourceName}.tar.bz2
Source1:	ReadMe.txt
# Alternative suspend script. Might not be necessary anymore.
# Kept for historical reasons.
Source2:	suspend.sh
# Blacklist the module shipped with kernel
Source3:	blacklist-rt2800usb.conf
# Needed for WPA2 support (RFBZ #664)
Patch0:		rt3070-allowTKIP.patch
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
%patch0 -p1

cp -a %{SOURCE1} .
cp -a %{SOURCE2} .

# Fix bunch of encoding issues

for file in ReadMe.txt *iwpriv_usage.txt LICENSE\ ralink-firmware.txt README_STA*; do
	chmod -x "$file"
	iconv -f JOHAB -t UTF8 "$file" -o "$file.tmp"
	sed 's/\r//' "$file.tmp" > "$file.tmp2"
	mv -f "$file.tmp2" "$file"
done

# To avoid possible conflict with rt2870 driver:
for sta in common/rtmp_init.c include/rt_ate.h include/os/rt_linux.h README_STA* RT2870STACard.dat ; do
 sed 's|RT2870STA|RT3070STA|g' $sta > tmp.sta
 touch -r $sta tmp.sta
 mv tmp.sta $sta
done

%build
sleep 1m

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/
install -pm 0644 RT2870STA.dat $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/RT3070STA.dat
install -pm 0644 RT2870STACard.dat $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/RT3070STACard.dat
%if 0%{fedora} < 15
install -dm 755 $RPM_BUILD_ROOT/%{_sysconfdir}/modprobe.d/
cp -a %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/modprobe.d/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README_STA_usb *.txt suspend.sh LICENSE*.txt
%dir %{_sysconfdir}/Wireless
%dir %{_sysconfdir}/Wireless/RT3070STA
%config(noreplace) %{_sysconfdir}/Wireless/RT3070STA/RT3070STA*.dat
%if 0%{fedora} < 14
%config(noreplace) %{_sysconfdir}/modprobe.d/blacklist-rt2800usb.conf
%endif

%changelog
* Thu Dec 02 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.3.0.4-2
- Rebuild. Somehow the package did not end up in the F-14 repo.

* Tue Aug 31 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.3.0.4-1
- Update to 2.3.0.4

* Sun Jun 27 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.3.0.2-1
- Update to 2.3.0.2

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
