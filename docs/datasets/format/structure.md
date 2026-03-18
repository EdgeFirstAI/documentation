# Directory Structure

EdgeFirst datasets follow a consistent directory layout where the annotation file and
the sensor data container share the same base name.

## File Naming

Annotation files use the dataset base name with the format extension:

```
dataset_name/
├── dataset_name.arrow          # Arrow IPC (default)
├── dataset_name.parquet        # Parquet (transfer)
├── dataset_name.json           # JSON (human-readable)
└── dataset_name/               # Sensor container (directory or .zip)
```

Only **one annotation file** per dataset. The sensor container directory name matches
the dataset base name regardless of annotation file format.

## Dataset Layouts

EdgeFirst supports three organizational patterns.

### 1. Sequence-Based Datasets

Video frames with temporal ordering (from MCAP recordings or video files):

```
deer_dataset/
├── deer_dataset.arrow
└── deer_dataset/
    └── 9331381uhd_3840_2160_24fps/
        ├── 9331381uhd_3840_2160_24fps_110.camera.jpeg
        ├── 9331381uhd_3840_2160_24fps_111.camera.jpeg
        └── ...
```

**File naming convention**:

- Sequence format: `{hostname}_{date}_{time}` (from MCAP)
- Frame format: `{sequence_name}_{frame_number}.{sensor}.{ext}`

### 2. Image-Based Datasets

Standalone images without temporal ordering:

```
coco_subset/
├── coco_subset.arrow
└── coco_subset/
    ├── image001.jpg
    ├── image002.jpg
    └── ...
```

### 3. Mixed Datasets

Combination of sequences and standalone images:

```
mixed_dataset/
├── mixed_dataset.arrow
└── mixed_dataset/
    ├── sequence_A/
    │   ├── sequence_A_001.camera.jpeg
    │   └── sequence_A_002.camera.jpeg
    ├── standalone_image1.jpg
    └── standalone_image2.jpg
```

## Multi-Sensor Examples

A single frame can include multiple sensor modalities:

```
sensor_fusion/
├── sensor_fusion.parquet
└── sensor_fusion/
    └── drive_2026_03_18/
        ├── drive_2026_03_18_001.camera.jpeg
        ├── drive_2026_03_18_001.radar.png
        ├── drive_2026_03_18_001.radar.pcd
        ├── drive_2026_03_18_001.lidar.pcd
        ├── drive_2026_03_18_002.camera.jpeg
        ├── drive_2026_03_18_002.radar.png
        └── ...
```

## Flattened Structure

As an alternative to nested subdirectories, datasets may use a flat layout with
sequence prefixes:

```
dataset_name/
├── dataset_name.arrow
└── dataset_name/
    ├── sequence_A_001.camera.jpeg
    ├── sequence_A_002.camera.jpeg
    ├── sequence_B_001.camera.jpeg
    └── standalone_image.jpg
```

The EdgeFirst Client SDK detects the layout automatically — no manual configuration is needed.

## ZIP Format

EdgeFirst supports ZIP64 as an alternative to directories for the sensor container:

```
dataset_name/
├── dataset_name.arrow
└── dataset_name.zip             # sensor data in ZIP
```

ZIP64 provides:

- Random access via file index
- Uncompressed storage (sensor files are already compressed — JPEG, PCD, etc.)
- Cross-platform support

## Sensor File Extensions

| Extension | Sensor | Description |
|-----------|--------|-------------|
| `.camera.jpeg` | Camera | Camera image (default) |
| `.camera.png` | Camera | Camera image (lossless) |
| `.jpg`, `.png` | Camera | Generic image formats |
| `.radar.pcd` | Radar | Radar point cloud |
| `.radar.png` | Radar | Radar data cube (16-bit PNG) |
| `.lidar.pcd` | LiDAR | LiDAR point cloud |
