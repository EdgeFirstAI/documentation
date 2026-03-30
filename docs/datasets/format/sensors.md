# Sensor Data

Sensor data is always stored **external** to the annotation file. Arrow, Parquet, and
JSON files contain annotations only — sensor data lives in sibling folders or
ZIP files.

## Sensor Types

| Sensor | Extension | Notes |
|--------|-----------|-------|
| Camera | `.camera.jpeg`, `.camera.png` | JPEG (default) or PNG (lossless) |
| Radar cube | `.radar.png` | 16-bit PNG encoding of complex int16 data |
| Radar PCD | `.radar.pcd` | Point cloud data |
| LiDAR PCD | `.lidar.pcd` | Point cloud data |

!!! warning "Removed in 2026.04"
    The `.lidar.png` (depth map) and `.lidar.jpeg` (reflectivity) projected visualization
    formats have been **removed** from the format specification in 2026.04.
    The SDK retains read support for backward compatibility but will not write these types.
    Consumers that need depth or reflectivity images should project LiDAR PCD data directly.

<<<<<<< HEAD
1. **Recording**: [Raivin or Maivin devices](../../perception/data_collection/recording.md) record sensor data as ROS2 topics into MCAP files
2. **Upload**: MCAP files are [uploaded as snapshots](../../perception/data_collection/publishing.md) to EdgeFirst Studio  
3. **Restore**: Snapshots are [restored into datasets](../../studio/snapshots.md#restore-snapshot), converting MCAP topics to discrete sensor files
4. **Create Snapshot**: Datasets can be [exported as snapshots](../../studio/snapshots.md#create-snapshot) for download
5. **Download**: Snapshots are downloaded as ZIP + Arrow file pairs in the [EdgeFirst Dataset Format](index.md)
=======
## Camera
>>>>>>> test

**Format**: JPEG (default) or PNG (lossless)

**Source**: H.265 video from MCAP converted to discrete frames

**EXIF metadata** (embedded in images):

- GPS coordinates (from MCAP `/gps` topic or NavSat)
- Capture timestamp
- Camera parameters
- Device information

**File extensions**:

- `.camera.jpeg` — camera image (default)
- `.camera.png` — camera image (lossless)
- `.jpg`, `.png` — generic image formats

## Radar

### Point Cloud Data

**Format**: PCD (Point Cloud Data)

**Extension**: `.radar.pcd`

**Fields**:

```
x, y, z          # Cartesian position (meters)
speed            # Velocity (m/s)
power            # Signal power
noise            # Noise level
rcs              # Radar cross-section
```

### Radar Data Cube

**Format**: 16-bit PNG (lossless encoding of complex int16 data)

**Extension**: `.radar.png`

**Dimensions**: `[sequence, rx_antenna, range_bins, doppler_bins]`

**Typical shape**: `[2, 4, 200, 256]`

**PNG encoding**:

- 4 x 2 grid layout (4 columns = RX antennas, 2 rows = sequences)
- Complex int16 split into pair of int16 values (PNG does not support complex)
- **int16 shifted to uint16** for PNG storage (shift back to int16 for processing)
- Double-width matrices (complex pairs)
- **Output size**: 2048 x 400 pixels for standard cube

## LiDAR

**Format**: PCD (Point Cloud Data)

**Extension**: `.lidar.pcd`

**Configuration**: Based on Maivin MCAP Recorder settings.

!!! note "Projected visualizations removed"
    Prior versions of EdgeFirst supported `.lidar.png` (depth map) and `.lidar.jpeg`
    (reflectivity) files that contained 2D projections of LiDAR point cloud data.
    These have been removed in 2026.04. If your pipeline requires depth or reflectivity
    images, project the PCD data using the LiDAR sensor calibration parameters.
