# Upgrading from 2025.10 to 2026.04

This guide covers the breaking changes introduced in schema version 2026.04 and how
to migrate existing datasets and code.

## What Changed

| Area | 2025.10 | 2026.04 | Impact |
|------|---------|---------|--------|
| Polygon storage | `mask: List<Float32>` with NaN separators | `polygon: List<List<Float32>>` nested lists | Column name and type changed |
| Mask type | `List<Float32>` (polygon data) | `List<UInt8>` (raster pixel data) | Column type changed; semantics changed |
| New columns | N/A | `polygon_score`, `mask_score`, `box2d_score`, `box3d_score`, `timing` | Additive (non-breaking for readers that ignore unknown columns) |
| File metadata | None | `schema_version`, `box2d_format`, `box2d_normalized`, etc. | Additive |
| JSON structure | Bare array `[...]` | Object wrapper `{"schema_version": ..., "samples": [...]}` | Readers must detect top-level type |
| LiDAR sensors | `.lidar.png`, `.lidar.jpeg` | **Removed** | Breaking for pipelines that depend on projected LiDAR images |
| Parquet support | N/A | `.parquet` files supported | New capability |

!!! danger "Old code will produce corrupt data"
    Code that reads the `mask` column as `List<Float32>` and splits on NaN values
    will fail or produce incorrect results when applied to 2026.04 files where `mask`
    is `List<UInt8>` raster data. Always check the schema version before processing.

## Migration Command

The EdgeFirst Client SDK provides a migration utility:

```bash
edgefirst migrate <input.arrow> [--output <output.arrow>]
```

The migration utility performs these steps:

1. Reads the 2025.10 `mask: List<Float32>` column with NaN separators
2. Converts to `polygon: List<List<Float32>>` (split on NaN, pair coordinates)
3. Removes the old `mask` column (no raster data to migrate — it did not exist in 2025.10)
4. Sets `schema_version = "2026.04"` in file metadata
5. Writes the new file (preserving all other columns unchanged)

This is a **lossless conversion** for polygon data. Raster masks are a new capability
with no migration path (they did not exist in 2025.10).

## Version Detection

### Arrow / Parquet Files

| Signal | Interpretation |
|--------|---------------|
| `schema_version` metadata = `"2026.04"` | 2026.04 format |
| `schema_version` absent + `mask: List<Float32>` | 2025.10 — NaN-separated polygon data in `mask` |
| `schema_version` absent + no `mask` / no `polygon` | 2025.10 — no geometry |
| `schema_version` absent + `mask: List<UInt8>` | 2026.04 — type is unambiguous |
| `polygon` column present | 2026.04 |

**Robustness rule**: If the physical type of the `mask` column is `List<UInt8>`, treat
as 2026.04 regardless of `schema_version` presence. The column type itself is unambiguous.

### JSON Files

| Signal | Interpretation |
|--------|---------------|
| Top-level is a JSON array `[...]` | 2025.10 — bare array of samples |
| Top-level is a JSON object with `schema_version` | 2026.04 — metadata wrapper |

```python
import json

with open("annotations.json") as f:
    data = json.load(f)

if isinstance(data, list):
    # 2025.10 legacy
    samples = data
else:
    # 2026.04
    samples = data["samples"]
    version = data.get("schema_version")
```

## Reading Both Versions

```python
import polars as pl

def read_dataset(path: str):
    """Read an EdgeFirst dataset, handling both 2025.10 and 2026.04."""
    if path.endswith(".parquet"):
        df = pl.read_parquet(path)
    else:
        df = pl.read_ipc(path)

    # Detect version
    if "polygon" in df.columns:
        return read_2026_04(df)

    if "mask" in df.columns:
        mask_dtype = str(df["mask"].dtype)
        if mask_dtype.startswith("List(Float32"):
            return read_2025_10(df)
        elif mask_dtype.startswith("List(UInt8"):
            return read_2026_04(df)

    # No geometry columns — compatible with either version
    return df


def read_2025_10(df: pl.DataFrame):
    """Handle 2025.10 NaN-separated polygon data in the mask column."""
    # Convert mask: List<f32> (NaN-separated) -> polygon: List<List<f32>>
    # This is what `edgefirst migrate` does
    print("2025.10 format detected — consider running: edgefirst migrate")
    return df


def read_2026_04(df: pl.DataFrame):
    """Handle 2026.04 format with polygon and raster mask columns."""
    # polygon: List<List<f32>> — interleaved xy pairs per ring
    # mask: List<UInt8> — row-major raster pixels (requires size column)
    return df
```

## Code Migration Checklist

### If you read the `mask` column directly

```python
# OLD (2025.10) — WILL BREAK on 2026.04 files
mask_data = row["mask"]  # List<f32> with NaN separators
rings = split_on_nan(mask_data)

# NEW (2026.04)
polygon_data = row["polygon"]  # List<List<f32>>, already split into rings
for ring in polygon_data:
    points = list(zip(ring[0::2], ring[1::2]))
```

### If you check `box2d_format`

```python
# OLD (2025.10) — assumed cxcywh for Arrow, ltwh for JSON
cx, cy, w, h = row["box2d"]

# NEW (2026.04) — check metadata
# box2d_format metadata describes the layout; default is still cxcywh for Arrow
cx, cy, w, h = row["box2d"]  # same default, but verify via metadata
```

### If you process LiDAR visualizations

```python
# OLD (2025.10) — projected LiDAR images
depth_image = load("frame_001.lidar.png")
reflect_image = load("frame_001.lidar.jpeg")

# NEW (2026.04) — project from PCD yourself
pcd = load("frame_001.lidar.pcd")
depth_image = project_to_depth(pcd, calibration)
```

## FAQ

**Q: Can I read 2026.04 files with old SDK versions?**

No. SDK versions prior to 3.0 do not understand the `polygon` column or the `List<UInt8>`
mask type. Update the EdgeFirst Client SDK to version 3.0 or later.

**Q: Do I need to migrate all my datasets at once?**

No. The EdgeFirst Client SDK 3.0+ reads both 2025.10 and 2026.04 files transparently.
Migrate when convenient — there is no deadline.

**Q: What happens to raster mask data during migration?**

Raster masks (`List<UInt8>`) are a **new** capability in 2026.04. The 2025.10 `mask`
column contained polygon data (NaN-separated `List<Float32>`), not raster data. Migration
moves polygon data to the new `polygon` column and removes the old `mask` column. There
is no raster data to lose.

**Q: Can polygon and mask coexist in the same file?**

Yes. A 2026.04 file can have both `polygon` (vector contours) and `mask` (raster pixels)
columns populated. This supports use cases like panoptic segmentation where instance
polygons and semantic raster masks are both needed.

**Q: How do I tell if a JSON file is 2025.10 or 2026.04?**

Check the top-level structure. 2025.10 JSON files are a bare array `[...]`. 2026.04
files are an object `{"schema_version": "2026.04", "samples": [...]}`.
