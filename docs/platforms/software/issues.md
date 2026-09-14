# Known Issues

This page lists the customer-visible issues known on the current Torizon for Maivin release along with their workarounds.  When reporting an issue to Au-Zone support, please include the release information from `/etc/os-release` (the `VERSION_ID` and `BUILD_ID` fields), the issue key from this page when applicable, the steps to reproduce, and whether the camera was running in the `1080p60` or `4k` [camera mode](../configuration/camera.md#camera-mode).

## Torizon for Maivin 2026.08.0

### Topic names changed to hostname namespaces (EDGEAI-1396)

All stock services publish inside a Zenoh session namespace equal to the device hostname and no longer use the legacy `rt/` prefix.  The stock camera, model, IMU, and GPS paths are verified on the release image, however any client application still subscribing to `rt/...` topics will not receive data.  The [Replay service](../../perception/data_collection/replay.md) and some of the [developer examples](../../perception/dev/index.md) were not completely verified against the new namespaces.

**Workaround:** subscribe to the bare topic name, for example `camera/h264`, from a Zenoh session configured with the device hostname as its namespace, or subscribe with a wildcard such as `**/camera/h264`.  Remove hard-coded `rt/` prefixes from your applications.  Use the current EdgeFirst Publisher and EdgeFirst Studio release when working with recordings.

### Web UI settings page gaps (EDGEAI-1229)

Some settings pages do not yet reflect every option supported by the services, notably the [Model Settings](../configuration/model.md) page which still shows options from the previous Model service.  Overlay state on the Camera page is not persisted across page refreshes and the GPS map has weak defaults.

**Workaround:** edit the corresponding `/etc/default/<service>` file over [SSH](../networking/ssh.md) and restart the service with `sudo systemctl restart <service>` when a setting cannot be changed from the Web UI.

### Configuration save may report success when nothing was written (EDGEAI-1402)

On earlier 2026.08 release candidates, saving a settings page only rewrote keys that were already present and uncommented in the configuration file.  Keys missing from the file or shipped commented out were silently skipped while the page reported a successful save.  The Web Server 4.2.0 and Web UI 4.4.0 included in 2026.08.0 rewrite the configuration atomically, add missing keys, and report the disposition of every key.

**Workaround:** if a saved setting does not take effect, uncomment or add the key in `/etc/default/<service>`, restart the service, and confirm the running configuration with `systemctl show -p Environment <service>` or the service log.

### Ethernet interfaces named end0 and end1 (EDGEAI-1424)

On lab units with a CPU serial number starting with `0`, the Ethernet interfaces may enumerate as `end0` and `end1` instead of `ethernet0` and `ethernet1`.  Customer units, whose serial numbers start with `1`, are not affected and no customer action is required.

### Some segmentation model configurations fail (EDGEAI-1221)

Some ModelPack and YOLO segmentation configurations fail to deploy on the Model service, including background class indexing issues, missing detections, and unsupported embedded configuration keys such as `protos` or `ultralytics`.

**Workaround:** use validated detection models such as the shipped Model Zoo YOLOv8n detector, and validate segmentation models on the device before deploying them in the field.

### Upload to Studio dialog limitations (EDGEAI-1407)

In the [Upload to EdgeFirst Studio](../../perception/data_collection/publishing.md#method-1-upload-from-the-web-ui) dialog the label controls are only available in Extended mode, the project selection can reset, the server may ignore the selected project, and identifiers are shown in decimal where EdgeFirst Studio shows hexadecimal.

**Workaround:** upload in Basic mode and complete the project and label binding in EdgeFirst Studio when [restoring the snapshot](../../studio/snapshots.md#restore-snapshot).

### Overlays can freeze the live camera view (EDGEAI-1445)

Enabling the detection box or segmentation mask overlays on the Camera page can freeze or stutter the live video, most noticeably with segmentation models.

**Workaround:** disable the overlays for live monitoring and review annotated output from recordings in Foxglove Studio or EdgeFirst Studio.

### Manual camera launch fails every other start (EDGEAI-1439)

Launching `edgefirst-camera` manually from the command line, rather than through `camera.service`, can fail with `Invalid argument` on every second start because the ISP media server only serves a single client per lifetime.  Repeated failures can wedge the capture pipeline until reboot.  The stock `camera.service` restarts the ISP before every start and is not affected.

**Workaround:** use `sudo systemctl restart camera` to restart the camera, or restart the ISP before a manual launch with `sudo systemctl restart imx8-isp` followed by `sudo edgefirst-camera ...`.  Reboot the device if the capture pipeline is wedged.

### 4K camera mode follow-ups (EDGEAI-1230, EDGEAI-1406)

The 1080p60 capture, recording, and streaming paths are verified for this release.  The `4k` camera mode with H.264 tiling has remaining issues with the `tf_static` frame mapping of the tiles and the tile stitching in Foxglove Studio which are deferred to a patch release.

**Workaround:** prefer the `1080p60` camera mode.  Do not rely on the 4K multi-tile Foxglove stitching until the patch release.

### IMU publishes near 140 Hz (EDGEAI-1468)

The `imu` topic publishes at roughly 140 Hz, above the previously documented 80 to 120 Hz band.  This is a warning only.

**Workaround:** downsample in the consumer when a strict rate is required.

### No 1080p30 camera mode (EDGEAI-1464)

The `CAMERA_MODE` setting supports `1080p60` and `4k` only.

**Workaround:** use `1080p60` and subsample frames in the consumer for 30 FPS workflows.

### Publisher frame sampling is slow (EDGEAI-1469)

Exporting a recording with the publisher at a sampled frame rate, for example `-f 1`, produces the correct output but decodes every H.264 frame in the recording.  A 66 second 60 FPS recording can take seven to eight minutes to export on the device.

**Workaround:** run long exports inside a `tmux` or `screen` session so the export survives a dropped SSH connection.

### Publisher 4K tile stitching runs out of memory (EDGEAI-1470)

Stitching 4K tiled recordings of about 60 seconds or longer can exhaust the device memory.  1080p exports are not affected.

**Workaround:** record short clips of about 8 seconds when using the tile topics, stop the `camera` and `model` services before running the publisher to free memory, and prefer the `1080p60` camera mode for HD capture.

### Replay service not verified on 2026.08.0

The Replay service included in this release predates the hostname namespace and EdgeFirst Schemas 4.0 migration of the other services.  It re-adds the `rt/` prefix when republishing recorded topics and still publishes the removed `DmaBuffer` type for camera frames, so replayed camera frames are not consumed by the Model service.  Radar, LiDAR, and fusion replay were not verified for this release.

**Workaround:** review recordings in [Foxglove Studio](../../perception/data_collection/foxglove.md) or upload them to [EdgeFirst Studio](../../perception/data_collection/publishing.md).

## General

### "SSL peer certificate or SSH remote key was not OK" during `ostree pull`

If you update the `ethernet0` network interface without a reboot and try to run an `ostree pull` command, you may get the following error:

```text
error: While fetching https://maivin.deepviewml.com/ostree/summary.sig: [60] SSL peer certificate or SSH remote key was not OK
```

If so, reboot the system with the `sudo reboot` command.  This should address the issue.

### "No update available" after a Torizon OTA update or manual deploy

A Torizon OTA (aktualizr) update, or an `ostree admin deploy` invoked with a branch name missing the `maivin:` remote prefix, clears the channel from the deployment origin.  The device then reports `No update available` from `ostree admin upgrade` and never updates again.  Check the refspec with `ostree admin status` and repair it following the [Software Updates](updates.md#repairing-the-deployment-origin) page.
