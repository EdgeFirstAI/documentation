# Migration Guide

This guide covers upgrading datasets and code to schema version **2026.10**, the format written by EdgeFirst Client 2.15.0 and later. 2026.10 is an additive change on top of 2026.04; 2026.04 introduced the breaking changes from 2025.10.

| From | To | Breaking | Migration command |
|------|----|----------|-------------------|
| 2026.04 | 2026.10 | No | Optional — readers accept 2026.04 files as is |
| 2025.10 | 2026.10 | Yes | `edgefirst-client migrate` converts directly to 2026.10 |

## Upgrading from 2026.04 to 2026.10

### What Changed

| Area | 2026.04 | 2026.10 |
|------|---------|---------|
| Don't-care flag | `iscrowd: Boolean` (COCO crowd regions only) | `ignore: Boolean` — same COCO source, plus don't-care regions from other formats (for example VisDrone `ignored regions`) |
| Excluded objects | Not represented | `exclude: Boolean` — real objects outside the class set (for example VisDrone `others`) |
| `iscrowd` | Current | **Deprecated** — written as a mirror of `ignore` for compatibility |
| Attribute columns | Not represented | `truncation` and `occlusion` (`UInt32`), JSON `attributes` object |
| IMU `pose` | Order not consistent between tools | `[roll, pitch, yaw]` in signed degrees |

