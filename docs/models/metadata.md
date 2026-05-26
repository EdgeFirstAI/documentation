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
|--------|-------------------|---------------|--------|
| TFLite | ZIP archive (associated files) | `edgefirst.json` | `labels.txt` |
| ONNX | Custom metadata properties | `edgefirst` (JSON) | `labels` (JSON array) |

### Supported Training Frameworks

| Framework | Decoder | Architecture | Use Case |
|-----------|---------|--------------|----------|
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
|-------|----------|---------|
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
  username: string         # User who initiated training

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
|---|---|---|
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
|---|---|---|
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
|---|---|
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
|---|---|---|---|
| `dfl` | `reg_max × 4` (typically 64) | Distribution Focal Loss encoding. Each coordinate is a probability distribution over `reg_max` bins. | Softmax over each `reg_max` group, then weighted sum → 4 coordinates. Common in YOLOv8, YOLO11. |
| `direct` | 4 | Direct coordinate values — already decoded. | Dequantize only. Common in YOLO26 (reg_max=1), ARA-2 post-split. |
| `anchor` | `anchors_per_cell × 4` | Anchor-based grid offsets. Each group of 4 is (tx, ty, tw, th) requiring sigmoid + anchor-scale transform. | Sigmoid + anchor transform per grid cell. Common in YOLOv5, SSD MobileNet, ModelPack. |

`encoding` is required on all `boxes` outputs in v2.

### Score Format

The `score_format` field on a `scores` logical output disambiguates YOLOv5's `obj_x_class` encoding from the default per-class encoding used by YOLOv8/v11/v26:

| Value | Description | Architecture |
|---|---|---|
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

**Root-level only:** `decoder_version`, `nms` (HAL NMS mode). These describe model-wide behaviour and never appear inside an `outputs[]` entry.

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

```
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
|---|---|---|---|
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

```
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
|---|---|---|---|
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
|---|---|---|---|---|
| ONNX | Scalar scale | 1-D scale + `axis` | Implicit (zero_point=0) | `axis` (default 1) |
| TFLite/LiteRT | Scalar (1-element array) | 1-D scale + `quantized_dimension` | Implicit (zero_point=0 for weights) | `quantized_dimension` |
| TensorRT | Scalar scale | Per-channel scale | Always symmetric | Output channel axis |
| PyTorch | Scalar scale | 1-D scale + `axis` | Explicit `qscheme` enum | `axis` parameter |

### Target-Specific Term Mapping

Some NPU toolchains use different terminology internally. Converters translate at the boundary — the compiled `edgefirst.json` always uses the standard terms above.

**Kinara ARA-2** (ioparams.json, qmode 9 — asymmetric):

| Kinara term | edgefirst.json term | Notes |
|---|---|---|
| `outputScale` / `outputQn` | `scale` | Identical value for qmode 9. For symmetric qmodes (0–3), Kinara's `qn` is 1/scale — but the ARA-2 converter always uses qmode 9 |
| `offset` | `zero_point` | Identical value |
| `bpp` + `isSigned` | `dtype` | `bpp=1, signed` → `int8`, `bpp=2, unsigned` → `uint16`, etc. |

**Hailo** (HEF quantization info):

| Hailo term | edgefirst.json term |
|---|---|
| `qp_scale` | `scale` |
| `qp_zp` | `zero_point` |

---

## Data Layout (NCHW vs NHWC)

Deep learning frameworks use different memory layouts for tensor data. The metadata accurately reflects each format's native layout:

| Format | Data Layout | Shape Convention | Example (batch=1, 640x640, RGB) |
|--------|-------------|------------------|----------------------------------|
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
|---|---|---|
| `rgb` | Standard RGB | Red, Green, Blue |
| `bgr` | OpenCV default | Blue, Green, Red |
| `rgba` | RGB with alpha | Red, Green, Blue, Alpha |
| `bgra` | BGR with alpha | Blue, Green, Red, Alpha |
| `grey` | Greyscale | Single channel |
| `yuyv` | YUV 4:2:2 packed | For direct camera sensor input |

