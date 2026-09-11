# Radar Module

The Raivin configuration includes an integrated [DRVEGRD-169 radar module][radar] from [smartmicro][smart].  The radar module is internally connected to the Raivin which provides power and data communications interfaces.  The primary data and control interface uses the CAN bus protocol.  The radar module is also connected through an internal automotive Ethernet interface which is used to transmit the [radar data cube][cube] used by the RadarExp Fusion model.

## Specifications

The DRVEGRD 169 radar module is a 79GHz radar sensor for multiple automotive applications that features 4D/PxHD technology.  The sensor's antenna aims at ultra-short, short and medium range applications with a very wide, horizontal angular coverage of 140°.  A full set of the radar module specifications can be found on the [smartmicro DRVEGRD product page][radar].

## Networking

The radar module is connected to the Raivin using two networking interfaces.  The primary interface is the `can0` interface which is used to configure the radar module and receive the radar point-cloud.  This interface is required to control the radar module.  The secondary interface is the `ethernet1` interface which is used to transmit the radar data cube to the Raivin.  This interface is required to provide input to the RadarExp Fusion model, but is not required for the radar module to function in point-cloud mode.  The radar data cube generates about 300Mb/s of data which is transmitted to the Raivin for processing.

### CAN Configuration

NetworkManager does not manage CAN interfaces, so the CAN bus is configured by the `can0.service` systemd unit which brings the interface up at 500 kbps whenever the CAN hardware is present.

```ini
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/sbin/ip link set can0 type can bitrate 500000
ExecStart=/sbin/ip link set can0 up
ExecStop=/sbin/ip link set can0 down
```

The [Radar Publishing Service](../configuration/radar.md) manages the radar configuration and reading of the point-cloud data over CAN and publishing the results over Zenoh.  Refer to the [radar topics](../../perception/topics/radar.md) for details.

### Ethernet Configuration

The radar module streams the low-level radar data cube over a 1000Base-T1 automotive Ethernet link which is internally connected to the Raivin's `ethernet1` interface.  The connection is managed by NetworkManager through the `ethernet1-radar` connection profile which assigns the static address `192.168.11.17/24` and uses policy routing so the sensor traffic never becomes the default route.  The `ethernet1-master.service` systemd service configures the automotive Ethernet PHY as the link master before the radar publisher starts.

```bash
$ nmcli -t connection
network0:...:802-3-ethernet:ethernet0
ethernet1-radar:...:802-3-ethernet:ethernet1
```

The `ethernet1-lidar` profile assigns the address used by the [LiDAR module](lidar.md) to the same port.  Only one of the two profiles is active at a time and the switch is made with `nmcli`.

```bash
sudo nmcli connection down ethernet1-lidar
sudo nmcli connection up ethernet1-radar
```

The Raivin runs a PTP grandmaster on `ethernet1` so that sensors on the port can synchronize their clocks to the GNSS disciplined system clock, refer to [Networking](../networking/networking.md#sensor-network) for details.

[radar]: https://www.smartmicro.com/automotive-radar/drvegrd-line#c20151
[smart]: https://www.smartmicro.com/
[cube]: https://www.mathworks.com/help/phased/gs/radar-data-cube.html
