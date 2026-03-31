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

## Camera

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

<<<<<<< HEAD
```text
{sequence_name}_{frame_number}.lidar.pcd
```

### Visualizations

**Depth Map** (`.lidar.png`):

- Visualization of depth from LiDAR returns
- Used for analysis and debugging

**Reflectivity** (`.lidar.jpeg`):

- Intensity/reflectivity visualization
- Shows how reflective each point is

**File naming**:

```text
{sequence_name}_{frame_number}.lidar.png       # depth map
{sequence_name}_{frame_number}.lidar.jpeg      # reflectivity
```

---

## Depth Data (Optional)

Some datasets include depth estimation from camera frames:

**File format**: `.depth.png` (16-bit depth map)

**File naming**:

```text
{sequence_name}_{frame_number}.depth.png
```

**Use case**:

- Pseudo-3D from monocular depth estimation
- Training or evaluating depth models

---

## File Organization Example

Here's a complete example showing all possible sensor types:

```text
my_dataset/
├── my_dataset.arrow
└── my_dataset/
    └── system_2025_01_15_143022/
        ├── system_2025_01_15_143022_001.camera.jpeg
        ├── system_2025_01_15_143022_001.camera.png         (if lossless)
        ├── system_2025_01_15_143022_001.radar.pcd
        ├── system_2025_01_15_143022_001.radar.png
        ├── system_2025_01_15_143022_001.lidar.pcd
        ├── system_2025_01_15_143022_001.lidar.png
        ├── system_2025_01_15_143022_001.lidar.jpeg
        ├── system_2025_01_15_143022_001.depth.png
        ├── system_2025_01_15_143022_002.camera.jpeg
        ├── system_2025_01_15_143022_002.radar.pcd
        ├── system_2025_01_15_143022_002.radar.png
        └── ... (more frames)
```

## Sensor Data Alignment

All sensor data for a given frame is aligned temporally:

```text
system_2025_01_15_143022_042
├── .camera.jpeg     ← Captured at T=42
├── .radar.pcd       ← Measured at T=42
├── .radar.png       ← Measured at T=42
└── .lidar.pcd       ← Measured at T=42
```

This means:

- Same frame number across sensors = captured at same moment
- No temporal skew between modalities
- Safe for multi-sensor fusion and training

## Accessing Sensor Data

Once you have your dataset, you can access sensor files:

```python
import os
from pathlib import Path

dataset_root = Path("my_dataset")
sensor_dir = dataset_root / "my_dataset"

# List all camera images
camera_files = sorted(sensor_dir.glob("**/*.camera.jpeg"))
print(f"Found {len(camera_files)} camera frames")

# List all radar files
radar_pcd_files = sorted(sensor_dir.glob("**/*.radar.pcd"))
radar_cube_files = sorted(sensor_dir.glob("**/*.radar.png"))
print(f"Found {len(radar_pcd_files)} radar point clouds")
print(f"Found {len(radar_cube_files)} radar data cubes")

# Group by sequence
from collections import defaultdict
sequences = defaultdict(list)
for file in camera_files:
    seq_name = file.stem.rsplit('_', 1)[0]
    sequences[seq_name].append(file)

for seq, files in sequences.items():
    print(f"Sequence '{seq}': {len(files)} frames")
```

## Best Practices

- **Verify alignment**: Ensure matching frame numbers exist for all sensors
- **Check completeness**: Not all frames need all sensors (e.g., LiDAR might be optional)
- **Test loading**: Try loading a few files before processing entire dataset
- **Handle missing data**: Some frames may lack optional sensors (depth, reflectivity)

## Further Reading

- [Dataset Organization](structure.md) — How sensor files are organized on disk
- [Annotation Schema](schema.md) — Metadata extracted from EXIF and sensors
- [Platform Recording](../../perception/data_collection/recording.md) — How sensor data is recorded on Raivin/Maivin
- [Publishing Workflows](../../perception/data_collection/publishing.md) — How to upload MCAP recordings as snapshots
- [Snapshots Dashboard](../../studio/snapshots.md) — How to download and restore snapshots
=======
!!! note "Projected visualizations removed"
    Prior versions of EdgeFirst supported `.lidar.png` (depth map) and `.lidar.jpeg`
    (reflectivity) files that contained 2D projections of LiDAR point cloud data.
    These have been removed in 2026.04. If your pipeline requires depth or reflectivity
    images, project the PCD data using the LiDAR sensor calibration parameters.
>>>>>>> test
