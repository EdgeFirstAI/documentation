# Annotation Schema

**Schema version**: `2026.10`

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
are always **normalized** (0..1) relative to the full image. Multiply by image dimensions
to get pixel coordinates.

**Coordinate space**: Polygon coordinates are always image-space normalized, regardless of
whether `box2d` coexists on the same row. The box provides object location; the polygon
provides the precise boundary in full-image coordinates.

**Validity rules**:

- Inner lists must have an **even** number of values (coordinate pairs)
- Minimum **6 values** (3 points) per valid ring
- Odd-length inner lists are invalid — writers reject, readers drop with a warning

### Geometry: Raster Mask

| Column | Type | Description |
|--------|------|-------------|
| `mask` | `Binary` | PNG-encoded grayscale raster pixels |
| `mask_score` | `Float32` | Per-instance confidence (0..1), nullable, optional |

!!! warning "Type changed in 2026.04"
    The `mask` column changed from `List<Float32>` (NaN-separated polygons in 2025.10)
    to `Binary` (PNG-encoded raster pixels in 2026.04). Code that assumes `Float32` will
    fail on 2026.04 files.

**Encoding**: Masks are stored as single-channel (grayscale) PNG images within the
`Binary` column. The PNG format provides:

- **Self-describing dimensions** — width and height in the PNG header (first 24 bytes),
  readable without full decode
- **Lossless compression** — typically 2–10× smaller than raw pixel arrays
- **Variable bit depth** — 1-bit for binary masks, 8-bit for confidence/sigmoid/logits,
  16-bit for high-precision outputs

| Source | PNG bit depth | Pixel values | Use case |
|--------|--------------|--------------|----------|
| Binary mask (any source) | **1-bit (preferred)** | 0/1 | Ground truth, thresholded output, COCO RLE import |
| Sigmoid scores | 8-bit | 0–255 (quantized) | Model confidence per-pixel |
| High-precision scores | 16-bit | 0–65535 | When 8-bit quantization is insufficient |

**1-bit is the preferred encoding for all binary masks**, regardless of source (COCO RLE,
thresholded model output, ground truth annotations). Alternatives like 8-bit with 0/255
are valid but wasteful and ambiguous — a reader cannot distinguish "binary mask stored as
8-bit" from "8-bit score data." 1-bit encoding is self-documenting: if the PNG is 1-bit,
the mask is binary.

**Dimensions**: Mask dimensions are defined by the PNG image itself, not by the `size`
column or `box2d`. The producer determines the resolution — it could be the original
image size, model input size, or model output size. Consumers read the PNG header to
discover the mask dimensions and rescale to the target coordinate space as needed.

**Coverage**: The mask covers the **full image**, not a crop of the bounding box. For
instance segmentation, most pixels are 0 (background) and the object region has
confidence scores or binary 1 values. This avoids lossy cropping and handles
interpolation that extends beyond box bounds.

**Interpretation by context**:

| Context | Pixel values | Label source |
|---------|-------------|-------------|
| `mask` + `box2d` (instance seg) | Sigmoid confidence (0–255) or binary (0/1) for a single instance | `label` column on the row |
| `mask` without `box2d` (semantic seg) | Argmax class indices | Optional file-level `labels` metadata; index ordering is model-specific |

