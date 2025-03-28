# Networking

Torizon for Maivin uses the standard [NetworkManager][nm] framework for managing system networking.  NetworkManager is used by most Linux distributions and can manage all of the system's networking interfaces, including the optional LTE modem, and be used to configure VPN connections.

As noted in the Quick Start, the Maivin can be discovered on a network using the `verdin-imx8mp-XXXXXXXX.local` hostname where the 'XXXXXXXX' is the eight-digit serial number of the unit.  The serial number can be found on the rear sticker near the connection ports.

This chapter documents the most common networking configurations for the Maivin.  For further detailed documentation, please refer to the [NetworkManager Documentation][nm].

## Network Interfaces

The Maivin includes a number of networking interfaces: Ethernet, WiFi, and an optional LTE modem.  The interface names and ports are described in the table below.  The `ethernet1` and `can0` interfaces are internal-only interfaces used by the Raivin to communicate with the internal radar module.  The remaining interfaces are user configurable.

| Name             | ID        | Details                                         |
| ---------------- | --------- | ----------------------------------------------- |
| Gigabit Ethernet | ethernet0 | RJ-45 port on the rear of the Maivin            |
| WiFi Client      | mlan0     | WiFi client interface                           |
| WiFi AP          | uap0      | WiFi Access Point interface                     |
| LTE Modem        | wwan0     | Optional LTE Modem using internal m.2 expansion |
| Radar Ethernet   | ethernet1 | Internal 1000BaseT1 interface to the Radar      |
| CAN Bus          | can0      | Internal CAN interface to the Radar             |

## Ethernet Setup

The Maivin ships with the Ethernet interface setup as a DHCP client and should automatically get an IP address on a network which provides DHCP.  Otherwise the Maivin will fallback to a link-local IP.  In either scenario, the Maivin can be accessed using the `verdin-imx8mp-XXXXXXXX.local` hostname.

```{note}
The Maivin also supports IPv6 which will be available through a link-local address.  This IPv6 link-local address will be assocated with the `verdin-imx8mp-XXXXXXXX.local` hostname.
```
```{tip}
If connecting to the Maivin using a Windows PC, either with an SSH client or a web browser, adding the ".local" suffix is optional.  For Linux or Mac machines, the suffix must be used.
```

Once connected to the Maivin, standard Linux tools are available for listing the network interfaces and their current status.  NetworkManager offers the `nmcli` command-line tool for querying the status of the interfaces it manages; for example, the `nmcli connection` command is shown below.  We see the connection names `network0` and `network1` which are associated to the network interfaces `ethernet0` and `ethernet1`, respectively.  The connection names can be user defined, by default the `networkX` convention is followed which maps `X` to the equivalent `ethernetX` interface.

```bash
$ nmcli -t connection
network0:958cc5e3-1bbf-3d64-beeb-020d4414e254:802-3-ethernet:ethernet0
network1:78c31df4-8c89-31a6-9aeb-d5603e230e4e:802-3-ethernet:ethernet1
```

```{tip}
When using `nmcli`, the -t parameter is used to provide simpler text output.  Without it, the rich console interface is used which requires an appropriate terminal to display correctly.  If you find the output of nmcli visually erroneous, use the -t parameter.
```

```{tip}
The `nmcli` sub-commands can be abbreviated.  For example, `nmcli connection` can simply be entered as `nmcli c`.
```

Other standard Linux tools such as `ifconfig`, `ip`, and `ethtool` are also available.  For example, `ifconfig` can be used to see the link status and IP address along with other details.

```bash
$ ifconfig ethernet0
ethernet0 Link encap:Ethernet  HWaddr 00:14:2D:E7:08:E3  
          inet addr:10.10.41.226  Bcast:10.10.47.255  Mask:255.255.248.0
          inet6 addr: fe80::1cc:4f8d:9ea2:815/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:2091191 errors:0 dropped:0 overruns:0 frame:0
          TX packets:251375 errors:2 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:188791038 (180.0 MiB)  TX bytes:329873651 (314.5 MiB)
          Interrupt:52
```

### Static IP

The Maivin can be configured to use a static IP for ethernet using the NetworkManager command-line tool.  You will need to know the desired IP address and subnet mask.  You will also need the gateway and DNS IP address, if required for Internet access.

First, you must identify the connection name of the interface you wish to configure with a static IP.  The external gigabit ethernet interface `ethernet0` has the connection name `network0` by default, which we can see in the first column of the output.  You will use this connection name in the following commands.

```bash
$ nmcli -t c
network0:958cc5e3-1bbf-3d64-beeb-020d4414e254:802-3-ethernet:ethernet0
```

The following steps are then followed to configure the static IP address.  Note that the network bitmask (or netmask) is provided in [Classless Inter-Domain Routing (CIDR)][cidr] format.  This lists the numbers of bits to set in the IP address as belonging to the network.  For example, the netmask '255.255.255.0' has the first 24 bits set (each 255 is 8 bits), so the netmask is set using `/24`.  You may need to adjust this according to your specific network configuration.

