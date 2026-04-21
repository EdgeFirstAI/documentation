# LiDAR Settings (Raivin-only)

This page configures the LiDAR publishing service that interacts with the Raivin's integrated [Ouster OS1-64 LiDAR sensor][ouster]. The configuration allows for fine-tuning of the LiDAR sensor's operation and data processing.

{{ figure("../assets/configuration/configuration-lidar.png", "LiDAR Settings page") }}

!!! tip
    These values are stored in the `/etc/default/lidarpub` file on the device and can be hand-edited.  This is not recommended.

### Log Level

Log level for the application, relevant sub-filters are 'lidarpub' and 'ouster'. Refer to [RUST_LOG documentation][rustlog] for details. Options are 'info', 'debug', 'warn', and 'error'.

### Zenoh Wait Before Drop (μs)

Microsecond timeout before dropping a Zenoh message. The default value of 100000 (100ms) is optimized for 10Hz operation. This setting helps manage message queuing and prevents buffer overflow.

### Target Device

Hostname or IP address of the LiDAR target device. This should match the static IP address configured in Ouster Studio. The default value is typically set to `10.10.41.216`.

### LiDAR Mode

Configures the LiDAR's column resolution and refresh rate. The format is `columnsxrate`, where:  

- **Columns**: Number of points per rotation (1024, 2048)  
- **Rate**: Refresh rate in Hz (10, 20)  

For example, `1024x20` means 1024 points per rotation at 20Hz refresh rate.

### Timestamp Mode

Controls how the LiDAR configures its clock. Options are:  

- **Internal**: Uses the LiDAR's internal clock  
- **PTP**: Uses Precision Time Protocol for synchronization  
- **NTP**: Uses Network Time Protocol for synchronization  

### Transform Vector

Defines the LiDAR frame transformation vector (X Y Z) from the base_link frame. This is used to properly position the LiDAR data in the vehicle's coordinate system. The default value is typically `0 0 -0.19` meters.

### Rotation Quaternion

Defines the LiDAR frame rotation quaternion (X Y Z W) from the base_link frame. This is used to properly orient the LiDAR data in the vehicle's coordinate system. The default value is typically `0 0 -0.9998157 0.0191974`.

### Field of View Settings

The LiDAR sensor has the following field of view characteristics:  

- **Horizontal Coverage**: 140° (configurable)  
- **Minimum Azimuth**: 110° (configurable)  
- **Maximum Azimuth**: 250° (configurable)  
- **Vertical Field of View**: 45° (+22.5° to -22.5°)  

These settings can be adjusted to focus the LiDAR's attention on specific areas of interest while reducing computational load.

### Additional Settings

The LiDAR configuration also includes:  

- **Camera Field of View**: 84° (for reference)  
- **Radar Field of View**: 140° (for reference)  
- **Full 360° Coverage**: Available when needed  
- **Minimum Range**: 0.3m  
- **Maximum Range**: 100m (at 80% reflectivity)  

[rustlog]: https://docs.rs/env_logger/latest/env_logger/#enabling-logging
[ouster]: https://ouster.com/products/os1-lidar-sensor/