---

## Validation Parameters

The `validation` section records the recommended settings based on how the model was trained. These parameters are **informational preferences** — they document the model author's intended configuration for validation and inference.

!!! note "Two distinct `nms` fields"
    This document uses `nms` at two levels with different semantics:

    - **`validation.nms`** (this section) — selects the NMS *implementation* (`hal`, `numpy`, `tensorflow`, `torch`) or `none` for models with embedded NMS.
    - **root-level `nms`** (see [HAL NMS Field](#hal-nms-field)) — selects HAL decoder *behaviour* (`class_agnostic` vs `class_aware`).

    The two fields are independent and can coexist. Keep the distinction in mind when reading the rest of this section.

### Parameter Semantics

| Parameter | Description | Default | Override at Runtime? |
|---|---|---|---|
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
|---|---|
| `none` | No external NMS. For models with embedded NMS — either architectural end-to-end (YOLO26) or engine-embedded (ONNX/TRT/TFLite with NMS ops appended). Supports both detection and segmentation |
| `numpy` | NumPy-based NMS implementation (default fallback) |
| `hal` | EdgeFirst HAL decoder NMS |
| `tensorflow` | TensorFlow NMS |
| `torch` | PyTorch (torchvision) NMS |

When `--override` is set, the validator reads `validation.nms` from the model metadata and applies it automatically.

### Box Coordinate Format (`normalized`)

The `normalized` field on `boxes` and `detections` outputs specifies the coordinate format:

| Value | Description | Coordinate Range |
|---|---|---|
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

The two-layer `outputs[]` structure (introduced in [Output Specification](#output-specification)) is descriptive: converters declare the logical contract and — when they split the tensor further — describe the physical decomposition they produced. This section covers the post-processing decoder contract that consumers honour at inference time. For the layout of logical outputs per architecture, see [Architecture Survey](#architecture-survey).

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
|---|---|---|
| YOLOv5  | C3              | Conv→Conv→Conv2d        |
| YOLOv8  | C2f             | Conv→Conv→Conv2d        |
| YOLO11  | C3k2, C2PSA     | DWConv→Conv (efficient) |
| YOLO26  | C3k2, A2C2f     | DWConv→Conv (efficient) |

### Decoder Version Field

The `decoder_version` field specifies the YOLO architecture version for Ultralytics models. This field is critical for determining the correct decoding strategy, especially for end-to-end models.

```yaml
decoder_version: yolo26    # End-to-end model with embedded NMS
# or
decoder_version: yolov8    # Traditional model requiring external NMS
```

**Supported values:**

| Value | Architecture | NMS Handling |
|---|---|---|
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
|---|---|
| `class_agnostic` | Suppress overlapping boxes regardless of class label (default) |
| `class_aware` | Only suppress boxes that share the same class AND overlap |

!!! warning "Two distinct `nms` fields"
    This document uses `nms` at two levels with different semantics:

    - **Root-level `nms`** (this field) — HAL decoder *behaviour*: `class_agnostic` vs `class_aware`.
    - **`validation.nms`** (see [Validation Parameters](#validation-parameters)) — NMS *implementation*: `hal`, `numpy`, `tensorflow`, `torch`, or `none`.

    The two fields are independent and can coexist.

---

## Split Hints

Split hints encode model-specific knowledge about where natural quantization boundaries exist within output tensors. The training framework identifies these boundaries based on its knowledge of the model architecture; the converter decides whether to apply them and how far to decompose beyond them.

### Lifecycle

Split hints are **input metadata only**. They live in the uncompiled (ONNX / SavedModel) `edgefirst.json` and are consumed by the converter. The compiled (converted) model **replaces** `split_hints` with the compiled `outputs[]` array — the two-layer logical/physical structure is the authoritative description of the compiled model.

```
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
|---|---|---|---|
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
|---|---|---|---|
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
|---|---|---|
| **Detection** | One `quantization_split` on output0 with `boxes` + `scores` boundaries | Per-component scales improve INT8 precision; boxes and scores have different distributions |
| **Segmentation** | One `quantization_split` on output0 with `boxes` + `scores` + `mask_coefs` boundaries | Mask coefficients (unbounded) especially benefit from their own scale |
| **End-to-end (YOLO26 `end2end: true`)** | None | Output is already post-NMS; nothing to split |
| **Single-output (BEV)** | None | Single output with uniform value distribution |

---

## Architecture Survey

Coverage of the two-layer output model across the detection, segmentation, and end-to-end architectures currently supported by the EdgeFirst ecosystem. The list grows as new architectures are onboarded — the two-layer model is general and accommodates additional families (SCRFD, EfficientDet, YOLACT, DETR variants, etc.) without schema changes.

| Architecture | Scales | Heads | Monolithic in ONNX? | Two-Layer Mapping |
|---|---|---|---|---|
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

Training frameworks produce a calibration artifact containing preprocessed, ready-to-consume calibration data. This artifact enables model-agnostic converters to perform quantization without knowing the model's preprocessing pipeline, input normalization, or data augmentation.

### Rationale

The training stage always generates calibration data because:

- The model knows its own preprocessing (normalization, resizing, color space, [CameraAdaptor](cameraadaptor.md))
- Multi-input models (e.g., camera + radar fusion) require model-specific preprocessing per input
- Smart sample selection (percentile bounds, coverage optimization) runs once at training time
- Converters become truly model-agnostic — they receive ready-to-consume tensors

### Format

Calibration data is stored in [safetensors](https://huggingface.co/docs/safetensors/) format with named tensors corresponding to model input names.

### Naming Convention

Calibration filenames encode the dataset and generation parameters for deterministic caching:

```
calibration-{dataset_id}-{param_hash}.safetensors
```

**Example:** `calibration-ds-2bcc-a1b2c3d4.safetensors`

- `{dataset_id}` — Studio dataset label (e.g., `ds-2bcc`)
- `{param_hash}` — Deterministic hash of the calibration generation parameters

### Parameter Hash

The parameter hash is computed from the inputs that determine calibration content. The hash is over the **parameters**, not the **content** — two trainers using the same parameters will produce the same hash even if they select different samples.

Parameters included in the hash:

| Parameter | Example | Why |
|---|---|---|
| Dataset ID | `ds-2bcc` | Which dataset |
| Annotation set ID | `as-1a3f` | Which annotation version |
| Validation group | `val` | Which split |
| Image size | `640x640` | Resize target |
| Preprocessing | `normalize_uint8`, `letterbox` | How pixels are transformed |
| CameraAdaptor | `rgb`, `yuyv`, `grey` | Color space / channel config |
| Calibration coverage | `10` | Percentage of validation set |
| Selection algorithm | `greedy_coverage_v1` | Algorithm version (invalidates cache on algorithm changes) |

The hash function and parameter serialization order are defined by each training framework but must be deterministic and consistent across runs.

### Storage: Studio Snapshots

Calibration artifacts are stored as **Studio snapshots**, not session artifacts. The filename is the cache key.

**Trainer workflow:**

1. Compute the parameter hash from calibration generation parameters
2. Build the filename: `calibration-{dataset_id}-{param_hash}.safetensors`
3. Look up the snapshot by filename via Studio API
4. If the snapshot exists → download and use it (skip generation)
5. If not → generate the calibration set, publish it as a snapshot with this filename

This means a calibration set is generated **once** for a given set of parameters. Subsequent training runs with the same dataset, preprocessing, and coverage reuse the cached snapshot automatically.

### Tensor Naming

Tensor names in the safetensors file **must match the model's input tensor names**. Converters load all tensors by name and feed them to the calibration generator.

#### Single-Input Model

For models with a single image input (e.g., Ultralytics detection or segmentation):

```
calibration-ds-2bcc-a1b2c3d4.safetensors:
  images: float32 [500, 3, 640, 640]    # [num_samples, channels, height, width]
```

- Tensor name `images` matches the model's input tensor name
- Samples are preprocessed identically to training/inference (normalized to [0.0, 1.0], resized, CameraAdaptor applied)
- Typical sample count: ~500 images (10% of validation set or 500, whichever is smaller)

#### Multi-Input Model

For models with multiple inputs (e.g., camera + radar fusion):

```
calibration-ds-2bcc-a1b2c3d4.safetensors:
  camera: float32 [500, 3, 360, 640]    # [num_samples, channels, height, width]
  radar:  float32 [500, 200, 128, 8]    # [num_samples, range_bins, doppler_bins, features]
```

- Each tensor name (`camera`, `radar`) matches the corresponding model input name
- Each input is preprocessed according to its own pipeline (image normalization for camera, range-doppler processing for radar)
- All inputs have the same number of samples (first dimension)

### Converter Usage

Converters consume the calibration artifact as follows:

1. Read `edgefirst.json` from the training session to get the calibration filename
2. Download the calibration snapshot by filename via Studio API
3. Load all tensors using any safetensors-compatible library
4. Match tensor names to model input names
5. Iterate over samples (first dimension) to feed the calibration generator

```python
from safetensors import safe_open

with safe_open(calibration_path, framework="numpy") as f:
    tensor_names = f.keys()
    num_samples = f.get_tensor(next(iter(tensor_names))).shape[0]

    for i in range(num_samples):
        feed_dict = {name: f.get_tensor(name)[i:i+1] for name in tensor_names}
        yield feed_dict  # Feed to TFLiteConverter representative_dataset or equivalent
```

---

## Converter Traceability

When a converter processes a model, it augments the existing `edgefirst.json` with a converter-specific section at the top level. This provides full traceability of all conversion steps applied to the model.

### Rules

- Converters **augment** — they never replace or remove existing fields in `edgefirst.json` except for `split_hints`, which is replaced by the compiled `outputs[]` array per the split-hints lifecycle.
- Each converter adds a top-level key named after itself (e.g., `"tflite_quantizer"`, `"neutron"`, `"ara2"`, `"hailo"`).
- The converter section records conversion parameters, version, and any decisions made during conversion.
- Multiple converter sections can coexist when a model passes through a pipeline chain (e.g., TFLite Quantizer followed by Neutron Converter).

### Converter Section Schema

Each converter section is a free-form object, but should include at minimum:

| Field | Type | Description |
|---|---|---|
| `version` | string | Converter app version |
| `timestamp` | string | ISO 8601 conversion timestamp |
| `task` | string | Studio batch task ID for this conversion step (e.g., `bt-3a1f`) |
| `splits_applied` | string[] | List of `split_hints[].type` values that were consumed |

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
|---|---|---|---|
| `producer_name` | "EdgeFirst ModelPack" | "EdgeFirst Ultralytics" | Identifies producing framework |
| `producer_version` | Package version | Package version | Version tracking |
| `graph.name` | Model name | Model name | Graph identification |
| `doc_string` | Description | Description | Human-readable description |

Custom metadata properties (all string values):

| Key | Content | Purpose |
|---|---|---|
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
  username: john.doe                    # User who initiated training
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
|---|---|---|---|---|---|
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
|---|---|---|---|---|---|
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
|---|---|---|---|---|---|
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
|---|---|---|---|---|---|
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
|---|---|---|---|---|---|---|
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
|---|---|---|---|---|---|---|
| boxes | [0, 4) | 4 | 12 | anchor | — | — |
| objectness | [4, 5) | 1 | 3 | — | sigmoid | — |
| scores | [5, 85) | 80 | 240 | — | sigmoid | obj_x_class |
| mask_coefs | [85, 117) | 32 | 96 | — | — | — |

Monolithic output0 shape: `[1, 351, 8400]`

### A.7 Summary Table

| Model | Task | Boundaries | output0 channels | anchors_per_cell | encoding | score_format |
|---|---|---|---|---|---|---|
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
