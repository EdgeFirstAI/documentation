# Model Metadata

This document describes the metadata schema embedded in EdgeFirst model files. Model metadata provides complete traceability for MLOps workflows and contains all information needed to decode model outputs for inference.

## Overview

EdgeFirst models embed metadata that enables:

- **Full Traceability**: Link any deployed model back to its [training session](../studio/models.md#training-sessions), [dataset](../datasets/index.md), and configuration in [EdgeFirst Studio](../studio/index.md)
- **Self-Describing Models**: Models contain all information needed for inference without external configuration files
- **Cross-Platform Compatibility**: Consistent schema across TFLite and ONNX formats
- **Third-Party Integration**: Any training framework can produce EdgeFirst-compatible models by following this schema
- **Converter Workflows**: Split hints and calibration artifacts enable model-agnostic conversion pipelines for quantization and target-specific compilation

### Schema Version

The current schema is **version 2**. The top-level `schema_version: 2` field is required on v2 metadata. Tooling uses this field to select the correct parser and to reject documents that omit fields mandated by the active version.

```yaml
schema_version: 2
```

### Supported Formats

EdgeFirst models from the [Model Zoo](index.md) (including [ModelPack](modelpack/index.md) and [Ultralytics](ultralytics/index.md)) embed metadata in format-specific locations:

| Format | Metadata Location | Config Format | Labels |
| ------ | ----------------- | ------------- | ------ |
| TFLite | ZIP archive (associated files) | `edgefirst.json` | `labels.txt` |
| ONNX | Custom metadata properties | `edgefirst` (JSON) | `labels` (JSON array) |
| Keras weights (`.keras`) | ZIP archive member | `edgefirst.json` | `labels.txt` |
| PyTorch weights (`.pt`) | Checkpoint dictionary key | `edgefirst` (JSON string) | `dataset.classes` |

Metadata is always embedded in the artifact it describes. Trainers embed the same metadata in the weights they publish (`.keras` or `.pt`) as in the exported models, so that a later session can load those weights and know exactly how they were trained. A standalone `edgefirst.json` is never published, because a session produces several artifacts and a loose file would not say which one it describes.

### Supported Training Frameworks

| Framework | Decoder | Architecture | Use Case |
| --------- | ------- | ------------ | -------- |
| [ModelPack](modelpack/index.md) | `modelpack` | Anchor-based YOLO | Semantic segmentation, detection |
| [Ultralytics](ultralytics/index.md) | `ultralytics` | Anchor-free DFL (YOLOv5/v8/v11/v26) | Instance segmentation, detection |

!!! note
    These metadata fields are automatically read and handled by the [EdgeFirst Profiler](../profiler/index.md) and the [EdgeFirst Perception Middleware](../perception/index.md). In most cases, developers don't need to worry about these details — the EdgeFirst ecosystem "Just Works." This documentation exists so developers understand what's happening under the hood when needed.

---

## Traceability for Production MLOps

One of the most critical aspects of production ML systems is **traceability** — the ability to answer questions like:

- Where was this model trained?
- What dataset was used?
- What were the training parameters?
- Can I reproduce this model?

EdgeFirst metadata provides complete traceability through these key fields:

| Field | Location | Purpose |
| ----- | -------- | ------- |
| `studio_server` | `host.studio_server` | Full hostname of [EdgeFirst Studio](../studio/index.md) instance (e.g., test.edgefirst.studio) |
| `project_id` | `host.project_id` | Project ID for constructing Studio URLs |
| `session_id` | `host.session` | [Training session](../studio/models.md#training-sessions) ID for accessing logs, metrics, artifacts |
| `dataset_id` | `dataset.id` | [Dataset](../datasets/index.md) identifier for reproducing training data |
| `dataset` | `dataset.name` | Human-readable dataset name |

### Example Traceability Workflow

Given a deployed model, you can trace back to its origins:

```python
# Extract metadata from deployed model
metadata = get_edgefirst_metadata(model_path)

# Construct EdgeFirst Studio URLs
studio_server = metadata['host']['studio_server']  # e.g., 'test.edgefirst.studio'
project_id = metadata['host']['project_id']        # e.g., '1123'
session = metadata['host']['session']              # e.g., 't-2110'
dataset_id = metadata['dataset']['id']             # e.g., 'ds-1c8'

# Note: Studio URL parameters require integer IDs. Metadata stores hex values
# with prefixes (t-, ds-). Convert by stripping the prefix and parsing as hex:
#   't-2110' -> int('2110', 16) -> 8464
#   'ds-1c8' -> int('1c8', 16)  -> 456

# Access training session: https://{studio_server}/{project_id}/experiment/training/details?train_session_id={session_int}
# Example: https://test.edgefirst.studio/1123/experiment/training/details?train_session_id=8464

# Access dataset: https://{studio_server}/{project_id}/datasets/gallery/main?dataset={dataset_int}
# Example: https://test.edgefirst.studio/1123/datasets/gallery/main?dataset=456

# View training logs, metrics, and original configuration
```

This enables:

- **Audit trails** for regulatory compliance
- **Debugging** production issues by examining [training data](../datasets/index.md)
- **Reproducibility** by re-running [training](training/vision.md) with identical configuration
- **Version control** of model lineage through [Model Experiments](../studio/models.md)

---

## Reading Metadata

### TFLite Models

TFLite models are ZIP-format files containing embedded `edgefirst.json` and `labels.txt`:

```python
import zipfile
import json
from typing import Optional, List

def get_edgefirst_metadata(model_path: str) -> Optional[dict]:
    """Extract EdgeFirst metadata from a TFLite model."""
    if not zipfile.is_zipfile(model_path):
        return None

    with zipfile.ZipFile(model_path) as zf:
        if 'edgefirst.json' in zf.namelist():
            with zf.open('edgefirst.json') as f:
                return json.loads(f.read().decode('utf-8'))
    return None

def get_labels(model_path: str) -> List[str]:
    """Extract class labels from a TFLite model."""
    if not zipfile.is_zipfile(model_path):
        return []

    with zipfile.ZipFile(model_path) as zf:
        if 'labels.txt' in zf.namelist():
            with zf.open('labels.txt') as f:
                content = f.read().decode('utf-8').strip()
                return [line for line in content.splitlines()
                        if line.strip()]
    return []
```

### ONNX Models

ONNX models store metadata directly in the model's custom properties:

```python
import onnx
import json
from typing import Optional, List

def get_edgefirst_metadata(model_path: str) -> Optional[dict]:
    """Extract EdgeFirst metadata from an ONNX model."""
    model = onnx.load(model_path)

    for prop in model.metadata_props:
        if prop.key == 'edgefirst':
            return json.loads(prop.value)
    return None

def get_labels(model_path: str) -> List[str]:
    """Extract class labels from an ONNX model."""
    model = onnx.load(model_path)

    for prop in model.metadata_props:
        if prop.key == 'labels':
            return json.loads(prop.value)
    return []

def get_quick_metadata(model_path: str) -> dict:
    """Get commonly-used fields without parsing full config."""
    model = onnx.load(model_path)

    result = {}
    quick_fields = ['name', 'description', 'author', 'studio_server',
                    'session_id', 'dataset', 'dataset_id']

    for prop in model.metadata_props:
        if prop.key in quick_fields:
            result[prop.key] = prop.value
        elif prop.key == 'labels':
            result['labels'] = json.loads(prop.value)

    return result
```

### ONNX Runtime Access

For inference applications using ONNX Runtime:

```python
import onnxruntime as ort
import json

session = ort.InferenceSession(model_path)
metadata = session.get_modelmeta()

# Access custom metadata
custom = metadata.custom_metadata_map
edgefirst_config = json.loads(custom.get('edgefirst', '{}'))
labels = json.loads(custom.get('labels', '[]'))

# Access official ONNX fields
print(f"Producer: {metadata.producer_name}")  # 'EdgeFirst ModelPack'
print(f"Graph: {metadata.graph_name}")
print(f"Description: {metadata.description}")
```

---

## Metadata Schema

The EdgeFirst metadata schema is organized into logical sections. All sections are optional — third-party integrations can include only the sections relevant to their use case — except `schema_version`, which is required on v2 metadata.

### Complete Schema Structure

```yaml
# Schema Version (required)
schema_version: 2

# Traceability & Identification
host:
  studio_server: string    # Full EdgeFirst Studio hostname (e.g., test.edgefirst.studio)
  project_id: string       # Project ID for Studio URLs
  session: string          # Training session ID
  organization: string     # Organization that initiated training

dataset:
  name: string             # Human-readable dataset name
  id: string               # Dataset identifier
  classes: [string]        # List of class labels

# Model Identification (from training session)
name: string               # Model/session name
description: string        # Model description
author: string             # Organization (typically "Au-Zone Technologies")

# Model Configuration (see ModelPack and Ultralytics documentation)
input:
  shape: [int]             # Input tensor shape (NCHW or NHWC depending on model)
  cameraadaptor: string    # Camera format (rgb, bgr, rgba, bgra, grey, yuyv)
  input_channels: int      # Channels from camera (3=RGB, 4=RGBA, 1=grey)
  output_channels: int     # Channels after CameraAdaptor transform

model:
  name: string             # Model/session name from training (artifact naming)
  version: string          # Training framework version (e.g., "8.4.9+edgefirst-1.4.2")
  task: string             # Training task: detection, segmentation, pose, classify
  backbone: string         # Backbone architecture (e.g., cspdarknet19, cspdarknet53)
  size: string             # Size variant (nano, small, medium, large, xlarge)
  activation: string       # Activation function (relu, relu6, silu)
  detection: boolean       # Detection task enabled
  segmentation: boolean    # Segmentation task enabled
  classification: boolean  # Classification task enabled
  anchors: [[[int, int]]]  # Anchor boxes per output level
  end2end: boolean         # True when NMS is embedded in the model graph (YOLO26 end-to-end, appended NMS)
  # ... additional model-specific parameters

# Training Configuration
trainer:
  epochs: int
  batch_size: int
  weights: string
  checkpoint_path: string

optimizer:
  optimizer: string
  learning_rate: float
  weight_decay: float

augmentation:
  random_hflip: int
  random_mosaic: int

validation:
  iou: float
  score: float
  nms: string
  normalization: string
  preprocessing: string
  skip_validation_steps: int

export:
  export: boolean
  export_input_type: string
  export_output_type: string
  calibration_samples: int

# Decoder Configuration (Ultralytics only)
decoder_version: string    # YOLO architecture version: yolov5, yolov8, yolo11, yolo26
nms: string                # HAL decoder NMS mode: class_agnostic, class_aware

# Calibration Artifact (see Calibration Artifact section)
calibration: string          # Snapshot filename: calibration-{dataset_id}-{param_hash}.safetensors

# Tiling (tile-trained models only — see Tiling section)
tiling:
  version: int                 # Section version (1)
  mode: string                 # tiled | whole_frame (how the runtime feeds frames)
  tile: [int, int]             # Runtime tile [H, W]; equals the input H, W in tiled mode
  grid: {algorithm: string, version: int, min_overlap: float}
  fit: string                  # letterbox
  pad: [int, int, int]
  per_tile: {nms: string, iou: float, score: float}
  merge: {mode: string, metric: string, threshold: float, class_agnostic: boolean, max_det: int}
  full_frame: {enabled: boolean, own_above_area: float}
  training: {session: string, sampler: string, version: string, params: object}
  export: {session: string, weights_from: string, calibration: {resize: string, input_shape: [int, int], full_frame: boolean}}

# Split Hints — INPUT metadata only, present in uncompiled ONNX/SavedModel.
# The compiled (converted) model REPLACES split_hints with the outputs[] array.
split_hints:
  - type: string                 # Hint type (e.g., "quantization_split")
    target: string               # Output tensor name this hint applies to
    input_dtype: string          # Suggested input quantization dtype
    output_dtype: string         # Suggested output quantization dtype
    description: string          # Human-readable purpose
    strides: [int]               # FPN strides (optional; declares spatial structure)
    anchors_per_cell: int        # Anchor count per cell (optional; default 1)
    boundaries:                  # Channel boundaries within the target tensor
      - name: string             #   Boundary region name
        channels: [int, int]     #   Channel range [start, end) (exclusive end)
        activation: string       #   Post-activation (sigmoid, softmax, tanh; optional)

# Converter Traceability (see Converter Traceability section)
# Converter-specific sections are added at the top level by each converter
# Examples: "neutron": {...}, "ara2": {...}, "tflite_quantizer": {...}

# Output Specification — Two-Layer Logical/Physical Model
outputs:
  - name: string               # Logical output name
    type: string               # Semantic type: boxes, scores, objectness, mask_coefs, protos,
                               # landmarks, classes, detections, segmentation, masks, detection
    shape: [int]               # Reconstructed logical shape (what fallback dequant+merge produces)
    dshape:                    # Named dimensions (see dshape section)
      - batch: int
      - height: int
      - width: int
      - num_features: int
      - num_boxes: int
      - num_classes: int
      - num_protos: int
      - num_anchors_x_features: int
      - box_coords: int
      - padding: int
    decoder: string            # 'modelpack' | 'ultralytics' — required for outputs needing decode
    encoding: string           # 'dfl' | 'direct' | 'anchor' — required on boxes
    score_format: string       # 'per_class' | 'obj_x_class' (scores only)
    normalized: boolean        # Coordinates in [0,1] (true) or pixels (false); boxes and detections only
    stride: int or [int, int]  # Spatial stride; 2-element form for non-square inputs
    anchors: [[float, float]]  # Normalized anchors (ModelPack anchor-based outputs)

    # When the converter did NOT further split this logical output,
    # it IS the physical tensor — the following fields are present directly:
    dtype: string              # Tensor data type (e.g. int8, uint8, float32)
    quantization:              # Quantization parameters (null for float models)
      scale: float or [float]
      zero_point: int or [int]
      axis: int
      dtype: string

    # When the converter split this logical output, 'outputs' contains the
    # physical children. One level of nesting only.
    # Physical children are a quantization concept — splitting minimizes
    # quantization error by giving each sub-tensor its own scale/zero_point.
    # Float models do not need physical children since there is no
    # quantization error to manage.
    outputs:
      - name: string           # Physical tensor name (as produced by the converter)
        type: string           # Semantic type (matches parent, or more specific e.g. boxes_xy)
        shape: [int]           # Physical tensor shape
        dshape: [...]          # Named dimensions for the physical shape
        dtype: string          # Tensor data type (e.g. int8, uint8, float32)
        quantization:          # Per-tensor {scale, zero_point}; always present (null for float models)
          scale: float or [float]
          zero_point: int or [int]
          axis: int
          dtype: string
        stride: int or [int, int]  # FPN stride for this child; 2-element form for non-square inputs
        scale_index: int       # 0-based index into strides array (per-scale splits)
        activation_applied: string   # Activation fused by NPU; HAL must NOT re-apply
        activation_required: string  # Activation NOT fused; HAL must apply
```

---

## Output Specification

The `outputs` section is critical for inference — it tells the runtime how to interpret model outputs. Schema v2 introduces a **two-layer model** that separates the logical contract (what the model produces semantically) from the physical realization (what tensors the converter actually emitted).

### Two-Layer Output Model

Each entry in the top-level `outputs[]` array is a **logical output**. A logical output either IS a physical tensor (when the converter did not split it further) or contains an `outputs[]` array of **physical children** that realize it.

**Rules:**

- Logical outputs always carry a `shape` field — the reconstructed shape the HAL obtains from the fallback dequantize+merge path.
- Each physical child self-describes with its own `name`, `shape`, `dshape`, `dtype`, and `quantization`.
- Only **one level** of nesting is permitted (logical → physical). No deeper.
- Semantic and decode fields (`decoder`, `encoding`, `score_format`, `normalized`) live on the logical output only — never on physical children.
- Physical-tensor fields (`dtype`, `quantization`, `activation_applied`, `activation_required`, `scale_index`) live on the physical level. When a logical output has no children, it carries them directly because it IS the physical tensor.

```yaml
# Logical output with no split — IS the physical tensor
- name: scores
  type: scores
  shape: [1, 80, 8400]
  dshape:
    - batch: 1
    - num_classes: 80
    - num_boxes: 8400
  dtype: int8
  quantization: {scale: 0.00392, zero_point: 0, dtype: int8}
  decoder: ultralytics

# Logical output split into per-scale physical children
- name: boxes
  type: boxes
  shape: [1, 64, 8400]
  encoding: dfl
  decoder: ultralytics
  normalized: true
  outputs:
    - name: boxes_0
      type: boxes
      stride: 8
      scale_index: 0
      shape: [1, 80, 80, 64]
      dshape:
        - batch: 1
        - height: 80
        - width: 80
        - num_features: 64
      dtype: uint8
      quantization: {scale: 0.0234, zero_point: 128, dtype: uint8}
    # ... boxes_1 (stride 16), boxes_2 (stride 32)
```

### Output Types

Logical output types used across frameworks:

| Type | Description | Typical Shape (logical) |
| ---- | ----------- | ----------------------- |
| `boxes` | Bounding box coordinates | `[1, 4, num_boxes]` or `[1, reg_max×4, num_boxes]` for DFL |
| `scores` | Per-class or class-aggregate scores | `[1, num_classes, num_boxes]` |
| `objectness` | Objectness scores (YOLOv5-style `obj_x_class`) | `[1, anchors_per_cell, num_boxes]` |
| `classes` | End-to-end class indices | `[1, num_boxes, 1]` |
| `mask_coefs` | Mask coefficients for instance segmentation | `[1, num_protos, num_boxes]` |
| `protos` | Instance segmentation prototypes | `[1, num_protos, H, W]` |
| `landmarks` | Facial / keypoint landmarks | `[1, num_landmarks, num_boxes]` |
| `detections` | Fully decoded post-NMS detections (end-to-end) | `[1, max_det, 6]` (x1,y1,x2,y2,conf,class) |
| `segmentation` | Semantic segmentation output (ModelPack) | `[1, H, W, num_classes]` |
| `masks` | Semantic segmentation masks (ModelPack) | `[1, H, W]` |
| `detection` | ModelPack anchor-grid raw output requiring anchor decode | `[1, H, W, anchors×features]` |

Physical-child subtypes (appear only inside `outputs[]` children):

| Subtype | When Used | Description |
| ------- | --------- | ----------- |
| `boxes_xy` | ARA-2 channel sub-split | xy coordinates split for independent INT16 quantization |
| `boxes_wh` | ARA-2 channel sub-split | wh coordinates split for independent INT16 quantization |
| *(same as parent)* | Per-scale split | Each FPN scale produces one child with the parent's type |

### The `dshape` Field

The `dshape` field provides **named dimensions** for each axis, making tensor shapes self-describing. Consumers resolve axes like `height` or `num_classes` by name rather than by position, which matters because ONNX uses NCHW and TFLite uses NHWC — the same dimension lives at a different index depending on format. `dshape` applies to both logical and physical outputs; each level describes its own shape.

```yaml
# Logical-level dshape
outputs:
  - name: output0
    shape: [1, 84, 8400]       # Raw shape
    dshape:                    # Named dimensions as ordered array
      - batch: 1
      - num_features: 84       # 4 box coords + 80 classes
      - num_boxes: 8400
```

**Standard dimension names:**

| Name | Description |
| ---- | ----------- |
| `batch` | Batch size (typically 1 for inference) |
| `height` | Spatial height |
| `width` | Spatial width |
| `num_classes` | Number of classification classes |
| `num_features` | Feature dimension (box coords + classes + mask coefficients) |
| `num_boxes` | Number of detection boxes/anchors |
| `num_protos` | Number of prototype masks (instance segmentation) |
| `num_anchors_x_features` | Combined anchor × features-per-anchor dimension (ModelPack grid outputs) |
| `padding` | Padding/alignment dimension used to satisfy expected tensor shapes. Must always be 1 |
| `box_coords` | The coordinates of the boxes. Must be 4 |

`dshape` entries are ordered objects — the position of each key matches the axis position in `shape`. Ordering is authoritative for consumers mapping shapes to names.

### Box Encoding

The `encoding` field on a `boxes` logical output tells the HAL how to interpret the raw channel data after dequantization.

| Value | Channels | Description | Decode Step |
| ----- | -------- | ----------- | ----------- |
| `dfl` | `reg_max × 4` (typically 64) | Distribution Focal Loss encoding. Each coordinate is a probability distribution over `reg_max` bins. | Softmax over each `reg_max` group, then weighted sum → 4 coordinates. Common in YOLOv8, YOLO11. |
| `direct` | 4 | Direct coordinate values — already decoded. | Dequantize only. Common in YOLO26 (reg_max=1), ARA-2 post-split. |
| `anchor` | `anchors_per_cell × 4` | Anchor-based grid offsets. Each group of 4 is (tx, ty, tw, th) requiring sigmoid + anchor-scale transform. | Sigmoid + anchor transform per grid cell. Common in YOLOv5, SSD MobileNet, ModelPack. |

`encoding` is required on all `boxes` outputs in v2.

### Score Format

The `score_format` field on a `scores` logical output disambiguates YOLOv5's `obj_x_class` encoding from the default per-class encoding used by YOLOv8/v11/v26:

| Value | Description | Architecture |
| ----- | ----------- | ------------ |
| `per_class` | Each anchor outputs `[nc]` class probabilities directly | YOLOv8, YOLO11, YOLO26, default |
| `obj_x_class` | Each anchor outputs `[nc]` class probabilities; a separate `objectness` logical output provides `[1]` per anchor. Final detection confidence = `objectness × class_score` per anchor | YOLOv5 |

When `score_format` is `obj_x_class`, the model produces a separate `objectness` logical output as a sibling of `scores` at the logical level.

### Decoding Information

The presence of a `decoder` field on a logical output signals that post-processing is required. Outputs consumed directly (e.g., `protos`) may omit `decoder`.

```yaml
- name: boxes
  type: boxes
  shape: [1, 64, 8400]
  encoding: dfl
  decoder: ultralytics      # Post-processing required
  normalized: true
  outputs: [...]            # Physical per-scale children

- name: protos
  type: protos
  shape: [1, 32, 160, 160]
  stride: 4
  dtype: int8
  quantization: {scale: 0.0156, zero_point: 0, dtype: int8}
  # No 'decoder' field — consumed directly
```

### Logical vs Physical Field Placement

Semantic and decode fields live on the **logical output** and apply to all children. Physical children carry only tensor-level fields.

**Root-level only:** `decoder_version`, `nms` (HAL NMS mode). These describe model-wide behavior and never appear inside an `outputs[]` entry.

**Logical output only:** `decoder`, `encoding`, `score_format`, `normalized`, `anchors`

**Physical output only:** `quantization` (always required), `dtype`, `scale_index`, `activation_applied`, `activation_required`

**Both levels:** `name`, `type`, `shape`, `dshape`, `stride`

When a logical output has no children, it also carries `dtype` and `quantization` directly — it IS the physical tensor.

Per-type semantic fields are scoped to their output type:

- `encoding` → `boxes` only
- `score_format` → `scores` only
- `normalized` → `boxes` and `detections` only
- `anchors` → `boxes` with `encoding: anchor` only
- `stride` on a non-split logical output → spatial stride hint (e.g. `protos` at stride 4)

---

## HAL Decoder Algorithm

The HAL uses the two-layer `outputs[]` structure to decode any converter's decomposition.

```text
For each logical output in outputs[]:
  if output has "outputs" children:
    # Converter split this logical output
    if HAL has optimized decoder for this (type, children types) combination:
      # Direct path: use quantized children directly
      decode_optimized(children)
    else:
      # Fallback: dequantize each child, reassemble into logical shape
      for child in children:
        dequantize(child) -> float32
      merge children -> logical tensor (concat along appropriate axis)
      decode_standard(logical_tensor)
  else:
    # No split — tensor IS the logical output
    dequantize(output) -> float32
    decode_standard(output)
```

### Merge Strategy

The `type` and `stride` fields on children tell the HAL which merge to perform:

- **Channel sub-splits** (e.g., `boxes_xy` + `boxes_wh`): Concat along the channel dimension. Children have no `stride` field. The concatenated result matches the logical output's `shape`.
- **Per-scale splits** (e.g., `boxes_0` + `boxes_1` + `boxes_2`): Children carry `stride` fields. Flatten each child's spatial dimensions to a single axis (`H×W`), concat along that axis, then reshape and transpose so the merged result matches the logical output's `shape` and `dshape`. The `dshape` named dimensions on both the children and the logical parent disambiguate axis ordering (e.g., NCHW vs NHWC), so no layout assumptions are hard-coded.

The HAL infers the merge strategy from child fields: presence of `stride` → spatial merge; absence → channel merge.

### Direct Path Examples

| Target | Logical Type | Children Types | Direct Decoder |
| ------ | ------------ | -------------- | -------------- |
| ARA-2 | `boxes` | `boxes_xy`, `boxes_wh` | `box_assembly` — INT16 dequant + dist2bbox in one pass |
| Hailo | `scores` | `scores` ×3 (per-scale) | Per-scale sigmoid already applied, just spatial concat |

### Fallback Path

The fallback always works for any decomposition:

1. Dequantize each child to float32 using its `quantization` parameters.
2. Merge using the inferred strategy.
3. The result is a float32 tensor matching the logical output's `shape`.
4. Pass to the standard decoder pipeline.

---

## Quantization Parameters

Quantized models store integer values instead of floats. Each output tensor includes parameters to convert back to floating-point using the dequantization formula:

```text
real_value = scale * (quantized_value - zero_point)
```

EdgeFirst supports two quantization granularities and two quantization modes:

- **Per-tensor**: A single scale (and optional zero_point) applies to the entire tensor
- **Per-channel** (per-axis): Each slice along a specified axis has its own scale (and optional zero_point)
- **Symmetric**: The quantized range is centered on zero; `zero_point` is 0 and can be omitted
- **Asymmetric** (affine): The quantized range is offset; `zero_point` shifts the range so floating-point 0.0 is exactly representable

For detailed specifications, see the [ONNX QuantizeLinear operator](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html) and [LiteRT 8-bit quantization specification](https://ai.google.dev/edge/litert/conversion/tensorflow/quantization/quantization_spec).

### Quantization Object Schema

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `scale` | float or \[float\] | Yes | Scale factor(s). Scalar = per-tensor, array = per-channel |
| `zero_point` | int or \[int\] | No | Zero point offset(s). Omit for symmetric quantization (implies 0) |
| `axis` | int | When per-channel | Tensor dimension index that the scale/zero_point arrays correspond to |
| `dtype` | string | Yes | Quantized data type: `int8`, `uint8`, `int16`, `uint16`, `float16` |

**Rules:**

- When `scale` is a scalar: per-tensor quantization
- When `scale` is an array: per-channel quantization; `axis` is required; array length must equal `tensor.shape[axis]`
- When `zero_point` is absent: symmetric quantization (zero_point = 0)
- When `zero_point` is present: asymmetric (affine) quantization
- `quantization: null` means the tensor is not quantized (float model)

### Examples

```yaml
# Per-tensor symmetric
quantization:
  scale: 0.176
  dtype: int8

# Per-tensor asymmetric
quantization:
  scale: 0.176
  zero_point: 198
  dtype: uint8

# Per-channel symmetric
quantization:
  scale: [0.054, 0.089, 0.195]
  axis: 0
  dtype: int8

# Per-channel asymmetric
quantization:
  scale: [0.054, 0.089, 0.195]
  zero_point: [10, 12, 8]
  axis: 0
  dtype: uint8

# Float model (not quantized)
quantization: null
```

### Dequantization Code

```python
import numpy as np

def dequantize(raw_output: np.ndarray, quantization: dict) -> np.ndarray:
    """Dequantize a quantized tensor using EdgeFirst metadata."""
    scale = np.array(quantization['scale'], dtype=np.float32)
    zero_point = np.array(quantization.get('zero_point', 0))

    # For per-channel: reshape scale/zero_point to broadcast along axis
    if scale.ndim > 0 and 'axis' in quantization:
        shape = [1] * raw_output.ndim
        shape[quantization['axis']] = -1
        scale = scale.reshape(shape)
        zero_point = zero_point.reshape(shape)

    return (raw_output.astype(np.float32) - zero_point) * scale
```

### Framework Conventions

| Framework | Per-Tensor | Per-Channel | Symmetric | Axis Field |
| --------- | ---------- | ----------- | --------- | ---------- |
| ONNX | Scalar scale | 1-D scale + `axis` | Implicit (zero_point=0) | `axis` (default 1) |
| TFLite/LiteRT | Scalar (1-element array) | 1-D scale + `quantized_dimension` | Implicit (zero_point=0 for weights) | `quantized_dimension` |
| TensorRT | Scalar scale | Per-channel scale | Always symmetric | Output channel axis |
| PyTorch | Scalar scale | 1-D scale + `axis` | Explicit `qscheme` enum | `axis` parameter |

### Target-Specific Term Mapping

Some NPU toolchains use different terminology internally. Converters translate at the boundary — the compiled `edgefirst.json` always uses the standard terms above.

**Kinara ARA-2** (ioparams.json, qmode 9 — asymmetric):

| Kinara term | edgefirst.json term | Notes |
| ----------- | ------------------- | ----- |
| `outputScale` / `outputQn` | `scale` | Identical value for qmode 9. For symmetric qmodes (0–3), Kinara's `qn` is 1/scale — but the ARA-2 converter always uses qmode 9 |
| `offset` | `zero_point` | Identical value |
| `bpp` + `isSigned` | `dtype` | `bpp=1, signed` → `int8`, `bpp=2, unsigned` → `uint16`, etc. |

**Hailo** (HEF quantization info):

| Hailo term | edgefirst.json term |
| ---------- | ------------------- |
| `qp_scale` | `scale` |
| `qp_zp` | `zero_point` |

---

## Data Layout (NCHW vs NHWC)

Deep learning frameworks use different memory layouts for tensor data. The metadata accurately reflects each format's native layout:

| Format | Data Layout | Shape Convention | Example (batch=1, 640x640, RGB) |
| ------ | ----------- | ---------------- | ------------------------------- |
| TFLite | **NHWC** | `[batch, height, width, channels]` | `[1, 640, 640, 3]` |
| ONNX | **NCHW** | `[batch, channels, height, width]` | `[1, 3, 640, 640]` |

### Why This Matters

- **TFLite** (TensorFlow): Uses channels-last (NHWC) which is optimized for CPU and mobile inference
- **ONNX** (PyTorch-derived): Uses channels-first (NCHW) which is optimized for GPU and NPU inference

The metadata's `outputs` section reports shapes in the model's native format. When integrating with inference runtimes, ensure your input preprocessing matches the expected layout. The `dshape` field lets consumers look up dimensions by name rather than relying on positional assumptions that differ between layouts.

### Metadata Fields

```yaml
input:
  shape: [1, 640, 640, 3]  # Input tensor shape (layout varies by model)
  cameraadaptor: rgb       # Channel order (rgb, bgr, yuyv)
  # Common layouts:
  # - NHWC: [batch, height, width, channels] e.g., [1, 640, 640, 3]
  # - NCHW: [batch, channels, height, width] e.g., [1, 3, 640, 640]

outputs:
  - name: output_0
    shape: [1, 640, 640, 3]   # TFLite: NHWC
    # shape: [1, 3, 640, 640] # ONNX: NCHW
```

---

## Input Preprocessing

EdgeFirst models expect specific input preprocessing. The metadata documents these requirements so inference pipelines can prepare data correctly.

### Image Resizing

Models expect input images at the resolution specified in metadata. How images are resized depends on the training approach:

```yaml
input:
  shape: [1, 640, 640, 3]  # NHWC example: [batch, height, width, channels]
  # shape: [1, 3, 640, 640]  # NCHW example: [batch, channels, height, width]
  cameraadaptor: rgb       # Expected color format
```

**Native Aspect Ratio (typical for purpose-built datasets):**

- [ModelPack](modelpack/index.md) models are often trained at the camera's native aspect ratio
- Images are directly resized to target dimensions without padding
- Best accuracy when deployment camera matches training data

**Letterbox (typical for diverse datasets like [COCO](../datasets/coco/index.md)):**

- Used when training on images from diverse cameras and aspect ratios
- Image is scaled to fit within target size while maintaining aspect ratio
- Gray padding (value 114) added to reach exact dimensions
- Inference must apply same letterbox transform and account for padding offset in output coordinates

**Example:** A 1920x1080 image letterboxed to 640x640:

- Scaled to 640x360 (maintains 16:9 ratio)
- 140 pixels of padding added to top and bottom
- Output box coordinates must be adjusted to remove padding offset

### Pixel Normalization

Input pixels are normalized from `[0, 255]` to `[0.0, 1.0]`:

```python
# Standard normalization
normalized = pixels.astype(np.float32) / 255.0
```

For quantized models (INT8), the quantization parameters handle the scaling internally — raw uint8 pixel values can often be used directly.

### Camera Adaptor

The `cameraadaptor` field specifies the expected input format for the model. See [Camera Adaptor](cameraadaptor.md) for details on how this enables models to consume native camera formats without runtime conversion.

| Value | Description | Channel Order |
| ----- | ----------- | ------------- |
| `rgb` | Standard RGB | Red, Green, Blue |
| `bgr` | OpenCV default | Blue, Green, Red |
| `rgba` | RGB with alpha | Red, Green, Blue, Alpha |
| `bgra` | BGR with alpha | Blue, Green, Red, Alpha |
| `grey` | Greyscale | Single channel |
| `yuyv` | YUV 4:2:2 packed | For direct camera sensor input |

---

## Tiling

Models trained on native-resolution tiles of high-resolution frames carry an optional `tiling` section. A runtime reads it to decide whether to cut each frame into tiles or run the whole frame through the model, and it records how the model was trained, exported and calibrated. A model without the section is not tile-trained and is handled exactly as before.

The tiling mode and the input resolution are fixed when the model is exported, because edge runtimes compile a static input shape. Trainers export a tile-trained model **tiled** at its tile size by default. The contract defines one workflow for deploying the same weights at another resolution, for example whole-frame at a camera's native resolution: it is done by starting a new training session with training disabled, selecting the tile-trained session as its weights source, and choosing the deployment mode and input resolution. That session exports and calibrates at the new geometry without retraining.

### Tiling Schema

```yaml
tiling:
  version: 1
  mode: tiled                    # tiled | whole_frame
  tile: [640, 640]               # runtime tile [H, W]
  grid: {algorithm: evendist, version: 1, min_overlap: 0.1}
  fit: letterbox
  pad: [114, 114, 114]
  per_tile: {nms: class_aware, iou: 0.5, score: 0.001}
  merge: {mode: keep_best, metric: ios, threshold: 0.5, class_agnostic: false, max_det: 300}
  full_frame: {enabled: false, own_above_area: 0.02}
  training:
    session: t-1a2b
    sampler: edgefirst-tiling
    version: "3.0"
    params: {tile_size: [640, 640], windows_per_frame: 4, seed: 0}
  export:
    session: t-1a2b
    calibration: {resize: tiled, input_shape: [640, 640], full_frame: false}
```

In version 1 every key shown above is required, except `export.weights_from` and the contents of `training.params`. Values in parentheses below are the values trainers write; they are not defaults that a runtime fills in for missing keys.

| Field | Type | Description |
| ----- | ---- | ----------- |
| `version` | int | Section version. The current version is `1`. A runtime that finds a version it does not support must warn and treat the model as not tile-trained. |
| `mode` | string | `tiled`: the runtime cuts each frame into a grid of `tile`-sized crops, runs each, and merges the detections. `whole_frame`: the runtime letterboxes the whole frame into the model input and runs it once. |
| `tile` | [int, int] | Runtime tile `[H, W]` in pixels. In `tiled` mode it equals the input height and width. |
| `grid.algorithm` | string | `evendist`: tile origins spread evenly from 0 to `frame − tile` per axis, so every seam overlaps by at least `min_overlap` and no tile is shifted. See [Grid](#grid). |
| `grid.version` | int | Grid algorithm version (`1`). |
| `grid.min_overlap` | float | Minimum overlap between neighbouring tiles as a fraction of the tile, `0 ≤ min_overlap < 1` (`0.1`). |
| `fit` | string | How a crop smaller than the tile is placed. Version 1 defines only `letterbox`: aspect preserved, content centred, padded with `pad` (see [Grid](#grid)). |
| `pad` | [int, int, int] | Letterbox pad colour, three integers from 0 to 255 (`114` per channel). |
| `per_tile.nms` | string | NMS applied to each tile's detections before merging: `class_aware`, `class_agnostic`, or `none` for end-to-end models. |
| `per_tile.iou` / `per_tile.score` | float | Per-tile NMS IoU threshold (`0.5`) and score floor (`0.001`), each from 0 to 1. |
| `merge.mode` | string | Cross-tile merge: `keep_best` keeps the highest-scoring box of each group unchanged; `union` replaces the group with its enclosing box. See [Merge](#merge). |
| `merge.metric` | string | `ios` (intersection over the smaller box, which matches objects cut by a tile seam) or `iou`. |
| `merge.threshold` | float | Overlap at which two boxes of the same class (or any class if `class_agnostic`) are merged, from 0 to 1 (`0.5`). |
| `merge.class_agnostic` | boolean | Merge across classes (`false`). |
| `merge.max_det` | int | Maximum detections per frame after merging, a positive integer (`300`). |
| `full_frame` | object | Extra whole-frame pass merged with the tiles: `enabled` (boolean, `false`) and `own_above_area`, a fraction of the frame area from 0 to 1 above which whole-frame boxes replace overlapping tile boxes (`0.02`). In the pass the whole frame is letterboxed into the tile. `enabled` may be `true` only in `tiled` mode. |
| `training` | object | How the weights were trained: the training `session`, the `sampler` and its `version`, and its parameters as trained. Written once by the session that trained the weights and copied unchanged by every later export. |
| `export` | object | How this model was produced: the exporting `session`, `weights_from` (the session whose weights were loaded, omitted when the same session trained and exported), and the `calibration` geometry: `resize`, `input_shape`, and `full_frame`, which is `true` when the snapshot also holds whole-frame samples (see [Tiling Rules](#tiling-rules)). |

### Grid

The `evendist` version 1 grid is computed per axis, for a frame length `L` and a tile length `T` in pixels, identically on every runtime:

1. If `L ≤ T`, the axis has a single origin `0` and the crop covers the whole axis.
2. Otherwise let `last = L − T`, `step = max(1, ⌊(1 − min_overlap) × T⌋)` and `n = ⌈last / step⌉`. `min_overlap` is first rounded to a 32-bit float, then `step` is evaluated in 64-bit floating point; `n` is an integer division rounded up. The origins are `oᵢ = round(i × last / n)` for `i = 0 … n`, with `i`, `last` and `n` converted to 32-bit floats, the product and quotient evaluated in 32-bit floating point, and the result rounded half away from zero. The first origin is `0` and the last is `last`.

A 3840-pixel axis with a 640-pixel tile and `min_overlap: 0.1` gives `step = 575` (0.1 as a 32-bit float is slightly larger than 0.1), `n = 6` and origins 0, 533, 1067, 1600, 2133, 2667, 3200. A 2160-pixel axis gives origins 0, 507, 1013, 1520.

The tiles are every pair of a row origin and a column origin, in row-major order: rows top to bottom, and within a row the columns left to right. A tile's index is its position in this order. Each crop is `min(T, L)` pixels along each axis, so crops are full tiles except on an axis shorter than the tile. Such a crop is letterboxed: scaled by the largest factor that fits it in the tile with its aspect ratio kept, the scaled size rounded half away from zero (at least 1 pixel), placed at offset `⌊(tile − scaled) / 2⌋` on each axis, and the rest filled with `pad`.

### Merge

Each tile's detections are filtered with `per_tile` NMS, mapped back into frame pixels in 32-bit floating point, and concatenated in tile-index order. The merge then groups them greedily:

1. Sort the detections by score, highest first. Equal scores keep their concatenated order.
2. Walk the sorted list. Each detection not yet claimed is kept, and claims every later unclaimed detection of the same class (any class if `class_agnostic`) whose overlap with it, by `metric`, is at least `threshold`. `ios` is the intersection divided by the smaller box's area and `iou` the intersection over the union, each with the denominator floored at `1e-9`.
3. A detection is compared only with the kept detection that claims it; grouping is not transitive. If A claims B, and C overlaps B but not A, C stays unclaimed and is considered in its own turn.
4. `keep_best` emits the kept detection unchanged. `union` emits the box enclosing the kept detection and everything it claimed, with the kept detection's score and class.
5. The output is the emitted detections in the order they were kept, truncated to `max_det`.

### Tiling Modes

| | `tiled` | `whole_frame` |
| - | ------- | ------------- |
| Model input | The tile, e.g. `640×640` | The export resolution, e.g. `3840×2176` for 4K frames (height and width are multiples of 32) |
| Runtime | Grid of tiles per frame, per-tile NMS, merge into frame coordinates | One inference per frame on the letterboxed frame |
| Calibration snapshot | Deployment-grid tiles at native scale (`resize: tiled`), plus whole-frame samples when `full_frame.enabled` | Frames letterboxed or stretched to the export resolution (`resize: letterbox` or `stretch`) |
| When to use | High-resolution cameras on accelerators that cannot fit the whole frame, and the default for tile-trained models | The accelerator fits the whole frame; usually faster than tiling the same frame |

Both modes use the same weights, because the detectors are fully convolutional and were trained at native scale.

### Tiling Rules

1. In `tiled` mode the input height and width equal `tile`. The tile may differ from the training tile (`training.params.tile_size`), because objects are still seen at native scale.
2. In `whole_frame` mode the input is the export resolution, with height and width multiples of 32.
3. `export.calibration.resize` is `tiled` in `tiled` mode and `letterbox` in `whole_frame` mode, `export.calibration.input_shape` equals the input height and width, and `export.calibration.full_frame` equals `full_frame.enabled`. See [Calibration Snapshot](conversion/calibration.md#geometry-check).
4. `training` is never modified after the session that trained the weights wrote it. `export` describes the most recent export.
5. Converters copy the `tiling` section unchanged; see [Converter Traceability](#converter-traceability).
6. Unknown keys are ignored.

### Example: Whole-Frame Re-Export

The weights trained tiled in session `t-1a2b`, re-exported whole-frame at 4K by export-only session `t-3c4d`:

```yaml
input:
  shape: [1, 3, 2176, 3840]
tiling:
  version: 1
  mode: whole_frame
  tile: [640, 640]
  grid: {algorithm: evendist, version: 1, min_overlap: 0.1}
  fit: letterbox
  pad: [114, 114, 114]
  per_tile: {nms: class_aware, iou: 0.5, score: 0.001}
  merge: {mode: keep_best, metric: ios, threshold: 0.5, class_agnostic: false, max_det: 300}
  full_frame: {enabled: false, own_above_area: 0.02}
  training:
    session: t-1a2b
    sampler: edgefirst-tiling
    version: "3.0"
    params: {tile_size: [640, 640], windows_per_frame: 4, seed: 0}
  export:
    session: t-3c4d
    weights_from: t-1a2b
    calibration: {resize: letterbox, input_shape: [2176, 3840], full_frame: false}
```

### Example: Tiled Re-Export at a New Tile Size

The same weights re-exported tiled at a 1280×1280 tile by export-only session `t-3c4e`, as a TFLite model with an NHWC input. The runtime tile differs from the 640×640 training tile, which rule 1 allows. This model has an end-to-end head, so `per_tile.nms` is `none`:

```yaml
input:
  shape: [1, 1280, 1280, 3]
tiling:
  version: 1
  mode: tiled
  tile: [1280, 1280]
  grid: {algorithm: evendist, version: 1, min_overlap: 0.1}
  fit: letterbox
  pad: [114, 114, 114]
  per_tile: {nms: none, iou: 0.5, score: 0.001}
  merge: {mode: keep_best, metric: ios, threshold: 0.5, class_agnostic: false, max_det: 300}
  full_frame: {enabled: false, own_above_area: 0.02}
  training:
    session: t-1a2b
    sampler: edgefirst-tiling
    version: "3.0"
    params: {tile_size: [640, 640], windows_per_frame: 4, seed: 0}
  export:
    session: t-3c4e
    weights_from: t-1a2b
    calibration: {resize: tiled, input_shape: [1280, 1280], full_frame: false}
```

### Models Without Tiling

A model that was not tile-trained has no `tiling` key. Its runtime behavior is unchanged: the runtime letterboxes each frame into the model input and runs it once, and tiled inference happens only when an application requests it explicitly.

!!! note "Session references"
    Session IDs in metadata use the `t-` prefix with a hexadecimal value, as elsewhere in this document. Tools that accept a session reference must also accept the decimal integer, with or without quotes: `t-2a3f`, `"10815"` and `10815` name the same session.

---

## Validation Parameters

The `validation` section records the recommended settings based on how the model was trained. These parameters are **informational preferences** — they document the model author's intended configuration for validation and inference.

!!! note "Two distinct `nms` fields"
    This document uses `nms` at two levels with different semantics:

    - **`validation.nms`** (this section) — selects the NMS *implementation* (`hal`, `numpy`, `tensorflow`, `torch`) or `none` for models with embedded NMS.
    - **root-level `nms`** (see [HAL NMS Field](#hal-nms-field)) — selects HAL decoder *behavior* (`class_agnostic` vs `class_aware`).

    The two fields are independent and can coexist. Keep the distinction in mind when reading the rest of this section.

### Parameter Semantics

| Parameter | Description | Default | Override at Runtime? |
| --------- | ----------- | ------- | -------------------- |
| `iou` | NMS IoU threshold | `0.7` | Yes |
| `score` | NMS confidence score threshold | `0.001` | Yes |
| `nms` | NMS algorithm | *(not set)* | See below |
| `normalization` | Input pixel normalization | `unsigned` | Yes |
| `preprocessing` | Image preprocessing method | `letterbox` | Yes |

Most parameters (`iou`, `score`, `normalization`, `preprocessing`, and NMS algorithm choices like `hal`/`tensorflow`/`numpy`/`torch`) can be overridden at runtime based on deployment preferences.

**Exception: `nms: none`** must be respected because the model does not produce outputs compatible with external NMS. This applies to two cases:

1. **Architectural end-to-end models** (e.g., YOLO26) — NMS is part of the model architecture via one-to-one matching heads. The model graph itself produces final predictions.
2. **Engine-embedded NMS** — Models exported with NMS operations appended to the inference graph (ONNX, TensorRT, TFLite). NMS is not part of the original model architecture but was added during export or conversion.

Both produce post-NMS output in `[x1, y1, x2, y2, conf, class, ...]` format. Detection models output `(1, max_det, 6)`. Segmentation models output `(1, max_det, 6 + nm)` plus prototype masks — the mask coefficients for NMS-selected detections are preserved, so only the mask decode step is needed externally (`mask = sigmoid(coefficients @ prototypes)`). Use `--nms none` (CLI) or `validation.nms: none` (metadata) for either case.

### Allowed `nms` Values

| Value | Description |
| ----- | ----------- |
| `none` | No external NMS. For models with embedded NMS — either architectural end-to-end (YOLO26) or engine-embedded (ONNX/TRT/TFLite with NMS ops appended). Supports both detection and segmentation |
| `numpy` | NumPy-based NMS implementation (default fallback) |
| `hal` | EdgeFirst HAL decoder NMS |
| `tensorflow` | TensorFlow NMS |
| `torch` | PyTorch (torchvision) NMS |

When `--override` is set, the validator reads `validation.nms` from the model metadata and applies it automatically.

### Box Coordinate Format (`normalized`)

The `normalized` field on `boxes` and `detections` outputs specifies the coordinate format:

| Value | Description | Coordinate Range |
| ----- | ----------- | ---------------- |
| `true` | Normalized coordinates relative to model input dimensions | `[0.0, 1.0]` |
| `false` | Pixel coordinates relative to model input (letterboxed frame) | `[0, width]` / `[0, height]` |

**Normalized coordinates are preferred** because they:

- Don't require knowledge of model input resolution for downstream processing
- Quantize better (smaller dynamic range)
- Work consistently across different model input sizes

**Pixel coordinates** are typically used by:

- End-to-end models with embedded NMS (YOLO26, engine-embedded NMS)
- Models exported with specific output coordinate conventions

!!! note
    Coordinates are always relative to the **letterboxed model input**, not the original image aspect ratio. The caller must apply the inverse letterbox transform to map boxes back to original image coordinates regardless of whether `normalized` is `true` or `false`.

```yaml
# End-to-end model with pixel coordinates
outputs:
  - name: output0
    type: detections
    shape: [1, 100, 6]       # [batch, max_det, x1+y1+x2+y2+conf+class]
    dshape:
      - batch: 1
      - num_boxes: 100
      - num_features: 6
    normalized: false         # Pixel coordinates
    decoder: ultralytics
```

---

## Post-Processing & Two-Layer Outputs

The two-layer `outputs[]` structure (introduced in [Output Specification](#output-specification)) is descriptive: converters declare the logical contract and — when they split the tensor further — describe the physical decomposition they produced. This section covers the post-processing decoder contract that consumers honor at inference time. For the layout of logical outputs per architecture, see [Architecture Survey](#architecture-survey).

### Decoding Flow

When a logical output has a `decoder` field set, the inference pipeline must:

1. **Run model inference** → Get quantized physical tensors
2. **Identify the logical output** → Each entry in `outputs[]`, with or without children
3. **Dequantize physical tensors** → Using each child's `quantization` (or the logical's own if no children)
4. **Reassemble into the logical tensor** → If the logical output has physical children, merge them per the rules in [HAL Decoder Algorithm — Merge Strategy](#merge-strategy) (channel concat for sub-splits, spatial concat for per-scale splits). If there are no children, the logical output IS the tensor.
5. **Apply decoder** → Framework-specific: anchor decode (`modelpack`), DFL/direct decode (`ultralytics`)
6. **Run NMS** → Unless the model has embedded NMS (`validation.nms: none`)

### Decoder Field

The `decoder` field specifies which decoding algorithm to use:

```yaml
outputs:
  - name: boxes
    type: boxes
    encoding: dfl
    decoder: ultralytics
```

#### `modelpack` — Anchor-Based YOLO Decoder

Used by [ModelPack](modelpack/index.md) models. Traditional YOLO-style grid decoding with pre-defined anchor boxes.

**Characteristics:**

- **Anchor-based**: Uses pre-defined anchor boxes per output level (3 anchors × 3 scales typical)
- **Grid outputs**: Raw features from detection grid cells
- **Sigmoid activations**: Applied to xy, wh, objectness, and class predictions

**Decoding formula:**

```python
xy = (sigmoid(xy) * 2.0 + grid - 0.5) * stride
wh = (sigmoid(wh) * 2) ** 2 * anchors * stride * 0.5
xyxy = concat([xy - wh, xy + wh]) / input_dims  # normalized xyxy
```

**Required metadata fields** (on the logical `detection` output):

```yaml
outputs:
  - type: detection
    decoder: modelpack
    encoding: anchor
    anchors:              # Required — normalized anchor boxes for this scale
      - [0.054, 0.065]
      - [0.089, 0.139]
    stride: [16, 16]      # Required — spatial stride
```

#### `ultralytics` — Anchor-Free DFL Decoder

Used by [Ultralytics](ultralytics/index.md) models (YOLOv5, YOLOv8, YOLO11, YOLO26). Modern anchor-free detection using Distribution Focal Loss (DFL).

**Characteristics:**

- **Anchor-free**: Uses anchor points (grid centers) instead of pre-defined boxes
- **DFL regression**: Converts 16-bin distribution to box coordinates (`encoding: dfl`)
- **Direct coordinates**: YOLO26 uses reg_max=1 for direct 4-channel output (`encoding: direct`)
- **Unified architecture**: Same decoder for YOLOv5, YOLOv8, YOLO11, YOLO26 — differences are captured by `encoding`, `score_format`, and `decoder_version`

**Decoding formula:**

```python
# DFL converts 16-bin distribution to coordinate value (encoding: dfl only)
box = dfl(raw_box)  # [batch, 64, anchors] -> [batch, 4, anchors]

# dist2bbox converts LTRB distances to boxes
x1y1 = anchor_points - lt
x2y2 = anchor_points + rb
# Returns xywh in pixel coordinates (ONNX float) or [0,1] normalized (TFLite INT8)
```

**Version differences** — all Ultralytics versions use the same anchor-free `Detect` class. Differences are in backbone architecture:

| Version | Backbone Blocks | Classification Head |
| ------- | --------------- | ------------------- |
| YOLOv5 | C3 | Conv→Conv→Conv2d |
| YOLOv8 | C2f | Conv→Conv→Conv2d |
| YOLO11 | C3k2, C2PSA | DWConv→Conv (efficient) |
| YOLO26 | C3k2, A2C2f | DWConv→Conv (efficient) |

### Decoder Version Field

The `decoder_version` field specifies the YOLO architecture version for Ultralytics models. This field is critical for determining the correct decoding strategy, especially for end-to-end models.

```yaml
decoder_version: yolo26    # End-to-end model with embedded NMS
# or
decoder_version: yolov8    # Traditional model requiring external NMS
```

**Supported values:**

| Value | Architecture | NMS Handling |
| ----- | ------------ | ------------ |
| `yolov5` | YOLOv5 | External NMS required |
| `yolov8` | YOLOv8 | External NMS required |
| `yolo11` | YOLO11 | External NMS required |
| `yolo26` | YOLO26 | Embedded NMS (end-to-end) |

!!! note "Naming Convention"
    The naming follows Ultralytics conventions: `yolov5` and `yolov8` include the 'v' prefix, while `yolo11` and `yolo26` do not (Ultralytics dropped the 'v' starting with YOLO11).

**When `decoder_version` is `yolo26` and `model.end2end: true`:**

- The model uses one-to-one matching heads with NMS embedded in the architecture
- Output format is `type: detections` with shape `[1, max_det, 6]` = `[x1, y1, x2, y2, conf, class]`
- The HAL decoder uses end-to-end model types regardless of the `nms` field
- No external NMS is applied

**When `decoder_version` is absent or any other value:**

- Traditional YOLO architecture requiring external NMS
- The root-level `nms` field controls which NMS algorithm the HAL decoder uses

### HAL NMS Field

The root-level `nms` field controls the HAL decoder's NMS behavior:

```yaml
nms: class_agnostic    # Suppress overlapping boxes regardless of class (default)
# or
nms: class_aware       # Only suppress boxes with the same class label
```

| Value | Behavior |
| ----- | -------- |
| `class_agnostic` | Suppress overlapping boxes regardless of class label (default) |
| `class_aware` | Only suppress boxes that share the same class AND overlap |

!!! warning "Two distinct `nms` fields"
    This document uses `nms` at two levels with different semantics:

    - **Root-level `nms`** (this field) — HAL decoder *behavior*: `class_agnostic` vs `class_aware`.
    - **`validation.nms`** (see [Validation Parameters](#validation-parameters)) — NMS *implementation*: `hal`, `numpy`, `tensorflow`, `torch`, or `none`.

    The two fields are independent and can coexist.

---

## Split Hints

Split hints encode model-specific knowledge about where natural quantization boundaries exist within output tensors. The training framework identifies these boundaries based on its knowledge of the model architecture; the converter decides whether to apply them and how far to decompose beyond them.

### Lifecycle

Split hints are **input metadata only**. They live in the uncompiled (ONNX / SavedModel) `edgefirst.json` and are consumed by the converter. The compiled (converted) model **replaces** `split_hints` with the compiled `outputs[]` array — the two-layer logical/physical structure is the authoritative description of the compiled model.

```text
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│  Training Framework  │     │      Converter        │     │       HAL        │
│                      │     │                       │     │                  │
│  Embeds split_hints  │────▶│  Reads split_hints    │────▶│  Reads compiled  │
│  in ONNX metadata    │     │  Splits (at minimum   │     │  outputs[]       │
│                      │     │  on logical bounds,   │     │                  │
│  Logical boundaries  │     │  optionally further)  │     │  Direct path or  │
│  only.               │     │                       │     │  fallback path   │
│                      │     │  Replaces split_hints │     │                  │
│                      │     │  with outputs[] using │     │                  │
│                      │     │  two-layer structure  │     │                  │
└──────────────────────┘     └──────────────────────┘     └──────────────────┘
```

1. **ONNX / SavedModel** — Training framework embeds `split_hints` in `edgefirst.json` metadata. These describe logical boundaries only; there is no `outputs[]` decomposition yet.
2. **Converter** — Reads `split_hints`, performs the split (at minimum on logical bounds, optionally further). The compiled `edgefirst.json` replaces `split_hints` with the actual `outputs[]` array.
3. **HAL** — Reads the compiled `outputs[]` array. Each logical output either has direct tensor data (no children) or has `outputs[]` children that are the real physical tensors.

### Purpose

When a single output tensor contains channels with different value distributions (e.g., [0,1]-bounded box coordinates alongside unbounded linear projections), a shared quantization scale degrades accuracy. Split hints tell converters where these natural boundaries exist so they can apply independent quantization scales to each region.

### Schema

```yaml
split_hints:
  - type: quantization_split
    target: output0
    input_dtype: uint8
    output_dtype: int8
    description: "YOLOv8 detection head: boxes + scores + mask coefficients"
    strides: [8, 16, 32]
    anchors_per_cell: 1
    boundaries:
      - name: boxes
        channels: [0, 4]
      - name: scores
        channels: [4, 84]
        activation: sigmoid
      - name: mask_coefs
        channels: [84, 116]
```

### Fields

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `type` | string | Yes | Hint type identifier. Converters ignore types they do not understand |
| `target` | string | Yes | Name of the output tensor this hint applies to |
| `input_dtype` | string | No | Suggested input quantization dtype (e.g., `uint8`) |
| `output_dtype` | string | No | Suggested output quantization dtype (e.g., `int8`) |
| `description` | string | No | Human-readable description of the split |
| `strides` | int[] | No | FPN stride values (ascending). Declares spatial structure for converters that can perform per-scale decomposition |
| `anchors_per_cell` | int | No | For anchor-based models (default: 1). Per-scale channel count = `anchors_per_cell × boundary_channels` |
| `boundaries` | object[] | Yes | Ordered list of channel regions within the target tensor |

### Boundary Fields

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `name` | string | Yes | Free-form semantic label (e.g., `boxes`, `scores`, `mask_coefs`, `landmarks`, `objectness`, `confidence`) |
| `channels` | [int, int] | Yes | Channel range `[start, end)` in the logical output. Always post-decode, post-DFL logical channels (e.g., 4 for decoded box coords, not 64 for DFL-encoded) |
| `activation` | string | No | Post-activation to apply (`sigmoid`, `softmax`, `tanh`). Converters that can fuse it into the NPU do so; others note it for the HAL |

Boundary names are free-form semantic labels — not a fixed enum. Common ones: `boxes`, `scores`, `objectness`, `mask_coefs`, `landmarks`, `confidence`.

### Behavior Rules

- `split_hints` is an array — multiple hints can coexist (e.g., one per output tensor).
- Each hint has a `type` field — converters **must ignore** types they do not understand (forward compatibility).
- Converter UI presents all known split types from this schema as options.
- If the user enables a split type and matching hints exist in the model, the converter applies them.
- If the user enables a split type and no matching hints exist, the converter warns (not an error) and proceeds without splitting.
- Hints include suggested quantization defaults (`input_dtype`, `output_dtype`) that converters use as UI defaults; the user can override them.
- Boundary `channels` ranges must be non-overlapping and cover the full channel dimension of the target tensor when taken together.
- End-to-end models (`model.end2end: true`) are **incompatible with split_hints** — there is nothing to split because the output is already the final result.

### Hint Types

#### `quantization_split`

Channel boundaries within an output tensor that have different value distributions and benefit from independent quantization scales. The converter applies graph surgery to split the tensor at the specified boundaries, then quantizes each resulting tensor independently.

**Example: Ultralytics segmentation model**

The monolithic detection output `[1, 116, 8400]` contains 84 detection channels ([0,1]-bounded boxes + scores) and 32 mask coefficient channels (unbounded linear projection). Splitting at channel 84 allows independent quantization scales:

```yaml
split_hints:
  - type: quantization_split
    target: output0
    input_dtype: uint8
    output_dtype: int8
    description: "Separate mask coefficients from detection channels for independent quantization"
    strides: [8, 16, 32]
    boundaries:
      - name: boxes
        channels: [0, 4]
      - name: scores
        channels: [4, 84]
        activation: sigmoid
      - name: mask_coefs
        channels: [84, 116]
```

### Per-Task Split Recommendations

Based on quantization experiments:

| Task | Hints | Rationale |
| ---- | ----- | --------- |
| **Detection** | One `quantization_split` on output0 with `boxes` + `scores` boundaries | Per-component scales improve INT8 precision; boxes and scores have different distributions |
| **Segmentation** | One `quantization_split` on output0 with `boxes` + `scores` + `mask_coefs` boundaries | Mask coefficients (unbounded) especially benefit from their own scale |
| **End-to-end (YOLO26 `end2end: true`)** | None | Output is already post-NMS; nothing to split |
| **Single-output (BEV)** | None | Single output with uniform value distribution |

---

## Architecture Survey

Coverage of the two-layer output model across the detection, segmentation, and end-to-end architectures currently supported by the EdgeFirst ecosystem. The list grows as new architectures are onboarded — the two-layer model is general and accommodates additional families (SCRFD, EfficientDet, YOLACT, DETR variants, etc.) without schema changes.

| Architecture | Scales | Heads | Monolithic in ONNX? | Two-Layer Mapping |
| ------------ | ------ | ----- | ------------------- | ----------------- |
| YOLOv8 / YOLO11 detection | 3 | 2 (box, score) | Yes | 2 logical (`boxes`, `scores`), optional per-scale or xy/wh children |
| YOLOv8 / YOLO11 segmentation | 3 | 3 + protos | Yes | 3 logical w/ children + 1 direct (`protos`) |
| YOLO26 detection | 3 | 2 (box, score) | Yes | 2 logical, optional children — `encoding: direct` |
| YOLO26 segmentation | 3 | 3 + protos | Yes | 3 logical w/ children + 1 direct — `encoding: direct` |
| YOLO26 end-to-end | — | 1 | — | 1 logical `detections`, no children |
| YOLOv5 detection | 3 | combined (obj×cls) | No | 3 logical (`boxes`, `objectness`, `scores`), per-scale children — `score_format: obj_x_class` |
| YOLOv5 segmentation | 3 | combined + protos | No | 4 logical w/ children + 1 direct (`protos`) |
| ModelPack detection | 3 | 1 per-scale | No | 3 logical `type: detection` (one per scale), no children — `encoding: anchor` |
| ModelPack semantic seg | — | 1 | No | 1 logical `type: segmentation`, no children |
| SSD MobileNet | 6 | 2 (box, score) | No | 2 logical (`boxes`, `scores`), 6 per-scale children each — `encoding: anchor` |
| FastSAM | 3 | 3 + protos | Yes | Same as YOLOv8 segmentation |

**Key observations:**

- Every FPN-based architecture maps to logical outputs with per-scale children (when the converter splits) or direct outputs (when it doesn't).
- Models with non-spatial outputs (protos) use direct logical outputs for those.
- The only variable is whether the converter produces channel sub-splits (ARA-2 xy/wh), per-scale splits (Hailo), or no split (TFLite).

---

## Full Examples

### Example 1: ModelPack Semantic Segmentation

Direct logical output, no children — the output tensor IS the physical tensor.

```yaml
schema_version: 2
outputs:
  - name: segmentation_output
    type: segmentation
    shape: [1, 480, 640, 5]
    dshape:
      - batch: 1
      - height: 480
      - width: 640
      - num_classes: 5
    dtype: uint8
    quantization:
      scale: 0.00392
      zero_point: 0
      dtype: uint8
    decoder: modelpack
```

### Example 2: ModelPack Detection (Anchor Grid, Per-Scale Flat)

Each FPN scale is a direct logical output with `encoding: anchor`. No children — ModelPack grid outputs carry all streams (boxes + objectness + scores) in the channel dimension and are decoded by the `modelpack` decoder using `anchors` + `stride`.

```yaml
schema_version: 2
outputs:
  - name: output_0
    type: detection
    shape: [1, 40, 40, 54]    # 3 anchors × (4 box + 1 obj + 13 classes)
    dshape:
      - batch: 1
      - height: 40
      - width: 40
      - num_anchors_x_features: 54
    dtype: uint8
    quantization:
      scale: 0.176
      zero_point: 198
      dtype: uint8
    decoder: modelpack
    encoding: anchor
    stride: [16, 16]
    anchors:
      - [0.054, 0.065]
      - [0.089, 0.139]
      - [0.195, 0.196]

  - name: output_1
    type: detection
    shape: [1, 20, 20, 54]
    dshape:
      - batch: 1
      - height: 20
      - width: 20
      - num_anchors_x_features: 54
    dtype: uint8
    quantization:
      scale: 0.172
      zero_point: 201
      dtype: uint8
    decoder: modelpack
    encoding: anchor
    stride: [32, 32]
    anchors:
      - [0.125, 0.126]
      - [0.208, 0.260]
      - [0.529, 0.491]
```

### Example 3: Ultralytics YOLOv8 Detection — TFLite (Flat, No Children)

The TFLite quantizer splits boxes from scores (per `split_hints`) but does not decompose further — the DFL distribution is preserved in the compiled graph and decoded by the HAL. Each logical output IS the physical tensor.

```yaml
schema_version: 2
decoder_version: yolov8
nms: class_agnostic
outputs:
  - name: boxes
    type: boxes
    shape: [1, 64, 8400]         # DFL: 4 coords × reg_max=16
    dshape:
      - batch: 1
      - num_features: 64
      - num_boxes: 8400
    dtype: int8
    quantization:
      scale: 0.00392
      zero_point: 0
      dtype: int8
    decoder: ultralytics
    encoding: dfl                # HAL applies softmax + weighted-sum to recover 4 coords
    normalized: true

  - name: scores
    type: scores
    shape: [1, 80, 8400]
    dshape:
      - batch: 1
      - num_classes: 80
      - num_boxes: 8400
    dtype: int8
    quantization:
      scale: 0.00392
      zero_point: 0
      dtype: int8
    decoder: ultralytics
    score_format: per_class
```

### Example 4: Ultralytics YOLOv8 Detection — ARA-2 (xy/wh Channel Split)

ARA-2 splits `boxes` into `boxes_xy` and `boxes_wh` for independent INT16 quantization.

```json
{
  "schema_version": 2,
  "decoder_version": "yolov8",
  "nms": "class_agnostic",
  "outputs": [
    {
      "name": "boxes",
      "type": "boxes",
      "shape": [1, 4, 8400, 1],
      "dshape": [
        {"batch": 1},
        {"box_coords": 4},
        {"num_boxes": 8400},
        {"padding": 1}
      ],
      "encoding": "direct",
      "decoder": "ultralytics",
      "normalized": true,
      "outputs": [
        {
          "name": "_model_22_Div_1_output_0",
          "type": "boxes_xy",
          "shape": [1, 2, 8400, 1],
          "dshape": [
            {"batch": 1},
            {"box_coords": 2},
            {"num_boxes": 8400},
            {"padding": 1}
          ],
          "dtype": "int16",
          "quantization": {"scale": 3.129e-05, "zero_point": 0, "dtype": "int16"}
        },
        {
          "name": "_model_22_Sub_1_output_0",
          "type": "boxes_wh",
          "shape": [1, 2, 8400, 1],
          "dshape": [
            {"batch": 1},
            {"box_coords": 2},
            {"num_boxes": 8400},
            {"padding": 1}
          ],
          "dtype": "int16",
          "quantization": {"scale": 3.149e-05, "zero_point": 0, "dtype": "int16"}
        }
      ]
    },
    {
      "name": "scores",
      "type": "scores",
      "shape": [1, 80, 8400, 1],
      "dshape": [
        {"batch": 1},
        {"num_classes": 80},
        {"num_boxes": 8400},
        {"padding": 1}
      ],
      "dtype": "int8",
      "quantization": {"scale": 0.00392, "zero_point": 0, "dtype": "int8"},
      "decoder": "ultralytics",
      "score_format": "per_class"
    }
  ]
}
```

### Example 5: Ultralytics YOLOv8 Segmentation — Hailo (Per-Scale, 10 Physical Outputs)

Hailo splits at per-scale Conv nodes, producing one physical tensor per FPN scale for each logical output. `protos` is not split.

```json
{
  "schema_version": 2,
  "decoder_version": "yolov8",
  "nms": "class_agnostic",
  "outputs": [
    {
      "name": "boxes",
      "type": "boxes",
      "shape": [1, 64, 8400],
      "dshape": [{"batch": 1}, {"num_features": 64}, {"num_boxes": 8400}],
      "encoding": "dfl",
      "decoder": "ultralytics",
      "normalized": true,
      "outputs": [
        {
          "name": "boxes_0", "type": "boxes", "stride": 8, "scale_index": 0,
          "shape": [1, 80, 80, 64],
          "dshape": [{"batch": 1}, {"height": 80}, {"width": 80}, {"num_features": 64}],
          "dtype": "uint8", "quantization": {"scale": 0.0234, "zero_point": 128, "dtype": "uint8"}
        },
        {
          "name": "boxes_1", "type": "boxes", "stride": 16, "scale_index": 1,
          "shape": [1, 40, 40, 64],
          "dshape": [{"batch": 1}, {"height": 40}, {"width": 40}, {"num_features": 64}],
          "dtype": "uint8", "quantization": {"scale": 0.0198, "zero_point": 130, "dtype": "uint8"}
        },
        {
          "name": "boxes_2", "type": "boxes", "stride": 32, "scale_index": 2,
          "shape": [1, 20, 20, 64],
          "dshape": [{"batch": 1}, {"height": 20}, {"width": 20}, {"num_features": 64}],
          "dtype": "uint8", "quantization": {"scale": 0.0312, "zero_point": 125, "dtype": "uint8"}
        }
      ]
    },
    {
      "name": "scores",
      "type": "scores",
      "shape": [1, 80, 8400],
      "dshape": [{"batch": 1}, {"num_classes": 80}, {"num_boxes": 8400}],
      "decoder": "ultralytics",
      "score_format": "per_class",
      "outputs": [
        {
          "name": "scores_0", "type": "scores", "stride": 8, "scale_index": 0,
          "shape": [1, 80, 80, 80],
          "dshape": [{"batch": 1}, {"height": 80}, {"width": 80}, {"num_classes": 80}],
          "dtype": "uint8", "quantization": {"scale": 0.00392, "zero_point": 0, "dtype": "uint8"},
          "activation_applied": "sigmoid"
        },
        {
          "name": "scores_1", "type": "scores", "stride": 16, "scale_index": 1,
          "shape": [1, 40, 40, 80],
          "dshape": [{"batch": 1}, {"height": 40}, {"width": 40}, {"num_classes": 80}],
          "dtype": "uint8", "quantization": {"scale": 0.00389, "zero_point": 0, "dtype": "uint8"},
          "activation_applied": "sigmoid"
        },
        {
          "name": "scores_2", "type": "scores", "stride": 32, "scale_index": 2,
          "shape": [1, 20, 20, 80],
          "dshape": [{"batch": 1}, {"height": 20}, {"width": 20}, {"num_classes": 80}],
          "dtype": "uint8", "quantization": {"scale": 0.00401, "zero_point": 0, "dtype": "uint8"},
          "activation_applied": "sigmoid"
        }
      ]
    },
    {
      "name": "mask_coefs",
      "type": "mask_coefs",
      "shape": [1, 32, 8400],
      "dshape": [{"batch": 1}, {"num_protos": 32}, {"num_boxes": 8400}],
      "decoder": "ultralytics",
      "outputs": [
        {
          "name": "mask_coefs_0", "type": "mask_coefs", "stride": 8, "scale_index": 0,
          "shape": [1, 80, 80, 32],
          "dshape": [{"batch": 1}, {"height": 80}, {"width": 80}, {"num_protos": 32}],
          "dtype": "uint8", "quantization": {"scale": 0.0156, "zero_point": 64, "dtype": "uint8"}
        },
        {
          "name": "mask_coefs_1", "type": "mask_coefs", "stride": 16, "scale_index": 1,
          "shape": [1, 40, 40, 32],
          "dshape": [{"batch": 1}, {"height": 40}, {"width": 40}, {"num_protos": 32}],
          "dtype": "uint8", "quantization": {"scale": 0.0148, "zero_point": 66, "dtype": "uint8"}
        },
        {
          "name": "mask_coefs_2", "type": "mask_coefs", "stride": 32, "scale_index": 2,
          "shape": [1, 20, 20, 32],
          "dshape": [{"batch": 1}, {"height": 20}, {"width": 20}, {"num_protos": 32}],
          "dtype": "uint8", "quantization": {"scale": 0.0171, "zero_point": 60, "dtype": "uint8"}
        }
      ]
    },
    {
      "name": "protos",
      "type": "protos",
      "shape": [1, 32, 160, 160],
      "dshape": [{"batch": 1}, {"num_protos": 32}, {"height": 160}, {"width": 160}],
      "dtype": "uint8",
      "quantization": {"scale": 0.0203, "zero_point": 45, "dtype": "uint8"},
      "stride": 4
    }
  ]
}
```

### Example 6: YOLO26 End-to-End (Embedded NMS)

The model graph contains NMS; output is fully decoded. Single flat logical output with `type: detections`, no children. The root-level `nms` field is intentionally omitted — there is no external HAL NMS step to configure when NMS is embedded in the graph.

```yaml
schema_version: 2
decoder_version: yolo26
# Root-level 'nms' omitted: embedded NMS means no HAL NMS to configure.
model:
  end2end: true
outputs:
  - name: output0
    type: detections
    shape: [1, 100, 6]
    dshape:
      - batch: 1
      - num_boxes: 100
      - num_features: 6      # x1, y1, x2, y2, conf, class
    dtype: int8
    quantization:
      scale: 0.0078
      zero_point: 0
      dtype: int8
    normalized: false
    decoder: ultralytics
validation:
  nms: none                  # Tells validators not to invoke external NMS
```

### Example 7: YOLOv5 Detection (Anchor-Based, Per-Scale Children, `obj_x_class`)

YOLOv5 is anchor-based with 3 anchors per cell. Per-scale physical channel counts are multiplied by `anchors_per_cell`: boxes = 3×4 = 12, objectness = 3×1 = 3, scores = 3×80 = 240.

```json
{
  "schema_version": 2,
  "decoder_version": "yolov5",
  "nms": "class_agnostic",
  "outputs": [
    {
      "name": "boxes",
      "type": "boxes",
      "shape": [1, 12, 8400],
      "dshape": [{"batch": 1}, {"num_features": 12}, {"num_boxes": 8400}],
      "encoding": "anchor",
      "decoder": "ultralytics",
      "normalized": false,
      "outputs": [
        {
          "name": "boxes_0", "type": "boxes", "stride": 8, "scale_index": 0,
          "shape": [1, 80, 80, 12],
          "dshape": [{"batch": 1}, {"height": 80}, {"width": 80}, {"num_features": 12}],
          "dtype": "uint8", "quantization": {"scale": 0.032, "zero_point": 128, "dtype": "uint8"}
        },
        {
          "name": "boxes_1", "type": "boxes", "stride": 16, "scale_index": 1,
          "shape": [1, 40, 40, 12],
          "dshape": [{"batch": 1}, {"height": 40}, {"width": 40}, {"num_features": 12}],
          "dtype": "uint8", "quantization": {"scale": 0.029, "zero_point": 130, "dtype": "uint8"}
        },
        {
          "name": "boxes_2", "type": "boxes", "stride": 32, "scale_index": 2,
          "shape": [1, 20, 20, 12],
          "dshape": [{"batch": 1}, {"height": 20}, {"width": 20}, {"num_features": 12}],
          "dtype": "uint8", "quantization": {"scale": 0.035, "zero_point": 126, "dtype": "uint8"}
        }
      ]
    },
    {
      "name": "objectness",
      "type": "objectness",
      "shape": [1, 3, 8400],
      "dshape": [{"batch": 1}, {"num_features": 3}, {"num_boxes": 8400}],
      "decoder": "ultralytics",
      "outputs": [
        {
          "name": "objectness_0", "type": "objectness", "stride": 8, "scale_index": 0,
          "shape": [1, 80, 80, 3],
          "dshape": [{"batch": 1}, {"height": 80}, {"width": 80}, {"num_features": 3}],
          "dtype": "uint8", "quantization": {"scale": 0.0039, "zero_point": 0, "dtype": "uint8"},
          "activation_applied": "sigmoid"
        },
        {
          "name": "objectness_1", "type": "objectness", "stride": 16, "scale_index": 1,
          "shape": [1, 40, 40, 3],
          "dshape": [{"batch": 1}, {"height": 40}, {"width": 40}, {"num_features": 3}],
          "dtype": "uint8", "quantization": {"scale": 0.0041, "zero_point": 0, "dtype": "uint8"},
          "activation_applied": "sigmoid"
        },
        {
          "name": "objectness_2", "type": "objectness", "stride": 32, "scale_index": 2,
          "shape": [1, 20, 20, 3],
          "dshape": [{"batch": 1}, {"height": 20}, {"width": 20}, {"num_features": 3}],
          "dtype": "uint8", "quantization": {"scale": 0.0038, "zero_point": 0, "dtype": "uint8"},
          "activation_applied": "sigmoid"
        }
      ]
    },
    {
      "name": "scores",
      "type": "scores",
      "shape": [1, 240, 8400],
      "dshape": [{"batch": 1}, {"num_features": 240}, {"num_boxes": 8400}],
      "decoder": "ultralytics",
      "score_format": "obj_x_class",
      "outputs": [
        {
          "name": "scores_0", "type": "scores", "stride": 8, "scale_index": 0,
          "shape": [1, 80, 80, 240],
          "dshape": [{"batch": 1}, {"height": 80}, {"width": 80}, {"num_features": 240}],
          "dtype": "uint8", "quantization": {"scale": 0.0039, "zero_point": 0, "dtype": "uint8"},
          "activation_applied": "sigmoid"
        },
        {
          "name": "scores_1", "type": "scores", "stride": 16, "scale_index": 1,
          "shape": [1, 40, 40, 240],
          "dshape": [{"batch": 1}, {"height": 40}, {"width": 40}, {"num_features": 240}],
          "dtype": "uint8", "quantization": {"scale": 0.0040, "zero_point": 0, "dtype": "uint8"},
          "activation_applied": "sigmoid"
        },
        {
          "name": "scores_2", "type": "scores", "stride": 32, "scale_index": 2,
          "shape": [1, 20, 20, 240],
          "dshape": [{"batch": 1}, {"height": 20}, {"width": 20}, {"num_features": 240}],
          "dtype": "uint8", "quantization": {"scale": 0.0041, "zero_point": 0, "dtype": "uint8"},
          "activation_applied": "sigmoid"
        }
      ]
    }
  ]
}
```

### Instance Segmentation Mask Computation

For instance segmentation outputs (Ultralytics), the final per-object mask is computed from mask coefficients and prototypes:

```python
# For each detected object with mask_coefs [32]:
instance_mask = sigmoid(mask_coefs @ protos)  # [32] @ [32, H, W] -> [H, W]
# Crop to bounding box region for final instance mask
```

---

## Calibration Artifact

Quantizing converters need a representative sample of model inputs to measure activation ranges. EdgeFirst Studio captures that sample when a session exports the model, at that model's input geometry, as a `.safetensors` **calibration snapshot**: a pre-filtered, pre-processed subset of the training data with embedded metadata and full provenance back to the source samples. Whole-frame and non-tiled models are calibrated on letterboxed (or, for direct-resize models, stretched) frames at the input resolution; [tiled models](#tiling) are calibrated on deployment-grid tiles at native scale.

The `edgefirst.json` `calibration` field records the snapshot filename:

```yaml
calibration: string          # calibration-{dataset_id}-{param_hash}.safetensors
```

Each consuming converter additionally records the filename it calibrated against in its [converter-traceability section](#converter-traceability) (e.g. `tflite_quantizer.calibration`), so the compiled model names its calibration snapshot, the snapshot names its parameter hash and source sample IDs, and the audit chain runs unbroken from a deployed binary back to individual training images.

The snapshot format (uint8 `[0, 255]` NCHW tensors plus a populated `__metadata__` map), the model-free dynamic-range selection algorithm, the parameter hash and caching scheme, the embedded-metadata schema, and the full producer/consumer contract are documented in [Model Conversion — Calibration Snapshot](conversion/calibration.md).

---

## Converter Traceability

When a converter processes a model, it augments the existing `edgefirst.json` with a converter-specific section at the top level. This provides full traceability of all conversion steps applied to the model.

### Rules

- Converters **augment** — they never replace or remove existing fields in `edgefirst.json` except for `split_hints`, which is replaced by the compiled `outputs[]` array per the split-hints lifecycle.
- Each converter adds a top-level key named after itself (e.g., `"tflite_quantizer"`, `"neutron"`, `"ara2"`, `"hailo"`).
- The converter section records conversion parameters, version, and any decisions made during conversion.
- Multiple converter sections can coexist when a model passes through a pipeline chain (e.g., TFLite Quantizer followed by Neutron Converter).
- Converters copy the [`tiling`](#tiling) section unchanged. It describes the model, and a runtime reads it from the compiled artifact to decide how to feed frames; conversion decisions belong in the converter's own section.
- The height and width in `input.shape` match the compiled artifact's input, in the layout of the output format.
- A converter that calibrates checks the snapshot's geometry against the model before using it (see [Calibration Snapshot — Geometry check](conversion/calibration.md#geometry-check)) and records `calibration_geometry: {resize, input_shape}` beside its `calibration` field, adding `full_frame: true` when the snapshot holds whole-frame samples.

### Converter Section Schema

Each converter section is a free-form object, but should include at minimum:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `version` | string | Converter app version |
| `timestamp` | string | ISO 8601 conversion timestamp |
| `task` | string | Studio batch task ID for this conversion step (e.g., `bt-3a1f`) |
| `splits_applied` | string[] | List of `split_hints[].type` values that were consumed |
| `calibration` | string or object | Calibration snapshot used: the snapshot filename, or a converter-specific record that names it |
| `calibration_geometry` | object | `{resize, input_shape}` of the snapshot, with `full_frame: true` when it holds whole-frame samples; present when the converter calibrated (see [Geometry check](conversion/calibration.md#geometry-check)) |

Additional fields are converter-specific and documented by each converter app.

### Example: Single Converter

After TFLite quantization of an Ultralytics detection model:

```json
{
  "schema_version": 2,
  "host": { "studio_server": "test.edgefirst.studio", "...": "..." },
  "model": { "...": "..." },
  "outputs": [ "..." ],

  "tflite_quantizer": {
    "version": "1.0.0",
    "timestamp": "2026-03-20T15:30:00Z",
    "task": "bt-3a1f",
    "input_dtype": "uint8",
    "output_dtype": "int8",
    "calibration": "calibration-ds-2bcc-a1b2c3d4.safetensors",
    "calibration_geometry": {"resize": "letterbox", "input_shape": [640, 640]},
    "calibration_samples": 500,
    "splits_applied": ["quantization_split"],
    "quantizer": "mlir"
  }
}
```

### Example: Pipeline Chain

After TFLite quantization followed by Neutron conversion for i.MX95 deployment:

```json
{
  "schema_version": 2,
  "host": { "...": "..." },
  "model": { "...": "..." },
  "outputs": [ "..." ],

  "tflite_quantizer": {
    "version": "1.0.0",
    "timestamp": "2026-03-20T15:30:00Z",
    "task": "bt-3a1f",
    "input_dtype": "uint8",
    "output_dtype": "int8",
    "calibration": "calibration-ds-2bcc-a1b2c3d4.safetensors",
    "calibration_geometry": {"resize": "letterbox", "input_shape": [640, 640]},
    "calibration_samples": 500,
    "splits_applied": [],
    "quantizer": "mlir"
  },

  "neutron": {
    "version": "2.1.0",
    "timestamp": "2026-03-20T15:45:00Z",
    "task": "bt-3a20",
    "target": "imx95",
    "neutron_version": "1.2.0",
    "delegate": "neutron"
  }
}
```

### Ordering

When a model passes through multiple converters, the chronological order is determined by the `timestamp` field in each converter section. The `task` field links each conversion step back to its Studio batch task (e.g., `bt-3a1f`) for full audit trail.

---

## ONNX-Specific Metadata

ONNX models exported from [ModelPack](modelpack/index.md) or [Ultralytics](ultralytics/index.md) include additional official metadata fields:

| Field | ModelPack Value | Ultralytics Value | Purpose |
| ----- | --------------- | ----------------- | ------- |
| `producer_name` | "EdgeFirst ModelPack" | "EdgeFirst Ultralytics" | Identifies producing framework |
| `producer_version` | Package version | Package version | Version tracking |
| `graph.name` | Model name | Model name | Graph identification |
| `doc_string` | Description | Description | Human-readable description |

Custom metadata properties (all string values):

| Key | Content | Purpose |
| --- | ------- | ------- |
| `edgefirst` | Full config as JSON | Complete configuration |
| `name` | Model name | Quick access (no JSON parsing) |
| `description` | Model description | Quick access |
| `author` | Author/organization | Quick access |
| `studio_server` | Full hostname | Quick access for traceability |
| `project_id` | Project ID | Quick access for traceability |
| `session_id` | Session ID | Quick access for traceability |
| `dataset` | Dataset name | Quick access |
| `dataset_id` | Dataset ID | Quick access for traceability |
| `labels` | JSON array of labels | Class labels |

---

## Third-Party Integration

Any training framework can produce EdgeFirst-compatible models by embedding the appropriate metadata.

### Minimum Required Fields

For basic [EdgeFirst Perception](../perception/index.md) stack compatibility:

```yaml
schema_version: 2

input:
  shape: [1, 640, 640, 3]
  cameraadaptor: rgb

model:
  detection: true
  segmentation: false

outputs:
  - name: boxes
    type: boxes
    shape: [1, 4, 8400]
    dshape:
      - batch: 1
      - box_coords: 4
      - num_boxes: 8400
    dtype: float32
    quantization: null
    encoding: direct
    decoder: ultralytics
    normalized: true

  - name: scores
    type: scores
    shape: [1, 80, 8400]
    dshape:
      - batch: 1
      - num_classes: 80
      - num_boxes: 8400
    dtype: float32
    quantization: null
    decoder: ultralytics
    score_format: per_class

dataset:
  classes:
    - class1
    - class2
```

### Full Traceability (Recommended)

For production MLOps integration with [EdgeFirst Studio](../studio/index.md):

```yaml
schema_version: 2

host:
  studio_server: test.edgefirst.studio
  project_id: "1123"
  session: t-2110              # Hex value, convert to int for URLs

dataset:
  name: "My Dataset"
  id: ds-xyz789
  classes: [...]

name: "my-model-v1"              # Model/session name
description: "Model for production deployment"
author: "My Organization"
```

### Embedding Metadata in TFLite

!!! note "Dependencies"
    This example requires the `tflite-support` and `pyyaml` packages:
    ```bash
    pip install tflite-support pyyaml
    ```

```python
from tensorflow_lite_support.metadata.python.metadata_writers import metadata_writer, writer_utils
from tensorflow_lite_support.metadata import metadata_schema_py_generated as schema
import yaml
from typing import List
import tempfile
import os

def add_edgefirst_metadata(tflite_path: str, config: dict, labels: List[str]):
    """Add EdgeFirst metadata to a TFLite model."""

    # Write config and labels to temp files in a cross-platform way
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, 'edgefirst.yaml')
        labels_path = os.path.join(tmpdir, 'labels.txt')

        with open(config_path, 'w') as f:
            yaml.dump(config, f)

        with open(labels_path, 'w') as f:
            f.write('\n'.join(labels))

        # Create model metadata
        model_meta = schema.ModelMetadataT()
        model_meta.name = config.get('name', '')
        model_meta.description = config.get('description', '')
        model_meta.author = config.get('author', '')

        # Load and populate
        tflite_buffer = writer_utils.load_file(tflite_path)
        writer = metadata_writer.MetadataWriter.create_from_metadata(
            model_buffer=tflite_buffer,
            model_metadata=model_meta,
            associated_files=[labels_path, config_path]
        )

        writer_utils.save_file(writer.populate(), tflite_path)
```

### Embedding Metadata in ONNX

!!! note "Dependencies"
    This example requires the `onnx` package:
    ```bash
    pip install onnx
    ```

```python
import onnx
import json
from typing import List

def add_edgefirst_metadata(onnx_path: str, config: dict, labels: List[str]):
    """Add EdgeFirst metadata to an ONNX model."""

    model = onnx.load(onnx_path)

    # Set official ONNX fields
    model.producer_name = 'My Training Framework'
    model.producer_version = '1.0.0'

    if config.get('name'):
        model.graph.name = config['name']
    if config.get('description'):
        model.doc_string = config['description']

    # Add custom metadata
    metadata = {
        'edgefirst': json.dumps(config),
        'labels': json.dumps(labels),
        'name': config.get('name', ''),
        'description': config.get('description', ''),
        'author': config.get('author', ''),
        'studio_server': config.get('host', {}).get('studio_server', ''),
        'project_id': str(config.get('host', {}).get('project_id', '')),
        'session_id': config.get('host', {}).get('session', ''),
        'dataset': config.get('dataset', {}).get('name', ''),
        'dataset_id': str(config.get('dataset', {}).get('id', '')),
    }

    for key, value in metadata.items():
        if value:
            prop = model.metadata_props.add()
            prop.key = key
            prop.value = str(value)

    onnx.save(model, onnx_path)
```

---

## Updating Metadata

### Updating TFLite Metadata

Since TFLite models are ZIP archives, you can update embedded files:

!!! note "zip command"
    The `zip` command is available on most platforms but may need to be installed:

    - **macOS**: Pre-installed
    - **Linux**: `sudo apt install zip` (Debian/Ubuntu) or `sudo yum install zip` (RHEL/CentOS)
    - **Windows**: Available via [Git Bash](https://git-scm.com/), WSL, or [Info-ZIP](http://infozip.sourceforge.net/)

```bash
# Update edgefirst.yaml
zip -u mymodel.tflite edgefirst.yaml

# Update labels
zip -u mymodel.tflite labels.txt

# Add new files
zip mymodel.tflite edgefirst.json
```

### Updating ONNX Metadata

```python
import onnx
import json

model = onnx.load('mymodel.onnx')

# Update existing metadata
for prop in model.metadata_props:
    if prop.key == 'description':
        prop.value = 'Updated description'

# Add new metadata
prop = model.metadata_props.add()
prop.key = 'custom_field'
prop.value = 'custom_value'

onnx.save(model, 'mymodel.onnx')
```

---

## Schema Reference

### Host Section

The host section identifies the [EdgeFirst Studio](../studio/index.md) instance and [training session](../studio/models.md#training-sessions) that produced the model.

```yaml
host:
  studio_server: test.edgefirst.studio  # Full EdgeFirst Studio hostname
  project_id: "1123"                    # Project ID for Studio URLs
  session: t-2110                       # Training session ID (hex, prefix t-)
  organization: Au-Zone Technologies    # Organization that initiated training
```

!!! note "Converting IDs for Studio URLs"
    Session and dataset IDs in metadata use hexadecimal values with prefixes (`t-` for training sessions, `ds-` for datasets). To construct Studio URLs, strip the prefix and convert from hex to decimal:

    - `t-2110` → `int('2110', 16)` → `8464`
    - `ds-1c8` → `int('1c8', 16)` → `456`

### Dataset Section

The dataset section references the [dataset](../datasets/index.md) used for training. See the [Dataset Zoo](../datasets/index.md) for available datasets and [Dataset Structure](../datasets/format/index.md) for format details.

```yaml
dataset:
  name: "COCO 2017"      # Human-readable name
  id: ds-abc123          # Dataset ID (prefix: ds-)
  classes:               # Ordered list of class labels
    - background
    - person
    - car
```

### Model Identification

Top-level fields for model identification, populated from the [training session](training/vision.md) name and description.

```yaml
name: "coffeecup-detection"       # Model/session name (used in filename)
description: "Object detection model for coffee cups"
author: "Au-Zone Technologies"    # Organization
```

### Input Section

The input section specifies image preprocessing requirements. See [Vision Augmentations](augmentations.md) for training-time augmentation configuration.

```yaml
input:
  shape: [1, 640, 640, 3]  # Input tensor shape
  cameraadaptor: rgb       # rgb, rgba, yuyv, bgr
```

!!! note "Data Layout"
    The `shape` field uses the model's native tensor layout. This can be either NHWC `[batch, height, width, channels]` or NCHW `[batch, channels, height, width]` depending on how the model was exported. While TFLite typically uses NHWC and ONNX typically uses NCHW, both formats can support either layout — always check the actual shape values.

### Model Section

The model section captures architecture configuration. These parameters can be configured during [training session setup](training/vision.md#create-training-session) in EdgeFirst Studio. See the [ModelPack](modelpack/index.md#training-parameters) and [Ultralytics](ultralytics/index.md) documentation for detailed parameter descriptions.

```yaml
# ModelPack model configuration
model:
  backbone: cspdarknet19
  model_size: nano       # nano, small, medium, large
  activation: relu6      # relu, relu6, silu, mish
  detection: true
  segmentation: false
  classification: false
  anchors:               # Per-level anchor boxes (pixels at input resolution)
    - [[35, 42], [57, 89], [125, 126]]
    - [[125, 126], [208, 260], [529, 491]]

# Ultralytics model configuration
model:
  model_version: v8      # v5, v8, v11, v26
  model_task: segment    # detect, segment
  model_size: n          # n (nano), s (small), m (medium), l (large), x (xlarge)
  detection: false
  segmentation: true
  end2end: false         # true for YOLO26 end-to-end models with embedded NMS
```

### Outputs Section

Each entry in the top-level `outputs[]` is a **logical output** following the two-layer model described in [Output Specification](#output-specification). See [Full Examples](#full-examples) for complete layouts per framework and task.

Minimal Ultralytics detection (TFLite, flat):

```yaml
outputs:
  - name: boxes
    type: boxes
    shape: [1, 4, 8400]
    dshape:
      - batch: 1
      - box_coords: 4
      - num_boxes: 8400
    dtype: int8
    quantization: {scale: 0.00392, zero_point: 0, dtype: int8}
    decoder: ultralytics
    encoding: direct
    normalized: true

  - name: scores
    type: scores
    shape: [1, 80, 8400]
    dshape:
      - batch: 1
      - num_classes: 80
      - num_boxes: 8400
    dtype: int8
    quantization: {scale: 0.00392, zero_point: 0, dtype: int8}
    decoder: ultralytics
    score_format: per_class
```

---

## Appendix: Ultralytics YOLO Split Hints Reference

This appendix shows the exact `split_hints` that edgefirst-studio-ultralytics embeds in ONNX metadata for each supported YOLO version × task combination, using 80 COCO classes as the reference.

All versions share:

- 3 FPN scales, strides [8, 16, 32]
- Image size 640 → spatial positions: 80×80 + 40×40 + 20×20 = 8400
- Segmentation adds 32 `mask_coefs` channels + `protos` output `[1, 32, 160, 160]` at stride 4
- `input_dtype: uint8`, `output_dtype: int8`
- Box coordinates are always 4 logical channels (post-decode)

Key differences:

- **YOLOv5**: `anchors_per_cell: 3`, `encoding: anchor`, has `objectness` boundary, `score_format: obj_x_class`. Total logical channels per anchor: 4+1+nc [+32]. Monolithic output = (4+1+80)×3 = 255 channels for detect, (4+1+80+32)×3 = 351 for segment.
- **YOLOv8 / YOLO11**: `encoding: dfl` (64 physical box channels, 4 logical), `score_format: per_class`. Total: 4+nc [+32]. So 84 for detect, 116 for segment.
- **YOLO26**: `encoding: direct` (reg_max=1, 4 box channels), `score_format: per_class`. Total: 4+nc [+32]. So 84 for detect, 116 for segment. Same `split_hints` as v8/v11.

### A.1 YOLOv8n / YOLO11n Detection (80 classes)

```json
{
  "split_hints": [
    {
      "type": "quantization_split",
      "target": "output0",
      "input_dtype": "uint8",
      "output_dtype": "int8",
      "strides": [8, 16, 32],
      "description": "Detection head: boxes + scores",
      "boundaries": [
        {"name": "boxes", "channels": [0, 4]},
        {"name": "scores", "channels": [4, 84], "activation": "sigmoid"}
      ]
    }
  ]
}
```

YOLO11 uses the same `Detect` head architecture as YOLOv8 (anchor-free, DFL with reg_max=16). Split hints are identical.

| Boundary | Channels | Logical | Encoding | Activation | score_format |
| -------- | -------- | ------- | -------- | ---------- | ------------ |
| boxes | [0, 4) | 4 | dfl | — | — |
| scores | [4, 84) | 80 | — | sigmoid | per_class |

Monolithic output0 shape: `[1, 84, 8400]`

### A.2 YOLOv8n / YOLO11n Segmentation (80 classes, 32 protos)

```json
{
  "split_hints": [
    {
      "type": "quantization_split",
      "target": "output0",
      "input_dtype": "uint8",
      "output_dtype": "int8",
      "strides": [8, 16, 32],
      "description": "Segmentation head: boxes + scores + mask coefficients",
      "boundaries": [
        {"name": "boxes", "channels": [0, 4]},
        {"name": "scores", "channels": [4, 84], "activation": "sigmoid"},
        {"name": "mask_coefs", "channels": [84, 116]}
      ]
    }
  ]
}
```

`output1` (protos `[1, 32, 160, 160]`) is not included in split_hints — it's a separate ONNX output that does not need splitting.

| Boundary | Channels | Logical | Encoding | Activation | score_format |
| -------- | -------- | ------- | -------- | ---------- | ------------ |
| boxes | [0, 4) | 4 | dfl | — | — |
| scores | [4, 84) | 80 | — | sigmoid | per_class |
| mask_coefs | [84, 116) | 32 | — | — | — |

Monolithic output0 shape: `[1, 116, 8400]`

### A.3 YOLO26n Detection (80 classes)

```json
{
  "split_hints": [
    {
      "type": "quantization_split",
      "target": "output0",
      "input_dtype": "uint8",
      "output_dtype": "int8",
      "strides": [8, 16, 32],
      "description": "Detection head: boxes + scores",
      "boundaries": [
        {"name": "boxes", "channels": [0, 4]},
        {"name": "scores", "channels": [4, 84], "activation": "sigmoid"}
      ]
    }
  ]
}
```

YOLO26 uses `reg_max=1`, producing 4-channel boxes directly (no DFL distribution). The logical split_hints are identical to YOLOv8/v11 — the `encoding` difference (`direct` vs `dfl`) is captured in the compiled `outputs[]`, not in `split_hints`. End-to-end mode (`model.end2end: true`) is incompatible with `split_hints`.

| Boundary | Channels | Logical | Encoding | Activation | score_format |
| -------- | -------- | ------- | -------- | ---------- | ------------ |
| boxes | [0, 4) | 4 | direct | — | — |
| scores | [4, 84) | 80 | — | sigmoid | per_class |

Monolithic output0 shape: `[1, 84, 8400]`

### A.4 YOLO26n Segmentation (80 classes, 32 protos)

```json
{
  "split_hints": [
    {
      "type": "quantization_split",
      "target": "output0",
      "input_dtype": "uint8",
      "output_dtype": "int8",
      "strides": [8, 16, 32],
      "description": "Segmentation head: boxes + scores + mask coefficients",
      "boundaries": [
        {"name": "boxes", "channels": [0, 4]},
        {"name": "scores", "channels": [4, 84], "activation": "sigmoid"},
        {"name": "mask_coefs", "channels": [84, 116]}
      ]
    }
  ]
}
```

| Boundary | Channels | Logical | Encoding | Activation | score_format |
| -------- | -------- | ------- | -------- | ---------- | ------------ |
| boxes | [0, 4) | 4 | direct | — | — |
| scores | [4, 84) | 80 | — | sigmoid | per_class |
| mask_coefs | [84, 116) | 32 | — | — | — |

Monolithic output0 shape: `[1, 116, 8400]`

### A.5 YOLOv5n Detection (80 classes)

```json
{
  "split_hints": [
    {
      "type": "quantization_split",
      "target": "output0",
      "input_dtype": "uint8",
      "output_dtype": "int8",
      "strides": [8, 16, 32],
      "anchors_per_cell": 3,
      "description": "Detection head: boxes + objectness + scores (anchor-based)",
      "boundaries": [
        {"name": "boxes", "channels": [0, 4]},
        {"name": "objectness", "channels": [4, 5], "activation": "sigmoid"},
        {"name": "scores", "channels": [5, 85], "activation": "sigmoid"}
      ]
    }
  ]
}
```

YOLOv5 is anchor-based with 3 anchors per cell. Per-scale physical channel counts are multiplied by `anchors_per_cell`: boxes=3×4=12, objectness=3×1=3, scores=3×80=240. Total per anchor: 4+1+80=85, total per cell: 85×3=255. Concrete anchor dimensions are in `model.anchors`.

| Boundary | Channels | Logical | ×anchors | Encoding | Activation | score_format |
| -------- | -------- | ------- | -------- | -------- | ---------- | ------------ |
| boxes | [0, 4) | 4 | 12 | anchor | — | — |
| objectness | [4, 5) | 1 | 3 | — | sigmoid | — |
| scores | [5, 85) | 80 | 240 | — | sigmoid | obj_x_class |

Monolithic output0 shape: `[1, 255, 8400]`

### A.6 YOLOv5n Segmentation (80 classes, 32 protos)

```json
{
  "split_hints": [
    {
      "type": "quantization_split",
      "target": "output0",
      "input_dtype": "uint8",
      "output_dtype": "int8",
      "strides": [8, 16, 32],
      "anchors_per_cell": 3,
      "description": "Segmentation head: boxes + objectness + scores + mask coefficients (anchor-based)",
      "boundaries": [
        {"name": "boxes", "channels": [0, 4]},
        {"name": "objectness", "channels": [4, 5], "activation": "sigmoid"},
        {"name": "scores", "channels": [5, 85], "activation": "sigmoid"},
        {"name": "mask_coefs", "channels": [85, 117]}
      ]
    }
  ]
}
```

| Boundary | Channels | Logical | ×anchors | Encoding | Activation | score_format |
| -------- | -------- | ------- | -------- | -------- | ---------- | ------------ |
| boxes | [0, 4) | 4 | 12 | anchor | — | — |
| objectness | [4, 5) | 1 | 3 | — | sigmoid | — |
| scores | [5, 85) | 80 | 240 | — | sigmoid | obj_x_class |
| mask_coefs | [85, 117) | 32 | 96 | — | — | — |

Monolithic output0 shape: `[1, 351, 8400]`

### A.7 Summary Table

| Model | Task | Boundaries | output0 channels | anchors_per_cell | encoding | score_format |
| ----- | ---- | ---------- | ---------------- | ---------------- | -------- | ------------ |
| YOLOv5 | detect | boxes, objectness, scores | 255 (85×3) | 3 | anchor | obj_x_class |
| YOLOv5 | segment | boxes, objectness, scores, mask_coefs | 351 (117×3) | 3 | anchor | obj_x_class |
| YOLOv8 | detect | boxes, scores | 84 | 1 | dfl | per_class |
| YOLOv8 | segment | boxes, scores, mask_coefs | 116 | 1 | dfl | per_class |
| YOLO11 | detect | boxes, scores | 84 | 1 | dfl | per_class |
| YOLO11 | segment | boxes, scores, mask_coefs | 116 | 1 | dfl | per_class |
| YOLO26 | detect | boxes, scores | 84 | 1 | direct | per_class |
| YOLO26 | segment | boxes, scores, mask_coefs | 116 | 1 | direct | per_class |

All models: 3 scales, strides [8, 16, 32], 8400 spatial positions at 640px input.

---

## Related Articles

1. [Camera Adaptor](cameraadaptor.md) - Native camera format support for edge deployment
2. [ModelPack Overview](modelpack/index.md) - Architecture details and training parameters
3. [Ultralytics Integration](ultralytics/index.md) - YOLOv8/v11/v26 training and deployment
4. [Training Vision Models](training/vision.md) - Step-by-step training workflow
5. [On Cloud Validation](validation/vision/managed.md) - Managed validation sessions
6. [On Target Validation](validation/vision/user_managed.md) - User-managed validation with the EdgeFirst Profiler
7. [Model Quantization](conversion/tflite.md) - Converting ONNX to quantized TFLite
8. [Deploying to Embedded Targets](deployment/launcher.md) - Model deployment workflow
9. [EdgeFirst Perception Middleware](../perception/index.md) - Runtime inference stack
10. [Dataset Zoo](../datasets/index.md) - Available datasets for training
11. [Model Experiments Dashboard](../studio/models.md) - Managing training and validation sessions