No existing column is removed or changes type. See [Annotation Schema](schema.md#annotation-metadata) for the column definitions.

### Migration Command

```bash
edgefirst-client migrate dataset.arrow [--output migrated.arrow]
```

`edgefirst-client migrate` upgrades a 2026.04 file to 2026.10:

1. Adds the `ignore` column from the deprecated `iscrowd` column when `ignore` is not already present, keeping `iscrowd` as a mirror
2. Leaves the Binary raster `mask` column and all other columns unchanged
3. Sets `schema_version = "2026.10"` in file metadata
4. Writes to `--output`, or overwrites the input file in place when `--output` is omitted

No `exclude` column is created — there is nothing in a 2026.04 file to derive it from. The command does not reorder `pose` or `location`; see [IMU Pose and GPS Location in Older Files](#imu-pose-and-gps-location-in-older-files).

### Readers Need Not Migrate

Files do not need to be migrated to be read. Readers prefer the `ignore` column but fall back to `iscrowd` (accepting either `Boolean` or the older integer type) when `ignore` is absent, so 2026.04 files continue to work with the current client without running `migrate`.

If your code reads `iscrowd` directly, switch it to `ignore` with the same fallback:

```python
import polars as pl

df = pl.read_ipc("dataset.arrow")

if "ignore" in df.columns:
    ignore = pl.col("ignore").fill_null(False)
elif "iscrowd" in df.columns:
    ignore = pl.col("iscrowd").cast(pl.Boolean).fill_null(False)
else:
    ignore = pl.lit(False)

annotations = df.filter(~ignore)
```

### IMU Pose and GPS Location in Older Files

Before 2026.10, the array order of the `pose` column was not consistent between the tools that write EdgeFirst datasets, and some EdgeFirst Publisher releases wrote `location` in the reverse order. The order cannot be detected from the file itself, so check which tool produced an older file:

| Writer | `pose` order | `pose` range | `location` order |
|--------|--------------|--------------|------------------|
| EdgeFirst Client 2.14 and earlier (`download-annotations`, `samples_dataframe`, Studio snapshots created through the client) | `[yaw, pitch, roll]` | Signed degrees | `[lat, lon]` |
| EdgeFirst Publisher 1.10 (Torizon for Maivin 2026.08) | `[roll, pitch, yaw]` | 0–360 degrees | `[lat, lon]` |
| EdgeFirst Publisher 1.9 and earlier | `[roll, pitch, yaw]` | 0–360 degrees | `[lon, lat]` |
| 2026.10 files (all writers) | `[roll, pitch, yaw]` | Signed degrees | `[lat, lon]` |

`edgefirst-client upload-dataset` (2.15.0 and later) reads `pose` as `[roll, pitch, yaw]` and `location` as `[lat, lon]` whatever the file's version, so correct an older file before uploading it. To bring an older file in line with 2026.10, swap roll and yaw for files from the client, convert the 0–360 range to signed degrees for files from the Publisher, and swap latitude and longitude for files from Publisher 1.9 and earlier:

```python
import polars as pl

df = pl.read_ipc("dataset.arrow")

pose = pl.col("pose")
location = pl.col("location")

def signed(angle: pl.Expr) -> pl.Expr:
    """Map an angle in 0..360 degrees to -180..180."""
    return (angle + 180.0) % 360.0 - 180.0

# EdgeFirst Client 2.14 and earlier: [yaw, pitch, roll] -> [roll, pitch, yaw]
df = df.with_columns(
    pl.when(pose.is_not_null())
    .then(pl.concat_list(pose.arr.get(2), pose.arr.get(1), pose.arr.get(0)).list.to_array(3))
    .alias("pose")
)

# EdgeFirst Publisher: 0..360 -> signed degrees (order is already [roll, pitch, yaw])
df = df.with_columns(
    pl.when(pose.is_not_null())
    .then(pl.concat_list(signed(pose.arr.get(0)), signed(pose.arr.get(1)), signed(pose.arr.get(2))).list.to_array(3))
    .alias("pose")
)

# EdgeFirst Publisher 1.9 and earlier: [lon, lat] -> [lat, lon]
df = df.with_columns(
    pl.when(location.is_not_null())
    .then(pl.concat_list(location.arr.get(1), location.arr.get(0)).list.to_array(2))
    .alias("location")
)
```

Apply only the steps that match the file's writer. Studio JSON and the Studio API use the named fields `{roll, pitch, yaw}` and `{lat, lon}` and are not affected.

## Upgrading from 2025.10

### What Changed

| Area | 2025.10 | 2026.04 and later | Impact |
|------|---------|-------------------|--------|
| Polygon storage | `mask: List<Float32>` with NaN separators | `polygon: List<List<Float32>>` nested lists | Column name and type changed |
| Mask type | `List<Float32>` (polygon data) | `Binary` (PNG-encoded raster pixels) | Column type changed; semantics changed |
| `label_index` semantics | Alphabetically re-indexed (0-based, contiguous) | Source-faithful `category_id` (non-contiguous, preserves gaps) | Existing files remain valid; new exports may differ |
| `iscrowd` type | `UInt8` (0/1) | `Boolean` (true/false), deprecated in 2026.10 in favor of `ignore` | Column type changed |
| New columns | N/A | `polygon_score`, `mask_score`, `box2d_score`, `box3d_score`, `timing`, `category_frequency`, `neg_label_indices`, `not_exhaustive_label_indices`, and in 2026.10 `ignore`, `exclude`, `truncation`, `occlusion` | Additive (non-breaking for readers that ignore unknown columns) |
| File metadata | None | `schema_version`, `category_metadata`, `labels` | Additive |
| JSON structure | Bare array `[...]` | Object wrapper `{"schema_version": ..., "samples": [...]}` | Readers must detect top-level type |
| LiDAR sensors | `.lidar.png`, `.lidar.jpeg` | **Removed** | Breaking for pipelines that depend on projected LiDAR images |
| Parquet support | N/A | `.parquet` files supported (client 2.14.0 and later) | New capability |

!!! danger "Old code will produce corrupt data"
    Code that reads the `mask` column as `List<Float32>` and splits on NaN values will fail or produce incorrect results when applied to 2026.04 and later files where `mask` is `Binary` (PNG-encoded raster data). Additionally, `iscrowd` changed from `UInt8` to `Boolean`. Always check the schema version before processing.

### Migration Command

```bash
edgefirst-client migrate dataset.arrow [--output migrated.arrow]
```

`edgefirst-client migrate` converts a 2025.10 Arrow file directly to 2026.10:

1. Reads the 2025.10 `mask: List<Float32>` column with NaN separators
2. Converts it to `polygon: List<List<Float32>>` (split on NaN, pair coordinates into rings)
3. Removes the old `mask` column (no raster data to migrate — it did not exist in 2025.10)
4. Converts an integer `iscrowd` column to `Boolean` and adds `ignore` from it
5. Sets `schema_version = "2026.10"` in file metadata
6. Writes to `--output`, or overwrites the input file in place when `--output` is omitted, and reports the number of polygon annotations converted

This is a **lossless conversion** for polygon data. Apart from `ignore`, no new columns are created: scores, timing, and LVIS fields are not added. Files already at 2026.10 are left unchanged.

## Version Detection

### Arrow / Parquet Files

Apply the rules in order; the first rule that matches wins:

| # | Signal | Interpretation |
|---|--------|----------------|
| 1 | `schema_version` metadata present | Use the stated version |
| 2 | `ignore` or `exclude` column present | 2026.10 |
| 3 | `polygon` column present, or `mask: Binary` | 2026.04 or later |
| 4 | `mask: List<Float32>`, or no geometry columns | 2025.10 |

A 2026.10 file with no flagged rows has no `ignore` or `exclude` column, because columns whose values are all null are dropped when a file is written. Rule 3 therefore cannot tell 2026.04 from 2026.10; rely on `schema_version`, which the EdgeFirst Client always writes.

### JSON Files

| Signal | Interpretation |
|--------|---------------|
| Top-level is a JSON array `[...]` | 2025.10 — bare array of samples |
| Top-level is a JSON object with `schema_version` | Use the stated version |

```python
import json

with open("annotations.json") as f:
    data = json.load(f)

if isinstance(data, list):
    # 2025.10 legacy
    samples = data
    version = "2025.10"
else:
    # 2026.04 and later
    samples = data["samples"]
    version = data.get("schema_version")
```

## Reading All Versions

```python
import polars as pl

def read_dataset(path: str):
    """Read an EdgeFirst dataset written in 2025.10, 2026.04, or 2026.10."""
    if path.endswith(".parquet"):
        df = pl.read_parquet(path)
    else:
        df = pl.read_ipc(path)

    if "polygon" in df.columns:
        return read_current(df)

    if "mask" in df.columns:
        mask_dtype = str(df["mask"].dtype)
        if mask_dtype.startswith("List(Float32"):
            return read_2025_10(df)
        elif mask_dtype == "Binary":
            return read_current(df)

    # No geometry columns — compatible with every version
    return read_current(df)


def read_2025_10(df: pl.DataFrame):
    """Handle 2025.10 NaN-separated polygon data in the mask column."""
    # Convert mask: List<f32> (NaN-separated) -> polygon: List<List<f32>>
    # This is what `edgefirst-client migrate` does
    print("2025.10 format detected — consider running: edgefirst-client migrate")
    return df


def read_current(df: pl.DataFrame):
    """Handle 2026.04 and 2026.10 files."""
    # polygon: List<List<f32>> — interleaved xy pairs per ring
    # mask: Binary — PNG-encoded raster pixels
    # ignore: prefer it, fall back to the deprecated iscrowd column
    if "ignore" not in df.columns and "iscrowd" in df.columns:
        df = df.with_columns(pl.col("iscrowd").cast(pl.Boolean).alias("ignore"))
    return df
```

## Code Migration Checklist

### If you read the `mask` column directly

```python
# OLD (2025.10) — WILL BREAK on 2026.04 and later files
mask_data = row["mask"]  # List<f32> with NaN separators
rings = split_on_nan(mask_data)

# NEW (2026.04 and later)
polygon_data = row["polygon"]  # List<List<f32>>, already split into rings
for ring in polygon_data:
    points = list(zip(ring[0::2], ring[1::2]))
```

### If you read `iscrowd`

```python
# OLD (2026.04)
is_crowd = row["iscrowd"]

# NEW (2026.10) — iscrowd is a deprecated mirror of ignore
is_dont_care = row["ignore"] if "ignore" in row else row.get("iscrowd")
is_excluded = row.get("exclude")
```

### If you read the `pose` column

```python
# 2026.10 — always [roll, pitch, yaw] in signed degrees
roll, pitch, yaw = row["pose"]
```

For older files, see [IMU Pose and GPS Location in Older Files](#imu-pose-and-gps-location-in-older-files).

### If you process LiDAR visualizations

```python
# OLD (2025.10) — projected LiDAR images
depth_image = load("frame_001.lidar.png")
reflect_image = load("frame_001.lidar.jpeg")

# NEW (2026.04 and later) — project from PCD yourself
pcd = load("frame_001.lidar.pcd")
depth_image = project_to_depth(pcd, calibration)
```

## FAQ

**Q: Which EdgeFirst Client versions read and write each schema?**

| Client version | Writes | Reads |
|----------------|--------|-------|
| 2.15.0 and later | 2026.10 (Arrow IPC or Parquet) | 2025.10, 2026.04, 2026.10 |
| 2.14.x | 2026.04 (Arrow IPC or Parquet) | 2025.10, 2026.04 |
| 2.9.0 – 2.13.x | 2026.04 (Arrow IPC) | 2025.10, 2026.04 |

**Q: Do I need to migrate all my datasets at once?**

No. The EdgeFirst Client reads 2025.10, 2026.04, and 2026.10 files transparently. Migrate when convenient — there is no deadline.

**Q: What happens to raster mask data during migration?**

Raster masks (`Binary`, PNG-encoded) are a **new** capability in 2026.04. The 2025.10 `mask` column contained polygon data (NaN-separated `List<Float32>`), not raster data. Migration moves polygon data to the new `polygon` column and removes the old `mask` column. There is no raster data to lose.

**Q: Can polygon and mask coexist in the same file?**

Yes. A file can have both `polygon` (vector contours) and `mask` (raster pixels) columns populated. This supports use cases like panoptic segmentation where instance polygons and semantic raster masks are both needed.

**Q: How do I tell if a JSON file is 2025.10 or later?**

Check the top-level structure. 2025.10 JSON files are a bare array `[...]`. Later files are an object `{"schema_version": "2026.10", "samples": [...]}`.

**Q: My `label_index` values changed after re-importing a dataset. Is that expected?**

Yes, if you are importing a file that was created with the 2025.10 SDK. The 2025.10 SDK assigned `label_index` values using alphabetical ordering of category names (0-based, contiguous). Since 2026.04 the SDK preserves the original source `category_id` as `label_index` (non-contiguous, may not start at 0). Both are valid; the current behavior is correct for round-trip fidelity with COCO and LVIS datasets.

**Q: Does the COCO importer support LVIS annotations?**

Yes. The COCO importer handles LVIS extensions automatically. LVIS-specific fields (`neg_category_ids`, `not_exhaustive_category_ids`, category `frequency`/`synset`/`synonyms`/`def`) are parsed when present and mapped to the corresponding EdgeFirst columns and file-level metadata. No separate LVIS mode is needed.

**Q: What are `neg_label_indices` and `not_exhaustive_label_indices`?**

These are LVIS-specific sample-level columns that support the LVIS federated annotation evaluation protocol. `neg_label_indices` lists categories confirmed absent from an image (valid false positives). `not_exhaustive_label_indices` lists categories with potentially incomplete annotation (unmatched predictions are ignored). Both reference `label_index` values. They are optional and absent from non-LVIS datasets.

**Q: Why are my crowd annotations missing after uploading to EdgeFirst Studio?**

Studio does not store the `ignore` and `exclude` flags yet. Uploads drop annotations flagged `ignore` or `exclude`, including COCO crowd annotations, and log one warning with the number skipped. Keep the Arrow or Parquet file as the source of truth for these annotations.
