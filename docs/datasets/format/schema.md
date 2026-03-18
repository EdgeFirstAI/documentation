# Annotation Schema

**Schema version**: `2026.04`

The EdgeFirst annotation schema uses a flat, columnar layout: **one row per annotation
instance**. All columns are nullable unless noted otherwise. Optional columns may be
absent entirely from a file.

## Column Reference

### Identity & Classification

| Column | Type | Description |
|--------|------|-------------|
| `name` | `String` | Sample identifier (derived from filename) |
| `frame` | `UInt32` | Sequence frame number (null for standalone images) |
| `object_id` | `String` | Instance tracking UUID |
| `label` | `Categorical` | Class label (JSON field: `label_name`) |
| `label_index` | `UInt64` | Numeric class index |
| `group` | `Categorical` | Dataset split — `train`, `val`, `test` (JSON field: `group_name`) |

### Geometry: Polygon

| Column | Type | Description |
|--------|------|-------------|
| `polygon` | `List<List<f32>>` | Interleaved `[x1, y1, x2, y2, ...]` coordinate pairs per ring |
| `polygon_score` | `Float32` | Confidence score (0..1), nullable, optional |

!!! info "New in 2026.04"
    The `polygon` column replaces the 2025.10 `mask: List<f32>` column that stored
    NaN-separated polygon coordinates. See [Migration Guide](migration.md) for details.

**Outer list**: Multiple polygon rings per instance (disjoint parts, holes).

**Inner list**: Interleaved `[x1, y1, x2, y2, ...]` pairs for one ring. Coordinates
are always **normalized** (0..1). Multiply by `size` values to get pixel coordinates.

**Validity rules**:

- Inner lists must have an **even** number of values (coordinate pairs)
- Minimum **6 values** (3 points) per valid ring
- Odd-length inner lists are invalid — writers reject, readers drop with a warning

### Geometry: Raster Mask

| Column | Type | Description |
|--------|------|-------------|
| `mask` | `List<UInt8>` | Row-major pixel values, `width * height` elements |
| `mask_score` | `Float32` | Per-instance confidence (0..1), nullable, optional |

!!! warning "Type changed in 2026.04"
    The `mask` column changed from `List<Float32>` (NaN-separated polygons in 2025.10)
    to `List<UInt8>` (raster pixels in 2026.04). Code that assumes `Float32` will fail
    on 2026.04 files.

**Encoding**: Raw row-major `u8` pixel values.

**Dimensions**: Derived from the `size` column `[width, height]`. The `size` column is
**required** when `mask` is populated — a raster mask without dimensions is uninterpretable.

**Interpretation**: Controlled by `mask_interpretation` file-level metadata:

| Value | Description |
|-------|-------------|
| `binary` | Thresholded 0/1 values (default) |
| `confidence` | 0–255 quantized confidence scores |
| `sigmoid` | 0–255 quantized sigmoid outputs |
| `logits` | 0–255 quantized logit outputs |

**Relationship to polygon**: `polygon` and `mask` can coexist in the same file
(e.g., panoptic segmentation). Typically a dataset uses one or the other.

### Geometry: 2D Bounding Box

| Column | Type | Description |
|--------|------|-------------|
| `box2d` | `Array<f32, 4>` | Layout described by `box2d_format` metadata |
| `box2d_score` | `Float32` | Confidence score (0..1), nullable, optional |

The array element order depends on the `box2d_format` file metadata. Default is
`[center_x, center_y, width, height]` (`cxcywh`). See [Box Formats](box_format.md)
for all layouts.

### Geometry: 3D Bounding Box

| Column | Type | Description |
|--------|------|-------------|
| `box3d` | `Array<f32, 6>` | Layout described by `box3d_format` metadata |
| `box3d_score` | `Float32` | Confidence score (0..1), nullable, optional |

Default layout: `[center_x, center_y, center_z, width, height, length]` (`cxcyczwhl`).

- Width (w) = X-axis extent
- Height (h) = Y-axis extent
- Length (l) = Z-axis extent

All coordinates represent the **geometric center** of the bounding box.
See [Box Formats](box_format.md) for details.

