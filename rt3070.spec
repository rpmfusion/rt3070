%define SourceName 2008_1225_RT3070_Linux_STA_v2.0.1.0

Name:		rt3070
Version:	2.0.1.0
Release:	1%{?dist}
Summary:	Common files for RaLink rt3070 kernel driver
Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/ralink/Home/Support/Linux.html
Source0:	http://www.ralinktech.com.tw/data/drivers/%{SourceName}.tar.bz2
Source1:	http://www.ralinktech.com.tw/data/drivers/ReleaseNote-RT3070.txt
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
Provides:	%{name}-kmod-common = %{version}
Requires:	%{name}-kmod >= %{version}

%description
This package contains the linux kernel module files for the Ralink rt3070
driver for WiFi, a linux device driver for 802.11a/b/g universal NIC cards -
either PCI, PCIe or MiniPCI - that use Ralink rt307x chipsets.

%prep
%setup -q -n %{SourceName}
iconv -f JOHAB -t UTF8 %{SOURCE1} -o ./ReleaseNotes
sed -i 's/\r//' ./ReleaseNotes
iconv -f JOHAB -t UTF8 README_STA -o README_STA
sed -i 's/\r//' README_STA
# To avoid possible conflict with rt2870 driver:
for sta in include/rt_linux.h README_STA ; do
 sed 's|RT2870STA|RT3070STA|g' $sta > tmp.sta
 touch -r $sta tmp.sta
 mv tmp.sta $sta
done

%build
echo "Nothing to build."

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/
install  -p -m 0644 RT2870STA.dat $RPM_BUILD_ROOT/%{_sysconfdir}/Wireless/RT3070STA/RT3070STA.dat

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ReleaseNotes README_STA iwpriv_usage.txt
%dir %{_sysconfdir}/Wireless
%dir %{_sysconfdir}/Wireless/RT3070STA
%config(noreplace) %{_sysconfdir}/Wireless/RT3070STA/RT3070STA.dat

%changelog
* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.0.1.0-1
- Initial build