**Interpretation**: The PNG bit depth determines the value range. The specification reserves a `mask_interpretation` file-level metadata key to name the pixel meaning; it is not yet written or read by the EdgeFirst Client (see [File-Level Metadata](#file-level-metadata)).

| Value | Description |
|-------|-------------|
| `binary` | 0/1 values — use 1-bit PNG (default) |
| `confidence` | Quantized confidence scores — use 8-bit (0–255) or 16-bit (0–65535) PNG |
| `sigmoid` | Quantized sigmoid outputs — use 8-bit or 16-bit PNG |
| `logits` | Quantized logit outputs — use 8-bit or 16-bit PNG |

**JSON representation**: base64-encoded PNG bytes.

**Relationship to polygon**: `polygon` and `mask` can coexist in the same file
(e.g., panoptic segmentation). Typically a dataset uses one or the other. Both use
full-image coordinates — polygons are normalized (0..1), masks cover the full image.

### Geometry: 2D Bounding Box

| Column | Type | Description |
|--------|------|-------------|
| `box2d` | `Array<f32, 4>` | `[center_x, center_y, width, height]`, normalized |
| `box2d_score` | `Float32` | Confidence score (0..1), nullable, optional |

Arrow and Parquet files always store `box2d` as `[center_x, center_y, width, height]` (`cxcywh`) in normalized coordinates. See [Box Formats](box_format.md) for the JSON layout and conversions.

### Geometry: 3D Bounding Box

| Column | Type | Description |
|--------|------|-------------|
| `box3d` | `Array<f32, 6>` | `[center_x, center_y, center_z, width, height, length]` |
| `box3d_score` | `Float32` | Confidence score (0..1), nullable, optional |

Layout: `[center_x, center_y, center_z, width, height, length]` (`cxcyczwhl`).

- Width (w) = X-axis extent
- Height (h) = Y-axis extent
- Length (l) = Z-axis extent

All coordinates represent the **geometric center** of the bounding box.
See [Box Formats](box_format.md) for details.

### Annotation Metadata

| Column | Type | Description |
|--------|------|-------------|
| `ignore` | `Boolean` | `true` = don't-care region, masked out of loss and evaluation. Optional. New in 2026.10. |
| `exclude` | `Boolean` | `true` = real object outside the dataset's class set. Optional. New in 2026.10. |
| `iscrowd` | `Boolean` | **Deprecated in 2026.10** — mirror of `ignore`, written for compatibility. Optional. |
| `category_frequency` | `Categorical` | Long-tail frequency group: `"f"`, `"c"`, or `"r"`. Optional. |
| `truncation` | `UInt32` | Source truncation flag (how much of the object is cut off by the image border). Optional. |
| `occlusion` | `UInt32` | Source occlusion flag (how much of the object is hidden by other objects). Optional. |

These columns are optional and absent from files whose source dataset does not provide them. Columns whose values are all null are dropped when a file is written, so a 2026.10 file with no flagged rows has no `ignore` or `exclude` column.

#### ignore

!!! info "New in 2026.10"

Marks a don't-care region that should be masked out of loss and evaluation rather than treated as a false negative or false positive.

- `true` — don't-care region
- `false` or absent — ordinary annotation

`label` and `label_index` are optional on a flagged row. A labeled `ignore` row applies to that class only (for example a crowd of people should not penalize a `person` detector inside the region); an unlabeled `ignore` row applies to all classes.

**Sources**: COCO `iscrowd=1` becomes `ignore=true`. VisDrone category 0 (`ignored regions`) becomes an unlabeled `ignore=true` row when `edgefirst-client visdrone-to-arrow --keep-ignored` is used; by default those rows are dropped.

**JSON representation**: `"ignore": true` on the annotation object, omitted when null. On read, `iscrowd` is accepted as an alias of `ignore`.

#### exclude

!!! info "New in 2026.10"

Marks a real object that falls outside the dataset's class set. Trainers leave it out of training, and evaluators should neither count a detection that matches it as a false positive nor count the object itself as a missed detection.

- `true` — real object outside the class set
- `false` or absent — ordinary annotation

`label` and `label_index` are optional on a flagged row and are typically absent, since the object has no class in this dataset.

**Sources**: VisDrone category 11 (`others`) becomes an unlabeled `exclude=true` row when `edgefirst-client visdrone-to-arrow --keep-ignored` is used; by default those rows are dropped.

**JSON representation**: `"exclude": true` on the annotation object, omitted when null.

!!! warning "EdgeFirst Studio does not store `ignore` or `exclude` yet"
    Uploads with `upload-dataset`, `populate_samples`, `import-coco`, and `import-coco --update` drop annotations flagged `ignore` or `exclude`, including COCO crowd annotations, and log one warning per upload with the number skipped. Keep the Arrow or Parquet file as the source of truth for these flags.

#### iscrowd

!!! warning "Deprecated in 2026.10"
    `iscrowd` is replaced by [`ignore`](#ignore). Read and write support will be removed in a future release.

Files written by the EdgeFirst Client carry `iscrowd` as an exact mirror of `ignore`, so it can be `true` on rows that are not COCO crowds (for example unlabeled VisDrone `ignored regions`). In 2026.04 files it holds the COCO `iscrowd` field.

The client reads `iscrowd` as `ignore` when `ignore` is absent:

- **Arrow / Parquet**: the fallback is per column. When the file has an `ignore` column, it is used for every row (even rows where it is null) and `iscrowd` is not consulted. Both `Boolean` and the older integer type are accepted.
- **JSON**: the fallback is per annotation. An annotation object without an `ignore` key, or with `"ignore": null`, takes its `iscrowd` value.

`edgefirst-client arrow-to-coco` writes COCO `iscrowd=1` from labeled `ignore` rows. Unlabeled `ignore` rows and all `exclude` rows have no COCO equivalent and are skipped with one warning giving the count.

#### category_frequency

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

#### truncation and occlusion

Source dataset flags describing how much of the object is cut off by the image border (`truncation`) or hidden by other objects (`occlusion`). Values keep the source dataset's scale:

| Source | `truncation` | `occlusion` |
|--------|--------------|-------------|
| VisDrone | 0 = none, 1 = 1–50% | 0 = none, 1 = 1–50%, 2 = over 50% |
| KITTI | `round(truncated * 100)`, clipped to 0–100 | `occluded` 0–3, stored as is |

**JSON representation**: a nested object on the annotation, `"attributes": {"truncation": 1, "occlusion": 2}`, omitted when both are absent.

!!! note "Not stored by EdgeFirst Studio yet"
    `upload-dataset` sends these columns but Studio does not persist them yet; the client warns which optional columns are not stored. Keep the Arrow or Parquet file as the source of truth.

### Sample Metadata

| Column | Type | Description |
|--------|------|-------------|
| `size` | `Array<u32, 2>` | `[width, height]` — original image dimensions in pixels. Optional. |
| `location` | `Array<f32, 2>` | `[latitude, longitude]` GPS coordinates in decimal degrees |
| `pose` | `Array<f32, 3>` | `[roll, pitch, yaw]` IMU orientation in signed degrees (see [IMU orientation](#imu-orientation)) |
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

#### IMU orientation

The `pose` column stores the sensor orientation as three Euler angles in **signed degrees**, listed in axis order:

| Index | Angle | Axis | Range |
|-------|-------|------|-------|
| `pose[0]` | roll | X | −180 to 180 |
| `pose[1]` | pitch | Y | −90 to 90 |
| `pose[2]` | yaw | Z | −180 to 180 |

The angles follow the [ROS REP-103](https://www.ros.org/reps/rep-0103.html) convention: rotations about the fixed X, Y, and Z axes, which is equivalent to the intrinsic Z-Y′-X″ (yaw, then pitch, then roll) sequence, so `R = Rz(yaw) · Ry(pitch) · Rx(roll)`. Listing the values by axis (x, y, z) matches ROS 2 (`tf2` `setRPY`/`getRPY`, URDF `rpy`, the `sensor_msgs/Imu` covariance layout), MAVLink `ATTITUDE`, and KITTI OXTS.

The JSON representation uses named fields `{roll, pitch, yaw}` in the `sensors.imu` object, so field order does not matter there.

!!! warning "Files written before 2026.10 may have roll and yaw swapped"
    Before 2026.10 the `pose` order was not consistent between tools. EdgeFirst Client 2.14 and earlier wrote `[yaw, pitch, roll]`, while the EdgeFirst Publisher wrote `[roll, pitch, yaw]` with each angle wrapped to 0–360. The order cannot be detected from the file, so check which tool produced an older file and swap `pose[0]` and `pose[2]` if needed. See [Migration Guide](migration.md#imu-pose-and-gps-location-in-older-files).

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

```text
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
- Raster masks can additionally carry **per-pixel** scores in 8-bit or 16-bit PNG pixels; `mask_score` is the per-instance aggregate
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
    ('mask', Binary),                            # PNG-encoded grayscale raster pixels
    ('mask_score', Float32),                    # OPTIONAL

    # ── Geometry: 2D Bounding Box ──────────────────────
    ('box2d', Array(Float32, shape=(4,))),      # [cx, cy, w, h]
    ('box2d_score', Float32),                   # OPTIONAL

    # ── Geometry: 3D Bounding Box ──────────────────────
    ('box3d', Array(Float32, shape=(6,))),      # [cx, cy, cz, w, h, l]
    ('box3d_score', Float32),                   # OPTIONAL

    # ── Annotation Metadata (optional) ─────────────────
    ('ignore', Boolean),                        # OPTIONAL - don't-care region (2026.10)
    ('exclude', Boolean),                       # OPTIONAL - object outside the class set (2026.10)
    ('iscrowd', Boolean),                       # DEPRECATED - mirror of ignore
    ('category_frequency', Categorical(ordering='physical')),  # OPTIONAL - LVIS "f"/"c"/"r"
    ('truncation', UInt32),                     # OPTIONAL - source truncation flag
    ('occlusion', UInt32),                      # OPTIONAL - source occlusion flag

    # ── Sample Metadata (optional) ─────────────────────
    ('size', Array(UInt32, shape=(2,))),         # [width, height]
    ('location', Array(Float32, shape=(2,))),    # [lat, lon]
    ('pose', Array(Float32, shape=(3,))),        # [roll, pitch, yaw], signed degrees
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

Arrow IPC stores key-value metadata on the schema, while Parquet stores key-value
metadata in the file footer. In both formats, all metadata values are strings.

| Key | Values | Default (absent) | Description | Implemented |
|-----|--------|-------------------|-------------|-------------|
| `schema_version` | `"2026.10"` (current), `"2026.04"` | `"2025.10"` | Format version. Absent = legacy file. | Yes |
| `category_metadata` | JSON string | absent | Per-label metadata (synset, synonyms, definition) | Yes |
| `labels` | JSON array `["person", "car", ...]` | absent | Ordered class names for semantic segmentation masks. `labels[i]` = class name for argmax pixel value `i`. | Yes |
| `box2d_format` | `"cxcywh"`, `"xyxy"`, `"ltwh"` | `"cxcywh"` | Box2D layout descriptor | Reserved |
| `box2d_normalized` | `"true"`, `"false"` | `"true"` | Box2D coordinate system | Reserved |
| `box3d_format` | `"cxcyczwhl"` | `"cxcyczwhl"` | Box3D layout descriptor | Reserved |
| `box3d_normalized` | `"true"`, `"false"` | `"true"` | Box3D coordinate system | Reserved |
| `mask_interpretation` | `"binary"`, `"confidence"`, `"sigmoid"`, `"logits"` | `"binary"` | Pixel value meaning | Reserved |

!!! note "Reserved keys"
    Only `schema_version`, `category_metadata`, and `labels` are written and read by the EdgeFirst Client. The reserved keys are part of the specification's design but are not yet implemented: `box2d` is always `cxcywh` in Arrow and Parquet and `ltwh` in JSON, and coordinates are always normalized. Readers should not rely on the reserved keys being present.

Version format is `YYYY.MM` with mandatory zero-padding (e.g., `"2025.10"`, `"2026.04"`, `"2026.10"`).
Versions are compared lexicographically. Unknown future versions should trigger a warning
(not an error) and attempt best-effort reading via schema introspection.

### Category Metadata

The `category_metadata` key stores per-label reference data as a JSON-encoded string.
This enriches label semantics without adding per-row columns for data that is constant
across all annotations sharing the same label.

```json
{
  "aerosol_can": {
    "id": 1,
    "supercategory": "accessory",
    "synset": "aerosol.n.02",
    "synonyms": ["aerosol_can", "spray_can"],
    "definition": "a dispenser that holds a substance under pressure"
  },
  "person": {
    "id": 1,
    "supercategory": "human",
    "synset": "person.n.01",
    "synonyms": ["person", "individual"],
    "definition": "a human being"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Source category ID (used to reconstruct `category_id` for categories with no annotations) |
| `supercategory` | string | Parent category name (e.g., `"vehicle"`, `"animal"`) |
| `synset` | string | WordNet synset identifier (e.g., `"aerosol.n.02"`) |
| `synonyms` | array of strings | Alternate names for the category |
| `definition` | string | Natural language definition (LVIS `def` field, renamed for clarity) |

**Source**: When importing from COCO with LVIS extensions, these fields are populated
from the LVIS `categories` array. Other datasets with taxonomic metadata can populate
the same fields.

!!! note "Frequency is a column, not metadata"
    The `frequency` field from LVIS is stored as the `category_frequency` **column**
    (not in `category_metadata`) because it is directly useful for DataFrame filtering
    and disaggregated metrics. The `image_count` and `instance_count` fields from LVIS
    are intentionally not stored — they are recomputable statistics.

### Labels Metadata

!!! info "New in 2026.04"

The `labels` key stores an ordered array of class names as a JSON-encoded string. This
metadata provides the index-to-name mapping for semantic segmentation masks where each
pixel value is an argmax class index.

**Structure**: JSON array where `labels[i]` is the class name for pixel value `i`:

```json
["background", "person", "car", "bicycle", "dog"]
```

In this example, pixel value `0` = `"background"`, pixel value `1` = `"person"`,
pixel value `2` = `"car"`, etc.

**When written**: Optional — only written when the source dataset provides an ordered
category list (e.g., COCO categories sorted by ID).

**Relationship to `category_metadata`**: The `labels` array provides index ordering for
mask pixel interpretation. The `category_metadata` object provides rich per-label
reference data (synset, synonyms, definition). Both may be present; they complement
each other.

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
