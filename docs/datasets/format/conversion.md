# Conversion Guidelines

!!! danger "2025.10 code is incompatible with 2026.04 and later files"
    Code written for the 2025.10 schema (NaN-separated masks, `mask: List<Float32>`) will produce **corrupt data** when applied to 2026.04 or 2026.10 files. Always check the schema version before processing. See the [Migration Guide](migration.md) for upgrade instructions.

## Version Detection

Always detect the schema version before reading annotation data.

### Arrow / Parquet Files

```python
import pyarrow.ipc as ipc
import pyarrow.parquet as pq
import polars as pl

# Method 1 (preferred): Check schema_version metadata
def get_schema_version(path: str) -> str:
    """Read schema_version from Arrow IPC or Parquet file metadata."""
    if path.endswith(".parquet"):
        metadata = pq.read_schema(path).metadata or {}
    else:
        with open(path, "rb") as f:
            metadata = ipc.open_file(f).schema.metadata or {}
    return metadata.get(b"schema_version", b"").decode()

schema_version = get_schema_version("dataset.arrow")

if schema_version:
    version = schema_version  # e.g. "2025.10", "2026.04", or "2026.10"
else:
    # Method 2 (fallback): Inspect column presence and types. The first rule that matches wins.
    df = pl.read_ipc("dataset.arrow")  # or pl.read_parquet(...)

    if "ignore" in df.columns or "exclude" in df.columns:
        version = "2026.10"
    elif "polygon" in df.columns:
        version = "2026.04"        # or 2026.10 with no flagged rows
    elif "mask" in df.columns:
        mask_dtype = str(df["mask"].dtype)
        if mask_dtype.startswith("List(Float32"):
            version = "2025.10"    # NaN-separated polygon coordinates
        elif str(mask_dtype) == "Binary":
            version = "2026.04"    # PNG-encoded raster pixels, or 2026.10
        else:
            version = "unknown"
    else:
        version = "2025.10"        # no geometry columns, no metadata
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
    # 2026.04 and later: object wrapper with metadata
    samples = data["samples"]
    version = data.get("schema_version", "2025.10")
```

## Reading 2026.04 and 2026.10 Files

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
            png_bytes = row["mask"]  # bytes (PNG-encoded raster pixels)

# Access box2d — always [cx, cy, w, h], normalized
if "box2d" in df.columns:
    for row in df.iter_rows(named=True):
        if row["box2d"] is not None:
            cx, cy, w, h = row["box2d"]

# Separate don't-care and excluded rows from ordinary annotations.
# Prefer ignore; fall back to the deprecated iscrowd column only when ignore is absent.
if "ignore" in df.columns:
    ignore = pl.col("ignore").fill_null(False)
elif "iscrowd" in df.columns:
    ignore = pl.col("iscrowd").cast(pl.Boolean).fill_null(False)
else:
    ignore = pl.lit(False)
exclude = pl.col("exclude").fill_null(False) if "exclude" in df.columns else pl.lit(False)

annotations = df.filter(~ignore & ~exclude)
dont_care = df.filter(ignore)
excluded = df.filter(exclude)

# IMU orientation — [roll, pitch, yaw] in signed degrees
if "pose" in df.columns:
    for row in df.iter_rows(named=True):
        if row["pose"] is not None:
            roll, pitch, yaw = row["pose"]

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

## JSON to DataFrame Conversion (2026.04 and later)

### Column Name Mapping

| Arrow / Parquet column | JSON field | Notes |
| ---------------------- | ---------- | ----- |
| `label` | `label_name` | Historical naming difference |
| `group` | `group_name` | Historical naming difference |
| `object_id` | `object_id` | 2026.04 uses `object_id` (not legacy `object_reference`) |
| `polygon` | `polygon` | JSON: `[[x,y], ...]` pairs; Arrow: interleaved `[x,y,x,y,...]` |
| `mask` | `mask` | Arrow: `Binary` (PNG bytes); JSON: base64-encoded PNG string |
| `ignore` | `ignore` | `Boolean` in both formats; JSON also accepts `iscrowd` as an alias |
| `exclude` | `exclude` | `Boolean` in both formats |
| `iscrowd` | `iscrowd` | Deprecated mirror of `ignore` |
| `category_frequency` | `category_frequency` | Same in both formats (`"f"`, `"c"`, `"r"`) |
| `truncation`, `occlusion` | `attributes.truncation`, `attributes.occlusion` | Arrow: `UInt32` columns; JSON: nested `attributes` object |
| `neg_label_indices` | `neg_label_indices` | Arrow: `List<UInt32>`; JSON: array of integers |
| `not_exhaustive_label_indices` | `not_exhaustive_label_indices` | Arrow: `List<UInt32>`; JSON: array of integers |
| `pose` | `sensors.imu` | Arrow: `[roll, pitch, yaw]` signed degrees; JSON: `{roll, pitch, yaw}` object |
| `location` | `sensors.gps` | Arrow: `[lat, lon]`; JSON: `{lat, lon}` object |