1. Set the static IP address:
   - `nmcli con mod network0 ipv4.addresses 192.168.1.10/24`
2. Set the gateway, if required:
   - `nmcli con mod network0 ipv4.gateway 192.168.1.1`
3. Set the DNS, if required:
   - `nmcli con mod network0 ipv4.dns 8.8.8.8`
4. Set the IPv4 method to manual:
   - `nmcli con mod network0 ipv4.method manual`
5. Finally, bring up the new configuration (or sudo reboot the unit):
   - `nmcli con up network0`

The device should now be configured with the new static IP address.

```{warning}
The internal Ethernet1 interface uses the 192.168.11.0/24 network to communicate with the radar module.  Do not configure the static IP address to reside on this network.
```
```{warning}
The `ipv4.addresses` element must be configured before switching the IPv4 method to manual.
```
```{warning}
Calling the `connection up` command while connected through this interface can cause the link to drop.  Reconnect using the new address.  An alternate to the `connection up` command is to use `sudo reboot` to restart the device.
```

### Re-enable DHCP

To revert the connection to using DHCP you must follow these steps.

1. Configure automatic (DHCP) mode:
   - `nmcli con mod network0 ipv4.method auto`
2. Remove the previous static addresses:
   - `nmcli con mod network0 ipv4.addresses ""`
3. Remove the previous gateway:
   - `nmcli con mod network0 ipv4.gateway ""`
4. Remove the previous DNS:
   - `nmcli con mod network0 ipv4.dns ""`
5. Activate the changes:
   - `nmcli con up network0`

### Mixed Static and DHCP

NetworkManager allows mixed static and DHCP configurations.   If you configure `ipv4.method auto` you can still configure some of the other IPv4 parameters statically.

## WiFi Client Setup

Maivin units with WiFi can be configured to connect to a WiFi Access Point (AP).  Refer to the next section if you instead want to use your Maivin as a WiFi AP.

```{warning}
FCC regulations require special certifications for colocated transmitters (a device with multiple RF transmitters).  Maivin and Raivin are not currently certified for colocated transmitters so users must not enable more than one of the WiFi, Modem, or Radar without first receiving FCC certification.  Refer to regulatory boards in your jurisdiction for your relevant regulations.
```

NetworkManager handles the WiFi client configuration.  Follow these steps to connect to an AP, you will need to know the AP Service Set Identifer (SSID, usually the network name) and the password, if required.

1. First scan for available WiFi networks to join:
   - `nmcli device wifi list`
2. Connect to the desired WiFi network using the SSID:
   - `nmcli -a device wifi connect <SSID>`
3. Enter the password, if needed, when prompted.
4. Confirm the `mlan0` interface is up and has received an IP address:
   - `ifconfig mlan0`

## WiFi AP Setup

Maivin units with WiFi can be configured as an AP allowing client devices to connect to the Maivin.  Instead of using NetworkManager, we use the [Host AP daemon (hostapd)][hostapd].

```{warning}
FCC regulations require special certifications for colocated transmitters (a device with multiple RF transmitters).  Maivin and Raivin are not currently certified for colocated transmitters so users must not enable more than one of the WiFi, Modem, or Radar without first receiving FCC certification.  Refer to regulatory boards in your jurisdiction for your relevant regulations.
```

WiFi AP mode is configured using the `hostapd` service in Linux.  We describe a common WiFi AP configuration; for more advanced setup, please refer to the [hostapd documentation][hostapd].

To enable the Maivin Access Point with default configurations simply enable the `hostapd` service.

```bash
sudo systemctl enable hostapd
sudo systemctl start hostapd
```

The Maivin ships with a default hostapd configuration which can be modified for your needs.  The following shows the base configuration which ships with Maivin. The full list of configuration options is documented in the [hostapd.conf][hostapd.conf] reference file.

```
ssid=Maivin
wpa_passphrase=maivin
own_ip_addr=10.10.10.1
interface=uap0

country_code=CA
hw_mode=a
channel=40

ieee80211ac=1
ieee80211n=1
ieee80211w=2
wmm_enabled=1

auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_pairwise=CCMP
sae_require_mfp=1

ht_capab=[LDPC][HT40+][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][DSSS_CCK-40]
```

```{warning}
Please make sure to change the default password before enabling WiFi AP mode!
```

The WiFi AP network configuration file is found under `/etc/systemd/network/hostapd.network` and is managed by [systemd][sysd].  The following is the default configuration.  The full list of configuration options is documented in the [systemd network manual][networkd].

```
[Match]
Name=wlan0 uap0
WLANInterfaceType=ap

[Network]
Address=10.10.10.1/24
DHCPServer=true
IPMasquerade=yes
IPForward=ipv4

[DHCPServer]
PoolOffset=100
PoolSize=100
```

