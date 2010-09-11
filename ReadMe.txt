[V2.3.0.4]
1. Fix ATE cannot switch Channel issue.
2. Fix ATE calibrate TX Power not work correctly issue.

[2.3.0.3]
1. Add "RESOURCE_PRE_ALLOC" support.

[2.3.0.2]
1. Add DWA-121(RT8070) VID/PID.
2. Fix wap_supplicant countermeasure re-connect issue.

[2.3.0.1]
1. Fix Shared WEP security mode can't work on wpa_supplicant wext driver.
2. Fix Hidden SSID can't work on wpa_supplicant wext driver.
3. Fix AdHoc mode can't work on wpa_supplicant wext driver.

[2.3.0.0]

1. Support PSP XLINK in ad-hoc mode.

2. Add mac80211 iw utility other commands support.

3. Fix issue: The start address of HeaderBuf must be aligned by 4 when

   VENDOR_FEATURE1_SUPPORT is enabled.

4. WMM ACM: see history of acm_comm.c.

5. Support WpaSupplicant(v0.6.9) WPS

6. Fix WPS issue: Check SelectRegistrar is TRUE or FALSE

7. Fix WPS issue: Some AP (ex. Buffalo WZR-AG300NH) would change SSID to another SSID after push WPS PBC button.

                                             After WPS process finish, change SSID to original SSID.

                                             Driver needs to wait AP to re-generate Beacon; otherwise, driver will update this PBC SSID to MlmeAux.

8. Shorten the waiting time when unplug the device.

9. Fix mgmt ring full issue: It happened only in big-endian platform and quickly switch the network type between Infra and Adhoc mode.

10. Fix statistics issue: It happened in big-endian platform, tx count would be zero.

11. Support WiFi Draft_3.0 11n test items.

12. Support Linux Kernel 2.6.31

13. Support Ad-hoc WPS2PSK/AES (DPO doesn't support this item)

14. Support Samsung Auto Provision (only for Samsung Project)

15. For GPL issue: Separate three kernel modules - util module, driver module, netif module. util module and netif module could license GPL.

16. Support CFG80211 of Linux Kernel 2.6.32

                                              Driver module couldn't license GPL.

