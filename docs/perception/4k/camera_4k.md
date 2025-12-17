# The 4K Camera Service
The Camera service on the Maivin/Raivin supports 4K video in multiple fashions, including command-line configuration, adding the parameters to the camera configuration file, as well as through the WebUI.

## Command Line Configuration
The camera service can be run at the platform's command-line interface. The first step would be to log on to the platform via [SSH](../../platforms/ssh.md). Then stop the current camera service with the `sudo systemctl stop camera`. The following command-line options for the camera service are described below.

```bash
# Enable 4K tile streaming
--h264-tiles

# Configure tile topics (default: rt/camera/h264/tl tr bl br)
--h264-tiles-topics "rt/camera/h264/tl rt/camera/h264/tr rt/camera/h264/bl rt/camera/h264/br"

# Set tile frame rate (default: 15 FPS)
--h264-tiles-fps 15

# Set H.264 bitrate
--h264-bitrate auto|mbps5|mbps25|mbps50|mbps100

# Camera resolution (should be 4K for tiles)
--camera-size 3840 2160

# How to Run
sudo camera --h264-tiles --h264-tiles-fps 30 --camera-size 3840 2160
```

You can also export these as environment variables prior to running the executable.

```bash
export H264_TILES=true
export H264_TILES_FPS=15
export TRACY=true
export H264_BITRATE=auto
export CAMERA_SIZE="3840 2160"
```
The H264 tile topics environment variable is not available at this time.

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
  --h264-tiles-topics rt/camera/tl rt/camera/tr rt/camera/bl rt/camera/br \
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
You can add the above parameters to the camera configuration file located at `/etc/default/camera`. The following lines can be added to the configuration file:
```
H264_TILES = "true"
H264_TILES_FPS = "15"
TRACY = "true"
```
The parameters for `CAMERA_SIZE` and `H264_BITRATE` already exist in `/etc/default/camera`. The H264 tile topics parameter is not available at this time.

## WebUI Configuration
There is no configuration item in the WebUI to specifically enable 4K tiling; however, you can set the [Camera Size](../../platforms/configuration/camera.md#camera-size) to `3840 2160` to implicitly enter 4K tiling. As well, you can set the [H264 Bitrate](../../platforms/configuration/camera.md#h264-bitrate) here as well. Lastly, it is recommended that you [disable H264 streaming](../../platforms/configuration/camera.md#h264-streaming) to disable the 1K video stream `/camera/h264`.

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

### Channel Full Errors
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