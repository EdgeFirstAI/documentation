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
| `label_index` | `UInt64` | Source-faithful numeric class index (see [label_index details](#label_index)) |
| `group` | `Categorical` | Dataset split — `train`, `val`, `test` (JSON field: `group_name`) |

### Geometry: Polygon

| Column | Type | Description |
|--------|------|-------------|
| `polygon` | `List<List<f32>>` | Interleaved `[x1, y1, x2, y2, ...]` coordinate pairs per ring |
| `polygon_score` | `Float32` | Confidence score (0..1), nullable, optional |

!!! info "New in 2026.04"
    The `polygon` column replaces the 2025.10 `mask: List<Float32>` column that stored
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

### Annotation Metadata

| Column | Type | Description |
|--------|------|-------------|
| `iscrowd` | `UInt8` | `1` = crowd region, `0` = single instance. Optional, from COCO. |
| `category_frequency` | `Categorical` | Long-tail frequency group: `"f"`, `"c"`, or `"r"`. Optional. |

!!! info "New in 2026.04"
    These columns support COCO/LVIS dataset extensions. They are optional and will be
    absent from files that don't originate from COCO-family datasets.

**`iscrowd`**: COCO crowd annotations mark regions containing multiple overlapping
instances. Evaluation protocols treat them differently (matched but not penalized as
false negatives). LVIS does not use crowd annotations — this column will be absent or
null for LVIS-sourced data.

**`category_frequency`**: LVIS assigns each category to a frequency group based on how
many training images contain it:

- `"f"` (frequent) — appears in >100 images
- `"c"` (common) — appears in 11–100 images
- `"r"` (rare) — appears in 1–10 images

This enables disaggregated AP metrics (AP_r, AP_c, AP_f) and long-tail distribution
analysis. Use with Polars:

```python
# Count annotations by frequency group
df.group_by("category_frequency").len()

# Filter to rare categories only
rare = df.filter(pl.col("category_frequency") == "r")
```

### Sample Metadata

| Column | Type | Description |
|--------|------|-------------|
| `size` | `Array<u32, 2>` | `[width, height]` in pixels. **Required when `mask` is populated.** |
| `location` | `Array<f32, 2>` | `[latitude, longitude]` GPS coordinates |
| `pose` | `Array<f32, 3>` | `[yaw, pitch, roll]` IMU orientation in degrees |
| `degradation` | `String` | Visual quality indicator (`none`, `low`, `medium`, `high`) |
| `neg_label_indices` | `List<UInt32>` | `label_index` values for categories verified absent from this image |
| `not_exhaustive_label_indices` | `List<UInt32>` | `label_index` values for categories with possibly incomplete annotation |

**`neg_label_indices`** and **`not_exhaustive_label_indices`** come from LVIS's federated
annotation protocol. They enable correct evaluation by indicating which categories have
known annotation status in each image:

- **`neg_label_indices`**: Categories confirmed as **not present**. A model prediction for
  one of these categories is a valid false positive.
- **`not_exhaustive_label_indices`**: Categories where annotation may be **incomplete**.
  Unmatched predictions for these categories are ignored during evaluation (not penalized).

Both columns reference `label_index` values from the same file. They are sample-level
fields (repeated per annotation row for a given image).

!!! note "UInt32 vs UInt64"
    These lists use `UInt32` elements while `label_index` is `UInt64`. This is safe for
    COCO (max ID ~90) and LVIS (max ID ~1723). If you cross-join these columns in Polars,
    cast to a common type first: `col("neg_label_indices").cast(List(UInt64))`.

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
    # ── Identity & Classification ──────────────────────
    ('name', String),
    ('frame', UInt32),
    ('object_id', String),
    ('label', Categorical(ordering='physical')),
    ('label_index', UInt64),                    # source-faithful, may be non-contiguous
    ('group', Categorical(ordering='physical')),

    # ── Geometry: Polygon ──────────────────────────────
    ('polygon', List(List(Float32))),           # interleaved [x1,y1,x2,y2,...] per ring
    ('polygon_score', Float32),                 # OPTIONAL

    # ── Geometry: Raster Mask ──────────────────────────
    ('mask', List(UInt8)),                      # row-major u8 pixels
    ('mask_score', Float32),                    # OPTIONAL

    # ── Geometry: 2D Bounding Box ──────────────────────
    ('box2d', Array(Float32, shape=(4,))),      # layout from metadata
    ('box2d_score', Float32),                   # OPTIONAL

    # ── Geometry: 3D Bounding Box ──────────────────────
    ('box3d', Array(Float32, shape=(6,))),      # [cx, cy, cz, w, h, l]
    ('box3d_score', Float32),                   # OPTIONAL

    # ── Annotation Metadata (optional) ─────────────────
    ('iscrowd', UInt8),                         # OPTIONAL - COCO crowd flag
    ('category_frequency', Categorical(ordering='physical')),  # OPTIONAL - LVIS "f"/"c"/"r"

    # ── Sample Metadata (optional) ─────────────────────
    ('size', Array(UInt32, shape=(2,))),         # [width, height]
    ('location', Array(Float32, shape=(2,))),    # [lat, lon]
    ('pose', Array(Float32, shape=(3,))),        # [yaw, pitch, roll]
    ('degradation', String),
    ('neg_label_indices', List(UInt32)),          # OPTIONAL - LVIS negative categories
    ('not_exhaustive_label_indices', List(UInt32)),  # OPTIONAL - LVIS incomplete categories

    # ── Instrumentation (optional) ─────────────────────
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
| `category_metadata` | JSON string | absent | Per-label metadata (synset, synonyms, definition) |

Version format is `YYYY.MM` with mandatory zero-padding (e.g., `"2025.10"`, `"2026.04"`).
Versions are compared lexicographically. Unknown future versions should trigger a warning
(not an error) and attempt best-effort reading via schema introspection.

### Category Metadata

The `category_metadata` key stores per-label reference data as a JSON-encoded string.
This enriches label semantics without adding per-row columns for data that is constant
across all annotations sharing the same label.

```json
{
  "aerosol_can": {
    "synset": "aerosol.n.02",
    "synonyms": ["aerosol_can", "spray_can"],
    "definition": "a dispenser that holds a substance under pressure"
  },
  "person": {
    "synset": "person.n.01",
    "synonyms": ["person", "individual"],
    "definition": "a human being"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `synset` | string | WordNet synset identifier (e.g., `"aerosol.n.02"`) |
| `synonyms` | array of strings | Alternate names for the category |
| `definition` | string | Natural language definition |

**Source**: Populated from LVIS `categories` array when importing COCO with LVIS
extensions. Other datasets with taxonomic metadata can populate the same fields.

!!! note "Frequency is a column, not metadata"
    The `frequency` field from LVIS is stored as the `category_frequency` **column**
    (not in `category_metadata`) because it is directly useful for DataFrame filtering
    and disaggregated metrics.

### label_index

The `label_index` column stores the **source-faithful** category identifier. When
importing from COCO or LVIS, the original `category_id` is preserved directly as
`label_index`.

**Key characteristics**:

- **May be non-contiguous** — COCO uses IDs 1–90 for 80 categories (gaps at 12, 26,
  29, 30, etc.). LVIS uses IDs up to ~1723 for 1,203 categories.
- **May not start at zero** — COCO starts at 1, not 0.
- **Must be preserved on round-trip** — exporting back to COCO/LVIS reconstructs
  the original `category_id` from `label_index`.

!!! warning "Model training note"
    Models are typically trained with a dense remapping (e.g., 80 contiguous class
    indices for COCO). This remapping is a **model-specific concern** handled in the
    training pipeline, not in the dataset format. Some legacy models (notably older
    SSDs) are trained with the original gaps and produce 91 outputs (90 categories +
    background); this is likewise a model-specific convention.
