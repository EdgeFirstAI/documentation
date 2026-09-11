# Release Notes

## Version 2026.08.0

Torizon for Maivin 2026.08.0 is a major platform release for Maivin and Raivin.  It moves the operating system to Torizon OS 7 and replaces the previous middleware packaging with the open source [EdgeFirst Perception Middleware](../../perception/index.md) services published from the [EdgeFirstAI GitHub organization](https://github.com/EdgeFirstAI).  The 2025.08 release candidates that some units received are superseded by this release.

The EdgeFirst services now run natively on the host as systemd services grouped under `maivin.target`.  Each service keeps a short name on Maivin, for example `camera.service` with its configuration in `/etc/default/camera`, and the previous `raivin.target` remains as a compatibility alias of `maivin.target`.  Refer to the [Configuration](../configuration/index.md) section for the service inventory and configuration files.

### Highlights

- **Torizon OS 7.7.0** (Yocto Scarthgap) with the PREEMPT-RT Linux 6.6.142 kernel and NetworkManager as the sole network manager.  The Wi-Fi access point, CAN bus, and automotive Ethernet configuration are covered in [Networking](../networking/networking.md).
- **EdgeFirst Perception Middleware** built from the [meta-edgefirst](https://github.com/EdgeFirstAI/meta-edgefirst) Yocto layer.  Camera, Model, Fusion, IMU, NavSat, Radar, LiDAR, Recorder, Replay, Web Server, and Web UI are all updated, see the component table below.
- **Hostname topic namespaces**.  Services publish on bare topics such as `camera/h264` inside a Zenoh session namespace equal to the device hostname, so the wire key is `verdin-imx8mp-XXXXXXXX/camera/h264`.  The legacy `rt/` prefix is no longer used by any stock service.  Refer to [Middleware Topics](../../perception/topics/index.md) for details and the [Known Issues](issues.md) for the impact on existing clients.
- **EdgeFirst Schemas 4.0 wire format**.  Camera frames are published as `edgefirst_msgs/CameraFrame` on `camera/frame`, replacing the `DmaBuffer` message on `camera/dma`.  The Model service publishes a unified `edgefirst_msgs/Model` message on `model/output` carrying boxes, masks, tracks, and timing.  Legacy `model/boxes2d` and `model/mask` topics are disabled by default and can be re-enabled through configuration.
- **Zenoh 1.10** router, C bindings, and Python bindings.
- **Model Zoo default model**.  The Model service ships with the [EdgeFirst Model Zoo](https://huggingface.co/EdgeFirst) YOLOv8n INT8 detection model installed under `/usr/share/edgefirst/modelzoo/` and uses the i.MX 8M Plus NPU through the TensorFlow Lite VX delegate.  The Model service also supports Ultralytics YOLO instance segmentation models exported with the EdgeFirst embedded configuration.
- **Camera capture modes**.  The Maivin camera exposes a `CAMERA_MODE` setting selecting the OS08A20 sensor readout, `1080p60` (default) or `4k`.  1080p60 capture, H.264 encoding, recording, and publisher export are verified on the release image.  Camera capture resilience improvements include retry on transient read failures, dropped frame telemetry, and a bounded service restart loop.
- **Web UI 4.4** with a redesigned landing page (Camera, LiDAR, Radar, IMU, and GPS views), a radar point cloud viewer, per-service settings pages backed by an atomic configuration API, and upload of MCAP recordings directly to EdgeFirst Studio from the MCAP dialog.
- **MCAP Recorder** records every active topic by default and embeds the current EdgeFirst Schemas definitions so recordings restore in EdgeFirst Studio.  The **EdgeFirst Publisher** (1.10) on the device exports recordings to the EdgeFirst Dataset Format 2026.04 and detects hostname namespaces automatically.
- **OSTree channels**.  Devices now track their release channel through the shipped deployment origin, so `sudo ostree admin upgrade` works with no arguments.  Refer to [Software Updates](updates.md).
- **Empty configuration values are treated as unset**.  A `KEY=""` line in `/etc/default/<service>` no longer prevents a service from starting.

### Resolved Issues

The following issues from the [Edge AI Middleware](https://au-zone.atlassian.net/browse/EDGEAI) project were resolved in this release.

| Issue | Summary |
|-------|---------|
| EDGEAI-1228 | Model Service issues found with the previous middleware builds |
| EDGEAI-1351 | Camera service does not start with "Invalid argument" |
| EDGEAI-1367 | Recorder service required a duration to be set before starting |
| EDGEAI-1389 | MCAP recorder updated to the latest EdgeFirst Schemas |
| EDGEAI-1390 | Publisher migrated to EdgeFirst Schemas 4.0 and direct-to-Studio publish |
| EDGEAI-1393 | Publisher schemas and direct-to-Studio publish verified on device |
| EDGEAI-1396 | Zenoh hostname topic namespacing, legacy `rt/` prefix dropped |
| EDGEAI-1403 | Camera capture resilience: timeout retry, dropped frame telemetry, tile FPS guard |
| EDGEAI-1438 | Camera service topic options are now settable from the configuration file |

Known issues and their workarounds are listed on the [Known Issues](issues.md) page.

### EdgeFirst Models

- EdgeFirst Model Zoo YOLOv8n detection and segmentation (INT8, i.MX 8M Plus NPU)
- ModelPack for detection and segmentation
- Ultralytics YOLO detection and instance segmentation
- RadarExp fusion models (ultra-short range) installed under `/usr/share/edgefirst/fusion/`

### EdgeFirst Packages

| Package | Version | Notes |
|---------|---------|-------|
| edgefirst-camera | 2.10.1 | `camera.service`, CameraFrame publishing, capture resilience |
| edgefirst-model | 2.10.2 | `model.service`, unified `model/output`, Model Zoo default model |
| edgefirst-fusion | 1.8.1 | `fusion.service`, disabled by default, radar late-fusion preconfigured |
| edgefirst-imu | 3.3.1 | `imu.service`, BNO08x transport fixes |
| edgefirst-navsat | 1.8.1 | `navsat.service` |
| edgefirst-radarpub | 1.7.2 | `radarpub.service`, disabled by default |
| edgefirst-lidarpub | 2.3.1 | `lidarpub.service`, disabled by default, Robosense E1R and Ouster |
| edgefirst-recorder | 1.10.1 | `recorder.service`, records all topics by default |
| edgefirst-replay | 2.3.1 | `replay.service`, see [Known Issues](issues.md) |
| edgefirst-websrv | 4.2.0 | `websrv.service`, configuration API and Studio uploads |
| edgefirst-webui | 4.4.0 | Web UI frontend served by `websrv` |
| edgefirst-schemas | 3.5.0 (C/Python), 4.0 wire format | Rust services pin schemas 4.0 |
| edgefirst-hal | 0.28.3 | Hardware abstraction library |
| videostream | 2.5.3 | Zero-copy camera frame sharing and codecs |
| edgefirst-client | 2.13.2 | EdgeFirst Studio CLI and Python bindings |
| edgefirst-publisher | 1.10.1 | MCAP to EdgeFirst Dataset Format export |
| mcap | 0.0.58 | MCAP command line tool |
| zenohd, zenoh-c, python3-zenoh | 1.10.1 | Zenoh router and bindings |

### System Packages

- Torizon OS 7.7.0 (Yocto Scarthgap)
- Linux 6.6.142-rt75 (Toradex BSP 7, PREEMPT-RT), reported as `6.6.142-rt75-2026.08.0` by `uname -r`
- TensorFlow Lite 2.16.2 with the VX delegate for the i.MX 8M Plus NPU
- TIM-VX 1.2.2
- NetworkManager, ModemManager, hostapd
- gpsd, chrony, and linuxptp for GNSS disciplined time synchronization
- Docker container engine for user applications

### Upgrade Notes

- **Topic names**.  Clients that subscribe to `rt/...` topics will not receive data from 2026.08.0 services.  Subscribe to the bare topic name from a Zenoh session using the device hostname as the namespace, or use a wildcard such as `**/camera/h264`.  Refer to [Middleware Topics](../../perception/topics/index.md).
- **Camera frames**.  Applications consuming `camera/dma` must migrate to `camera/frame` and the `CameraFrame` schema from EdgeFirst Schemas 4.0.
- **Model output**.  Applications consuming `model/boxes2d` or `model/mask` should migrate to `model/output`, or re-enable the legacy topics with the `DETECT_TOPIC` and `MASK_TOPIC` settings in `/etc/default/model`.
- **Configuration files**.  The configuration files under `/etc/default/` persist across OSTree upgrades.  A file that was modified on a previous release keeps its previous contents and will not receive keys added in this release.  Compare against the shipped defaults in `/usr/etc/default/` and refer to [Configuration](../configuration/index.md) to restore defaults.
- **Default model**.  The ModelPack people models previously installed under `/usr/share/model` are no longer shipped.  The Model service defaults to the Model Zoo YOLOv8n detector.  Upload your own model following [Uploading Models](model_uploads.md).

## Version 2025.01

This is the first official release of the Maivin Perception Platform.

For Maivin users this software release is a major upgrade which unifies the Torizon for Maivin branches of Raivin and Maivin into a single software release.  As part of this release the version naming has been updated to follow the the YEAR.MONTH.PATCH format instead of using the Torizon version number as the base.  The YEAR and MONTH refer to the data of the initial release of the software and the PATCH will be included for incremental patch release within this release cycle.  The upstream Torizon OS version number is documented in the release notes.

This release includes a major update to the Web UI interface of the Maivin Perception Platform.  The new interface provides a collection of panels that can be used to monitor and control the platform.  The primary page for the Maivin is the "Segmentation View" page, where the Raivin provides a combined segmentation view and occupancy grid panel.  The Web UI also provides a page for only the occupancy grid.  Configuration pages have been added allowing the user to configure various aspects of the Maivin platform. Currently, configuration is focused on the EdgeFirst Middleware services but future updates plan to add networking and other configuration options.

### EdgeFirst Models

- ModelPack for Detection and Segmentation
- RadarExp Fusion Model

### EdgeFirst Packages

- Camera
- Radarpub
- Model
- Fusion
- IMU
- NavSat
- Recorder
- Playback
- Web UI
- Web Server

### System Packages

- Torizon 6.8.1
- Linux 5.15.148
