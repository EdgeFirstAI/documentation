# Conversion Guidelines

!!! danger "2025.10 code is incompatible with 2026.04 files"
    Code written for the 2025.10 schema (NaN-separated masks, `mask: List<Float32>`)
    will produce **corrupt data** when applied to 2026.04 files. Always check the
    schema version before processing. See the [Migration Guide](migration.md) for
    upgrade instructions.

## Version Detection

Always detect the schema version before reading annotation data.

### Arrow / Parquet Files

```python
import polars as pl

df = pl.read_ipc("dataset.arrow")   # or pl.read_parquet("dataset.parquet")

# Method 1: Check for polygon column (most reliable)
if "polygon" in df.columns:
    version = "2026.04"

# Method 2: Check mask column type
elif "mask" in df.columns:
    mask_dtype = str(df["mask"].dtype)
    if mask_dtype.startswith("List(Float32"):
        version = "2025.10"    # NaN-separated polygon coordinates
    elif mask_dtype.startswith("List(UInt8"):
        version = "2026.04"    # raster pixel data
    else:
        version = "unknown"

else:
    version = "2025.10"        # no geometry columns
```

### JSON Files

```python
import json

with open("annotations.json") as f:
    data = json.load(f)

if isinstance(data, list):
    # 2025.10: bare array of samples
    samples = data
    version = "2025.10"
else:
    # 2026.04: object wrapper with metadata
    samples = data["samples"]
    version = data.get("schema_version", "2025.10")
```

## Reading 2026.04 Files

### Arrow IPC / Parquet

```python
import polars as pl

# Arrow IPC
df = pl.read_ipc("dataset.arrow")

# Parquet
df = pl.read_parquet("dataset.parquet")

# Access polygon data
if "polygon" in df.columns:
    for row in df.iter_rows(named=True):
        if row["polygon"] is not None:
            for ring in row["polygon"]:
                # ring is [x1, y1, x2, y2, ...] interleaved
                points = list(zip(ring[0::2], ring[1::2]))

# Access raster mask data
if "mask" in df.columns:
    for row in df.iter_rows(named=True):
        if row["mask"] is not None and row["size"] is not None:
            width, height = row["size"]
            pixels = row["mask"]  # List[int], length = width * height

# Access box2d — check format metadata
# (Schema metadata access depends on Polars version; prefer the EdgeFirst Client SDK)
if "box2d" in df.columns:
    for row in df.iter_rows(named=True):
        if row["box2d"] is not None:
            # Default: [cx, cy, w, h] — check box2d_format metadata if available
            cx, cy, w, h = row["box2d"]

# Access timing instrumentation
if "timing" in df.columns:
    for row in df.iter_rows(named=True):
        if row["timing"] is not None:
            t = row["timing"]
            load_ms = t["load"] / 1_000_000
            inference_ms = t["inference"] / 1_000_000
```

### Reading Parquet with DuckDB

```python
import duckdb

# Count labels
result = duckdb.sql("""
    SELECT label, count(*) as count
    FROM 'dataset.parquet'
    GROUP BY label
    ORDER BY count DESC
""")
print(result)

# Filter by score
result = duckdb.sql("""
    SELECT name, label, box2d, box2d_score
    FROM 'dataset.parquet'
    WHERE box2d_score > 0.8
""")
```

## JSON to DataFrame Conversion (2026.04)

### Column Name Mapping

| Arrow / Parquet column | JSON field | Notes |
|------------------------|------------|-------|
| `label` | `label_name` | Historical naming difference |
| `group` | `group_name` | Historical naming difference |
| `object_id` | `object_id` | 2026.04 uses `object_id` (not legacy `object_reference`) |
| `polygon` | `polygon` | JSON: `[[x,y], ...]` pairs; Arrow: interleaved `[x,y,x,y,...]` |
| `mask` | `mask` | Arrow: `List<UInt8>` row-major; JSON: base64-encoded string |
| `pose` | `sensors.imu` | Arrow: `[yaw, pitch, roll]`; JSON: `{yaw, pitch, roll}` object |
| `location` | `sensors.gps` | Arrow: `[lat, lon]`; JSON: `{latitude, longitude}` object |

### Full Conversion Example

```python
import polars as pl
import json, base64

with open("annotations.json") as f:
    data = json.load(f)

if isinstance(data, list):
    samples = data
    box2d_format = "ltwh"
else:
    samples = data["samples"]
    box2d_format = data.get("box2d_format", "ltwh")

rows = []
for sample in samples:
    size = [sample.get("width"), sample.get("height")]
    for ann in sample.get("annotations", []):
        row = {
            "name": sample["image_name"].rsplit(".", 1)[0],
            "frame": sample.get("frame_number"),
            "object_id": ann.get("object_id"),
            "label": ann["label_name"],
            "label_index": ann.get("label_index"),
            "group": sample.get("group_name"),
        }

        # Polygon: JSON [[x,y],...] per ring -> DataFrame [x,y,x,y,...] per ring
        if ann.get("polygon"):
            row["polygon"] = [
                [coord for pt in ring for coord in pt]
                for ring in ann["polygon"]
            ]
            row["polygon_score"] = ann.get("polygon_score")

        # Mask: JSON base64 -> DataFrame List<UInt8>
        if ann.get("mask") and isinstance(ann["mask"], str):
            row["mask"] = list(base64.b64decode(ann["mask"]))
            row["mask_score"] = ann.get("mask_score")

        # Box2D: convert based on format metadata
        if ann.get("box2d"):
            b = ann["box2d"]
            if box2d_format == "ltwh":
                row["box2d"] = [b["x"] + b["w"]/2, b["y"] + b["h"]/2, b["w"], b["h"]]
            elif box2d_format == "cxcywh":
                row["box2d"] = [b["cx"], b["cy"], b["w"], b["h"]]
            row["box2d_score"] = ann.get("box2d_score")

        # Box3D
        if ann.get("box3d"):
            b3 = ann["box3d"]
            row["box3d"] = [b3["x"], b3["y"], b3["z"], b3["w"], b3["h"], b3["l"]]
            row["box3d_score"] = ann.get("box3d_score")

        row["size"] = size
        rows.append(row)

df = pl.DataFrame(rows)
df.write_ipc("annotations.arrow")       # Arrow IPC
# df.write_parquet("annotations.parquet")  # or Parquet
```

### Key Conversions Summary

| # | Conversion | Direction |
|---|------------|-----------|
| 1 | **Unnest**: one row per annotation | JSON to DataFrame |
| 2 | **Column names**: `label_name` to `label`, `group_name` to `group` | JSON to DataFrame |
| 3 | **Polygon**: `[[x,y],...]` point pairs to `[x,y,x,y,...]` interleaved | JSON to DataFrame |
| 4 | **Mask**: base64 string to `List<UInt8>` | JSON to DataFrame |
| 5 | **Box2D**: check `box2d_format` — convert `ltwh` to `cxcywh` if needed | JSON to DataFrame |
| 6 | **Box3D**: `{x,y,z,w,h,l}` to `[cx,cy,cz,w,h,l]` | JSON to DataFrame |
| 7 | **GPS**: `{latitude, longitude}` to `[lat, lon]` | JSON to DataFrame |
| 8 | **IMU**: `{yaw, pitch, roll}` to `[yaw, pitch, roll]` | JSON to DataFrame |
| 9 | **Score columns**: omit entirely for ground truth files | Both |

!!! tip "Use the EdgeFirst Client SDK"
    The SDK handles all conversions automatically, including version detection and
    backward compatibility. Direct conversion code is shown here for reference and
    for users who need custom pipelines.
