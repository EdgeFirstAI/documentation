# The 4K Camera Service

The Camera service on the Maivin/Raivin supports 4K video in multiple fashions, including command-line configuration, adding the parameters to the camera configuration file, as well as through the Web UI.

!!! note "Camera Mode"

    On the Maivin and Raivin the sensor readout is selected by the `CAMERA_MODE` setting of `/etc/default/camera` and applied by the ISP before the camera service starts.  Set `CAMERA_MODE="4k"` for 4K capture, the default `1080p60` mode does not provide a 4K readout and the ISP does not upscale.  Refer to the [Camera Settings](../../platforms/configuration/camera.md#camera-mode).

## Command Line Configuration

The camera service can be run at the platform's command-line interface. The first step would be to log on to the platform via [SSH](../../platforms/networking/ssh.md). Then stop the current camera service with `sudo systemctl stop camera` and restart the ISP with `sudo systemctl restart imx8-isp` so the camera service is its first client, refer to the [Known Issues](../../platforms/software/issues.md#manual-camera-launch-fails-every-other-start-edgeai-1439). The following command-line options for the camera service are described below.

```bash
# Enable 4K tile streaming
--h264-tiles

# Configure tile topics (default: camera/h264/tl tr bl br)
--h264-tiles-topics "camera/h264/tl camera/h264/tr camera/h264/bl camera/h264/br"

# Set tile frame rate (default: 15 FPS, 0 for no limit)
--h264-tiles-fps 15

# Set H.264 bitrate
--h264-bitrate auto|mbps5|mbps25|mbps50|mbps100

# Camera resolution (should be 4K for tiles)
--camera-size 3840 2160

# How to Run
sudo camera --h264-tiles --h264-tiles-fps 30 --camera-size 3840 2160
```

You can also export these as environment variables prior to running the executable.  Every command-line option has an environment variable of the same name in upper-case.

```bash
export H264_TILES=true
export H264_TILES_FPS=15
export H264_TILES_TOPICS="camera/h264/tl camera/h264/tr camera/h264/bl camera/h264/br"
export TRACY=true
export H264_BITRATE=auto
export CAMERA_SIZE="3840 2160"
```

### Usage Examples

#### Basic 4K Tile Streaming

```bash
sudo camera \
  --h264-tiles \
  --camera-size 3840 2160 \
  --h264-bitrate mbps25 \
  --h264-tiles-fps 15
```

#### Custom Topic Configuration

```bash
sudo camera \
  --h264-tiles \
  --h264-tiles-topics "camera/tl camera/tr camera/bl camera/br" \
  --camera-size 3840 2160
```

#### High Performance Setup

```bash
sudo camera \
  --h264-tiles \
  --h264-bitrate mbps50 \
  --h264-tiles-fps 30 \
  --camera-size 3840 2160 \
  --tracy  # Enable profiling
```

## SystemD Configuration file

You can set the above parameters in the camera configuration file located at `/etc/default/camera`, every key is present in the shipped file.  Set the following keys and restart the service with `sudo systemctl restart camera`:

```ini
CAMERA_MODE="4k"
CAMERA_SIZE="3840 2160"
H264_TILES="true"
H264_TILES_FPS="15"
H264_TILES_TOPICS="camera/h264/tl camera/h264/tr camera/h264/bl camera/h264/br"
```

The `H264_BITRATE` and `TRACY` parameters are also available in `/etc/default/camera`.  Refer to the [Camera Settings](../../platforms/configuration/camera.md#h264-4k-tiling) page for the complete list.

## Web UI Configuration

There is no configuration item in the Web UI to specifically enable 4K tiling or select the camera mode.  You can set the [Camera Size](../../platforms/configuration/camera.md#camera-size) to `3840 2160` and the [H264 Bitrate](../../platforms/configuration/camera.md#h264-bitrate) from the Camera Settings page, the `CAMERA_MODE` and `H264_TILES` keys must be set in the configuration file.  Once tiling is enabled the four tile topics replace the single `camera/h264` stream.

## Troubleshooting

### Low FPS Warnings

- Check camera resolution settings  
- Verify hardware encoding support  
- Monitor system resources  
- Turn off Radar Publishing and Fusion services if running and unneeded

### Encoding Failures

- Ensure 4K camera resolution is set  
- Check bitrate settings  
- Verify G2D hardware support  

### Dropped Frames

The service log reports `dropped N of M frames (encoder channels full)` every 10 seconds along with the count per tile when the encoders cannot keep up.

- Reduce tile FPS if encoding is slow  
- Increase system performance  
- Check for memory issues  

## Performance Tuning

### Bitrate Selection

- `auto`: Let encoder decide (recommended)
- `mbps5`: Low quality, low bandwidth
- `mbps25`: Good balance for most use cases
- `mbps50`: High quality, requires more bandwidth
- `mbps100`: Very high quality, but requires tremendous bandwidth

### Frame Rate Optimization

- Lower tile FPS reduces CPU usage
- Higher tile FPS improves smoothness
- Balance based on application requirements

### System Resources

- Monitor CPU usage across all threads
- Ensure sufficient memory for buffers
- Check hardware encoding availability