```{warning}
If you change the network address in `hostapd.network`, make sure it matches the address in `hostapd.conf`!
```

## LTE Modem Setup

Maivin provides an m.2 expansion port which can be used to add an LTE modem to the device.  We offer Maivin and Raivin units pre-configured with an LTE modem and SIM card or a modem can be added by customers themselves following the instructions at the end of this section.

```{warning}
FCC regulations require special certifications for colocated transmitters (a device with multiple RF transmitters).  Maivin and Raivin are not currently certified for colocated transmitters so users must not enable more than one of the WiFi, Modem, or Radar without first receiving FCC certification.  Refer to regulatory boards in your jurisdiction for your relevant regulations.
```

### Modem Configuration

The modem in the Maivin is configured through [ModemManager][mm], which is a companion framework to NetworkManager but specializing in modem configuration.  Before you start, you need to ensure the modem is installed into the Maivin along with the SIM card and that you have the correct Access Point Name (APN) configuration string from your LTE carrier.

We describe the common modem configuration in this section.  For further details of the modem features and configuration, please refer to the [ModemManager Documentation][mm].

#### Configure m.2 Port

To configure the modem, we first need to ensure the m.2 expansion port is configured for the correct operating mode.  The expansion port supports PCI and USB operating mode and the correct one needs to be configured in the device tree.  Most modems use USB.  The device tree is configured through the `/etc/overlays.txt` file, so please make sure the entry `maivin2-m2usb.dtbo` is listed.

```bash
$ cat /etc/overlays.txt
fdt_overlays=maivin2.dtbo maivin2-os08a20.dtbo maivin2-m2usb.dtbo
```

```{warning}
The `maivin2.dtbo` overlay must always be present first.  Care must be taken when adjusting the device tree overlays as errors will cause boot failures!
```

#### Verify Modem Found

After confirming the correct device tree overlays are configured and rebooting the Maivin, you can verify the modem has been found.  For USB modems, the `lsusb` command is used, in the example below we see a Telit LN920 modem has been found.

```bash
$ lsusb
Bus 002 Device 002: ID 1bc7:1060 Telit Wireless Solutions LN920
```

#### Configure Networking

With the m.2 expansion and modem configured and detection verified the networking can now be configured.

First we must enable the ModemManager service which is disabled by default on Maivin.

```bash
sudo systemctl enable ModemManager
sudo systemctl start ModemManager
```

Next we can confirm that the modem and SIM card are found.

```bash
$ mmcli -m 0
  ----------------------------------
  General  |                   path: /org/freedesktop/ModemManager1/Modem/0
           |              device id: 7d04c0ee5027689a762768e20387443c2eb574ea
  ----------------------------------
  Hardware |           manufacturer: Telit
           |                  model: LN920A6-WW
           |      firmware revision: M0L.010002
           |         carrier config: default
           |           h/w revision: 1.10
           |              supported: gsm-umts, lte
           |                current: gsm-umts, lte
           |           equipment id: 352214163072532
<additional output removed>
```

```{note}
If `mmcli -m 0` returns the error "error: couldn't find the ModemManager process in the bus", then you need to first start the service using `sudo systemctl start ModemManager`.
```

```{note}
If `mmcli -m 0` returns the error "error: couldn't find modem", then wait a few minutes before trying again.  Modem startup can take a while.  If the modem is still not found, please contact support.
```

Now that the modem is properly detected by ModemManager, we switch to NetworkManager to configure the network.

```{warning}
Take careful note of the commands, as `mmcli` for ModemManager and `nmcli` for NetworkManager look very similar.
```

1. First we create a new NetworkManager connection for the cellular modem and provide the APN string which will be provided to you by your service provider:
   - `nmcli connection add type gsm ifname "*" con-name "Cellular Connection" autoconnect yes gsm.apn <APN_FROM_CARRIER>`
2. Next you can bring up the newly created connection:
   - `nmcli connection up "Cellular Connection"`
3. Then you can verify the connection is up:
   - `nmcli -c no connection show`

Once properly configured the `wwan0` interface can also be queried through `ifconfig`.

### Modem Installation

The modem installation can be performed by customers by following these instructions.  If your modem and service provide require physical SIM card installation that is also possible during installation.

```{warning}
Installing an LTE modem is an advanced configuration which requires opening up the Maivin.  Extreme caution should be followed during this procedure.  We suggest ordering Maivin or Raivin units with the LTE option pre-configured.
```

## Radar Networking

The `ethernet1` and `can0` interfaces are reserved for internal communications with the radar module on Raivin configurations.  Refer to the Radar chapter for details.


[nm]: https://networkmanager.dev
[mm]: https://modemmanager.org
[cidr]: https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing
[hostapd]: https://wireless.docs.kernel.org/en/latest/en/users/documentation/hostapd.html
[hostapd.conf]: https://w1.fi/cgit/hostap/plain/hostapd/hostapd.conf
[sysd]: https://systemd.io/
[networkd]: https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html