File-level metadata keys (`schema_version`, `category_metadata`, `labels`) are not per-row columns. They are stored in the Arrow/Parquet schema metadata or in the JSON top-level object. See [File-Level Metadata](schema.md#file-level-metadata) for the full list.

### Full Conversion Example

```python
import polars as pl
import json, base64

with open("annotations.json") as f:
    data = json.load(f)

samples = data if isinstance(data, list) else data["samples"]

rows = []
for sample in samples:
    size = [sample.get("width"), sample.get("height")]
    sensors = sample.get("sensors") or {}
    gps, imu = sensors.get("gps"), sensors.get("imu")
    location = [gps["lat"], gps["lon"]] if gps else None
    pose = [imu["roll"], imu["pitch"], imu["yaw"]] if imu else None

    for ann in sample.get("annotations", []):
        row = {
            "name": sample["image_name"].rsplit(".", 1)[0],
            "frame": sample.get("frame_number"),
            "object_id": ann.get("object_id"),
            "label": ann.get("label_name"),  # optional on ignore/exclude rows
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

        # Mask: JSON base64 PNG -> DataFrame Binary (PNG bytes)
        if ann.get("mask") and isinstance(ann["mask"], str):
            row["mask"] = base64.b64decode(ann["mask"])  # PNG bytes
            row["mask_score"] = ann.get("mask_score")

        # Box2D: JSON ltwh {x, y, w, h} -> Arrow cxcywh [cx, cy, w, h]
        if ann.get("box2d"):
            b = ann["box2d"]
            row["box2d"] = [b["x"] + b["w"]/2, b["y"] + b["h"]/2, b["w"], b["h"]]
            row["box2d_score"] = ann.get("box2d_score")

        # Box3D: x,y,z are center coordinates (not corner)
        if ann.get("box3d"):
            b3 = ann["box3d"]
            row["box3d"] = [b3["x"], b3["y"], b3["z"], b3["w"], b3["h"], b3["l"]]
            row["box3d_score"] = ann.get("box3d_score")

        # ignore / exclude flags; iscrowd is a deprecated alias of ignore
        ignore = ann.get("ignore")
        if ignore is None and ann.get("iscrowd") is not None:
            ignore = bool(ann["iscrowd"])  # handles legacy 0/1
        row["ignore"] = ignore
        row["exclude"] = ann.get("exclude")

        # Annotation metadata (LVIS, VisDrone, KITTI extensions)
        if "category_frequency" in ann:
            row["category_frequency"] = ann["category_frequency"]
        attributes = ann.get("attributes") or {}
        row["truncation"] = attributes.get("truncation")
        row["occlusion"] = attributes.get("occlusion")

        # Sample-level LVIS fields (repeated per annotation row)
        if "neg_label_indices" in sample:
            row["neg_label_indices"] = sample["neg_label_indices"]
        if "not_exhaustive_label_indices" in sample:
            row["not_exhaustive_label_indices"] = sample["not_exhaustive_label_indices"]

        row["size"] = size
        row["location"] = location
        row["pose"] = pose
        rows.append(row)

df = pl.DataFrame(rows)
df.write_ipc("annotations.arrow")       # Arrow IPC
# df.write_parquet("annotations.parquet")  # or Parquet
```

### Key Conversions Summary

| # | Conversion | Direction |
| --- | ---------- | --------- |
| 1 | **Unnest**: one row per annotation | JSON to DataFrame |
| 2 | **Column names**: `label_name` to `label`, `group_name` to `group` | JSON to DataFrame |
| 3 | **Polygon**: `[[x,y],...]` point pairs to `[x,y,x,y,...]` interleaved | JSON to DataFrame |
| 4 | **Mask**: base64 PNG string → `Binary` (PNG bytes) | JSON to DataFrame |
| 5 | **Box2D**: `ltwh` `{x, y, w, h}` to `cxcywh` `[cx, cy, w, h]` | JSON to DataFrame |
| 6 | **Box3D**: `{x,y,z,w,h,l}` to `[cx,cy,cz,w,h,l]` | JSON to DataFrame |
| 7 | **GPS**: `{lat, lon}` to `[lat, lon]` | JSON to DataFrame |
| 8 | **IMU**: `{roll, pitch, yaw}` to `[roll, pitch, yaw]`, signed degrees | JSON to DataFrame |
| 9 | **Score columns**: omit entirely for ground truth files | Both |
| 10 | **`ignore`** / **`exclude`**: annotation-level `Boolean`, same semantics in both formats; `iscrowd` is accepted as a deprecated alias of `ignore` | JSON to DataFrame |
| 11 | **Attributes**: JSON `attributes.truncation` / `attributes.occlusion` to `UInt32` columns | JSON to DataFrame |
| 12 | **`neg_label_indices`** / **`not_exhaustive_label_indices`**: sample-level, repeated per annotation row | JSON to DataFrame |
| 13 | **`label_index`**: preserved as-is (source-faithful, non-contiguous) | Both |
| 14 | **`category_metadata`**: file-level metadata — JSON-encoded string of per-label synset/synonyms/definition. Extract from LVIS `categories` array when importing; attach to Arrow schema metadata when writing. | Both |

!!! tip "Use the EdgeFirst Client SDK"
    The SDK handles all conversions automatically, including version detection and
    backward compatibility. Direct conversion code is shown here for reference and
    for users who need custom pipelines.
