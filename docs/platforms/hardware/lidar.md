# LiDAR Module

The Raivin configuration includes optional support for LiDAR sensors which provide high-resolution 3D point cloud data useful for creating ground-truth annotations.  The [LiDAR publishing service](../configuration/lidar.md) supports two sensor families:

- The [Robosense E1R][robosense] solid-state LiDAR, which is the default sensor type of the LiDAR service.  Calibration profiles for mounting the E1R on the Maivin are provided and the sensor's built-in IMU enables the ground plane filter of the LiDAR service.
- The [Ouster OS1-64 LiDAR sensor][ouster] spinning LiDAR.  A mounting kit for the Ouster is available from Au-Zone to attach the Raivin to the Ouster and calibration profiles for this mounting configuration are provided.

The LiDAR sensor is connected to the Raivin's sensor Ethernet port, providing both data communication and power over Ethernet (PoE) capabilities.  The sections below describe the Ouster OS1 configuration.

<iframe width="560" height="315" src="https://www.youtube.com/embed/LuA3JlRUfVY?si=FFKDY7dBWih5aG2W" title="Raivin Unboxing and LiDAR Mounting" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Specifications

The Ouster OS1-64 is a high-resolution imaging LiDAR sensor with the following key specifications:

- **Range**:
    - 100m @ >90% detection probability (80% Lambertian reflectivity)
    - 45m @ >90% detection probability (10% Lambertian reflectivity)
- **Field of View**:
    - Vertical: 45° (+22.5° to -22.5°)
    - Horizontal: 360°
- **Resolution**:
    - Vertical: 64 channels
    - Horizontal: Configurable (512, 1024, or 2048 points per rotation)
- **Data Rate**: 129 Mbps (64 channel mode)
- **Points Per Second**: 1,310,720 (64 channel mode)
- **Rotation Rate**: 10 or 20 Hz (configurable)
- **Power Consumption**: 14-20W (22W peak at startup)
- **Operating Voltage**: 22-26V, 24V nominal

A full set of the LiDAR sensor specifications can be found in the [Ouster OS1 datasheet][datasheet].

## Ouster Studio

Ouster Studio is a free digital LiDAR visualizer available for both web and desktop platforms. It provides a comprehensive solution for viewing, organizing, and sharing LiDAR point cloud data captured by Ouster OS series sensors. Download the [Ouster Studio][studio]

### Desktop Application

- Live streaming and recording of LiDAR data
- Real-time visualization
- Sensor discovery and configuration
- Cloud integration for data uploading and sharing

### Sensor configuration

Once you have downloaded Ouster Studio it can be used get the device name as well as make modifications to the Static IP of the device. It is recommended that the user sets a static ip as shown in the image below.

{{ figure("../assets/hardware/ouster-config.png", "Ouster Config") }}

After making all the changes required you can hit "Configure and Visualize" and it will show a LiDAR PCD as follow

{{ figure("../assets/hardware/ouster-pcd.png", "Ouster PCD") }}

## Networking

The LiDAR connects to the Raivin's `ethernet1` sensor port which is managed by NetworkManager.  The `ethernet1-lidar` connection profile assigns the static address `192.168.1.102/24` to the port, configure the LiDAR with a static address on the same subnet and set it as the [Target Device](../configuration/lidar.md#target-device) of the LiDAR service.  The profile is not active by default as the port is shared with the radar module, activate it when provisioning the LiDAR.

```bash
sudo nmcli connection down ethernet1-radar
sudo nmcli connection up ethernet1-lidar
```

The Raivin runs a PTP grandmaster on the sensor port, so the LiDAR can be configured to synchronize its clock to the Raivin by selecting the `ptp1588` [timestamp mode](../configuration/lidar.md#timestamp-mode).  Refer to [Networking](../networking/networking.md#sensor-network) for details.

## Firmware Requirements

The sensor should be running firmware version v2.5.3 or later. The sensor's local information page can be accessed at:

```text
http://os-<serial_number>.local/
```

### Data Format

The LiDAR sensor outputs data in the following formats:

- MCAP files for recorded data
- PCAP files for recorded data
- Live UDP stream over Ethernet

Each point in the point cloud contains:

- Range
- Signal
- Reflectivity
- Near-infrared
- Channel
- Azimuth angle
- Timestamp

## Configuration

### Azimuth Orientation

The 0° azimuth angle aligns with the RJ45 Ethernet connector on the Ouster OS1 sensor. Azimuth angles increase counterclockwise when viewed from above:

- 0°: Towards the Ethernet connector
- 90°: A quarter turn counterclockwise
- 180°: Opposite the connector
- 270°: Three-quarters counterclockwise from the connector

The LiDAR settings can be configured using the Web UI [LiDAR Settings page](../configuration/lidar.md)

{{ figure("../assets/lidar-config.png", "LiDAR Azimuth Orientation") }}

## Data Visualization

The LiDAR data can be visualized using:

1. Raivin Web UI [LiDAR page](../quickstart/raivin/webui.md#the-lidar-page) for both live and recorded MCAPs
2. Rerun visualization tool for both PCAP files and live data
3. Ouster Studio for live or recorded data

## Additional Resources

- [Ouster Sensor Documentation][docs]
- [Ouster OS1 Datasheet][datasheet]
- [Sensor Data Format Documentation][dataformat]

[ouster]: https://ouster.com/products/os1-lidar-sensor/
[robosense]: https://www.robosense.ai/en/rslidar/E1R
[studio]: https://ouster.com/products/software/ouster-studio
[datasheet]: https://data.ouster.io/downloads/datasheets/datasheet-revd-v2p0-os1.pdf
[docs]: https://static.ouster.dev/sensor-docs/
[dataformat]: https://static.ouster.dev/sensor-docs/image_route1/image_route2/sensor_data/sensor-data.html