### Sample Metadata

| Column | Type | Description |
|--------|------|-------------|
| `size` | `Array<u32, 2>` | `[width, height]` in pixels. **Required when `mask` is populated.** |
| `location` | `Array<f32, 2>` | `[latitude, longitude]` GPS coordinates |
| `pose` | `Array<f32, 3>` | `[yaw, pitch, roll]` IMU orientation in degrees |
| `degradation` | `String` | Visual quality indicator (`none`, `low`, `medium`, `high`) |

!!! tip "Pose array order"
    The `pose` array is always `[yaw, pitch, roll]` in degrees. The JSON representation
    uses named fields `{yaw, pitch, roll}` in the `sensors.imu` object.

### Instrumentation

| Column | Type | Description |
|--------|------|-------------|
| `timing` | `Struct` | Pipeline timing data (optional) |

The `timing` struct contains `Int64` nanosecond duration fields:

| Field | Description |
|-------|-------------|
| `load` | Time to load input data |
| `preprocess` | Time for preprocessing transforms |
| `inference` | Model inference time |
| `decode` | Time for postprocessing / decoding outputs |

**Example**:

```
timing: {load: 1500000, preprocess: 3200000, inference: 12500000, decode: 800000}
# = 1.5 ms load, 3.2 ms preprocess, 12.5 ms inference, 0.8 ms decode
```

Fields are extensible — future fields do not break older readers since Struct access is
by name.

## Score Columns

`box2d_score`, `box3d_score`, `polygon_score`, and `mask_score` are independent
per-geometry confidence values in the range 0..1.

- A single row may have **different scores** for different geometry types (e.g., high
  box confidence but lower polygon confidence)
- Raster masks additionally carry **per-pixel** scores via `mask_interpretation`
  metadata; `mask_score` is the per-instance aggregate
- **Ground truth files**: score columns should be **omitted entirely** (not filled
  with nulls). Readers must treat absent score columns as "not applicable."

## Complete Polars Schema

For reference, the full Polars-style schema:

```python
(
    ('name', String),
    ('frame', UInt32),
    ('object_id', String),
    ('label', Categorical(ordering='physical')),
    ('label_index', UInt64),
    ('group', Categorical(ordering='physical')),
    ('polygon', List(List(Float32))),
    ('polygon_score', Float32),
    ('mask', List(UInt8)),
    ('mask_score', Float32),
    ('box2d', Array(Float32, shape=(4,))),
    ('box2d_score', Float32),
    ('box3d', Array(Float32, shape=(6,))),
    ('box3d_score', Float32),
    ('size', Array(UInt32, shape=(2,))),
    ('location', Array(Float32, shape=(2,))),
    ('pose', Array(Float32, shape=(3,))),
    ('degradation', String),
    ('timing', Struct({
        'load': Int64,
        'preprocess': Int64,
        'inference': Int64,
        'decode': Int64,
    })),
)
```

## File-Level Metadata

Both Arrow IPC and Parquet files carry key-value metadata at the schema level.
All metadata values are strings.

| Key | Values | Default (absent) | Description |
|-----|--------|-------------------|-------------|
| `schema_version` | `"2026.04"` | `"2025.10"` | Format version. Absent = legacy file. |
| `box2d_format` | `"cxcywh"`, `"xyxy"`, `"ltwh"` | `"cxcywh"` | Box2D layout descriptor |
| `box2d_normalized` | `"true"`, `"false"` | `"true"` | Box2D coordinate system |
| `box3d_format` | `"cxcyczwhl"` | `"cxcyczwhl"` | Box3D layout descriptor |
| `box3d_normalized` | `"true"`, `"false"` | `"true"` | Box3D coordinate system |
| `mask_interpretation` | `"binary"`, `"confidence"`, `"sigmoid"`, `"logits"` | `"binary"` | Pixel value meaning |

Version format is `YYYY.MM` with mandatory zero-padding (e.g., `"2025.10"`, `"2026.04"`).
Versions are compared lexicographically. Unknown future versions should trigger a warning
(not an error) and attempt best-effort reading via schema introspection.
