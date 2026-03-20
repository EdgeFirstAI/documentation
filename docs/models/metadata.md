# Model Metadata

This document describes the metadata schema embedded in EdgeFirst model files. Model metadata provides complete traceability for MLOps workflows and contains all information needed to decode model outputs for inference.

## Overview

EdgeFirst models embed metadata that enables:

- **Full Traceability**: Link any deployed model back to its [training session](../studio/models.md#training-sessions), [dataset](../datasets/index.md), and configuration in [EdgeFirst Studio](../studio/index.md)
- **Self-Describing Models**: Models contain all information needed for inference without external configuration files
- **Cross-Platform Compatibility**: Consistent schema across TFLite and ONNX formats
- **Third-Party Integration**: Any training framework can produce EdgeFirst-compatible models by following this schema
- **Converter Workflows**: Split hints and calibration artifacts enable model-agnostic conversion pipelines for quantization and target-specific compilation

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
    These metadata fields are automatically read and handled by [`edgefirst-validator`](validation/vision/user_managed.md) and the [EdgeFirst Perception Middleware](../perception/index.md). In most cases, developers don't need to worry about these details — the EdgeFirst ecosystem "Just Works." This documentation exists so developers understand what's happening under the hood when needed.

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

The EdgeFirst metadata schema is organized into logical sections. All sections are optional — third-party integrations can include only the sections relevant to their use case.

### Complete Schema Structure

```yaml
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
  split_decoder: boolean   # Whether decoder is external (see Split Decoder section)
  anchors: [[[int, int]]]  # Anchor boxes per output level
  # ... additional model-specific parameters

# Training Configuration
trainer:
  epochs: int              # Number of training epochs
  batch_size: int          # Training batch size
  weights: string          # Pretrained weights source
  checkpoint_path: string  # Where checkpoints were saved

optimizer:
  optimizer: string        # Optimizer type (adam, adamw, sgd)
  learning_rate: float     # Base learning rate
  weight_decay: float      # L2 regularization strength
  # ... additional optimizer parameters

augmentation:  # See Vision Augmentations documentation
  random_hflip: int        # Horizontal flip probability (0-100)
  random_mosaic: int       # Mosaic augmentation probability
  # ... additional augmentation parameters

validation:
  iou: float               # NMS IoU threshold
  score: float             # NMS score threshold
  nms: string              # NMS algorithm (none, numpy, hal, tensorflow, torch)
  normalization: string    # Input normalization (unsigned, signed)
  preprocessing: string    # Preprocessing method (resize, letterbox)
  skip_validation_steps: int  # Steps to skip between validations

export:  # See Quantization documentation for ModelPack and Ultralytics
  export: boolean          # Whether model was quantized
  export_input_type: string   # Input quantization type
  export_output_type: string  # Output quantization type
  calibration_samples: int    # Samples used for calibration

# Decoder Configuration (Ultralytics only)
decoder_version: string    # YOLO architecture version: yolov5, yolov8, yolo11, yolo26
nms: string                # NMS mode for HAL decoder: class_agnostic, class_aware

# Calibration Artifact (see Calibration Artifact section)
calibration: string          # Snapshot filename: calibration-{dataset_id}-{param_hash}.safetensors

# Split Hints (see Split Hints section)
split_hints:
  - type: string             # Hint type (e.g., "quantization_split")
    target: string           # Output tensor name this hint applies to
    input_dtype: string      # Suggested input quantization dtype
    output_dtype: string     # Suggested output quantization dtype
    description: string      # Human-readable purpose
    boundaries:              # Channel boundaries within the target tensor
      - name: string         #   Boundary region name
        channels: [int, int] #   Channel range [start, end) (exclusive end)

# Converter Traceability (see Converter Traceability section)
# Converter-specific sections are added at the top level by each converter
# Examples: "neutron": {...}, "ara2": {...}, "tflite_quantizer": {...}

# Output Specification (Critical for Inference)
outputs:
  - name: string           # Output tensor name
    index: int             # Tensor index
    output_index: int      # Output order
    shape: [int]           # Tensor shape
    dshape:                # Named dimensions as ordered array (see dshape section)
      - batch: int
      - height: int                 # For spatial outputs
      - width: int                  # For spatial outputs
      - num_features: int           # For detection outputs
      - num_boxes: int              # For detection outputs
      - padding: int                # For detection outputs
      - box_coords: int             # For detection outputs
      - num_classes: int            # For detection outputs
      - num_anchors_x_features: int # For detection outputs
      - num_protos: int             # For instance segmentation
    dtype: string          # Data type (float32, uint8, int8)
    type: string           # Semantic type (detection, segmentation, boxes, scores, masks, protos)
    decode: boolean        # Whether decoding is required
    decoder: string        # Decoder type: 'modelpack' or 'ultralytics'
    quantization:              # Quantization parameters (null if float model)
      scale: float or [float]  #   Scale factor(s). Scalar=per-tensor, array=per-channel
      zero_point: int or [int] #   Zero point(s). Omit for symmetric (see Quantization Parameters)
      axis: int                #   Per-channel dimension index (required when scale is array)
      dtype: string            #   Quantized type: int8, uint8, int16, uint16, float16
    stride: [int, int]     # Spatial stride for this output (ModelPack)
    anchors: [[[float, float]]]  # Normalized anchors for this output level (ModelPack only)
    score_format: string   # Score encoding: 'per_class' or 'obj_x_class' (Ultralytics only)
    normalized: boolean    # Box coordinates in [0,1] range (true) or pixels (false). Optional field.
```

---

## Output Specification

The `outputs` section is critical for inference — it tells the runtime how to interpret model outputs.

### Output Types

For Ultralytics framework models, the following output types are used:


| Type                  | Description                                  | Typical Shape                    |
| --------------------- | -------------------------------------------- | -------------------------------- |
| `detection`         | Raw detection output (needs to be split)     | `[1, num_features, num_boxes]` |
| `boxes`             | Split bounding boxes                         | `[1, 4, num_boxes]`            |
| `scores`            | Split class scores                           | `[1, num_classes, num_boxes]`  |
| `classes`           | Class label indices (end-to-end split models) | `[1, num_boxes, 1]`           |
| `mask_coefficients` | Split coefficients for instance segmentation | `[1, num_protos, num_boxes]`   |
| `protos`            | Instance segmentation prototypes             | `[1, H, W, num_protos]` (NHWC) |

**`score_format` field** (Ultralytics only):

| Value | Description | Architecture |
|-------|-------------|--------------|
| `per_class` | Each anchor outputs `[nc]` class probabilities directly | YOLOv8, YOLO11, YOLO26 |
| `obj_x_class` | Each anchor outputs `[1 + nc]` where final score = objectness × class confidence | YOLOv5 |

When `score_format` is absent, the validator falls back to a shape-based heuristic on the feature dimension: `nc+5` features per anchor (4 box coordinates + 1 objectness + `nc` class probabilities) implies `obj_x_class` (e.g., `[1, 85, 8400]` for 80 classes).

!!! note "HAL Score Format"
    HAL determines score format from `decoder_version` rather than `score_format`. `yolov5` applies objectness × class; all other versions use per-class scores directly.

For ModelPack framework models the following output types are used:

| Type             | Description                           | Typical Shape                             |
| ---------------- | ------------------------------------- | ----------------------------------------- |
| `detection`    | Raw detection output (needs decoding) | `[1, H, W, num_anchors_x_features]` |
| `boxes`        | Bounding boxes                        | `[1, num_boxes, 1, 4]`                  |
| `scores`       | Class scores                          | `[1, num_boxes, num_classes]`           |
| `segmentation` | Semantic segmentation output          | `[1, H, W, num_classes]`               |
| `masks`        | Semantic segmentation masks           | `[1, H, W]`                             |

### Segmentation Types

EdgeFirst supports two distinct segmentation approaches:

#### Semantic Segmentation (ModelPack)

Per-pixel classification **without object instances**. Each pixel is assigned a class label, but individual objects are not distinguished.

**Use cases:**

- Drivable surface detection
- Lane segmentation
- Sky/ground separation
- Terrain classification

**Output structure:**

```yaml
outputs:
  - name: "segmentation_output"
    type: segmentation
    shape: [1, 480, 640, 5]    # [batch, H, W, num_classes]
    dshape:
      - batch: 1
      - height: 480
      - width: 640
      - num_classes: 5
    decoder: modelpack
```

#### Instance Segmentation (Ultralytics)

Per-pixel classification **with object instances**. Each detected object gets its own mask, enabling fine-grained object boundaries beyond bounding boxes.

**Use cases:**

- Individual person segmentation
- Vehicle instance masks
- Product segmentation
- Fine-grained object detection

**Output structure:**

```yaml
# Detection output with mask coefficients
outputs:
  - name: "detection_output"
    type: detection
    shape: [1, 116, 8400]      # [batch, 4+nc+32, num_boxes] - includes 32 mask coefficients
    dshape:
      - batch: 1
      - num_features: 116        # 4 box coords + 80 classes + 32 mask coefficients
      - num_boxes: 8400
    decoder: ultralytics

  # Prototype masks for instance computation
  - name: "protos_output"
    type: protos
    shape: [1, 32, 160, 160]   # [batch, num_protos, H, W] NCHW
    dshape:
      - batch: 1
      - num_protos: 32
      - height: 160
      - width: 160
    decoder: ultralytics
```

**Final mask computation:**

```python
# For each detected object with mask_coefficients [32]:
instance_mask = sigmoid(mask_coefficients @ protos)  # [32] @ [32, H, W] → [H, W]
# Crop to bounding box region for final instance mask
```

### The `dshape` Field

The `dshape` field provides **named dimensions** for easier interpretation of tensor shapes. This is especially useful when shapes vary between data layouts (NCHW vs NHWC).

```yaml
outputs:
  - name: "output_0"
    shape: [1, 84, 8400]       # Raw shape
    dshape:                    # Named dimensions as ordered array
      - batch: 1
      - num_features: 84         # 4 box coords + 80 classes
      - num_boxes: 8400
```

**Standard dimension names:**

| Name                       | Description                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------- |
| `batch`                  | Batch size (typically 1 for inference)                                                            |
| `height`                 | Spatial height                                                                                    |
| `width`                  | Spatial width                                                                                     |
| `num_classes`            | Number of classification classes                                                                  |
| `num_features`           | Feature dimension (box coords + classes + mask coefficients)                                      |
| `num_boxes`              | Number of detection boxes/anchors                                                                 |
| `num_protos`             | Number of prototype masks (instance segmentation)                                                 |
| `num_anchors_x_features` | Combined anchor and feature dimension for ModelPack grid outputs (anchors × features per anchor)  |
| `padding`                | Padding/alignment dimension used to satisfy expected tensor shapes. Must always be 1              |
| `box_coords`             | The coordinates of the boxes. Must be 4                                                           |

### Decoding Information

For outputs with `decode: true`, the metadata provides all information needed to decode:

```yaml
outputs:
  - name: "detection_output_0"
    type: detection
    decode: true
    decoder: modelpack
    shape: [1, 40, 40, 54]      # Grid output
    dshape:
      - batch: 1
      - height: 40
      - width: 40
      - num_anchors_x_features: 54
    anchors:                    # Normalized anchor boxes
      - [0.054, 0.065]
      - [0.089, 0.139]
      - [0.195, 0.196]
    quantization:               # For dequantization
      scale: 0.176
      zero_point: 198
      dtype: uint8
```

### Quantization Parameters

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

#### Quantization Object Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
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

#### Examples

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

#### Dequantization Code

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

#### Framework Conventions

| Framework | Per-Tensor | Per-Channel | Symmetric | Axis Field |
|-----------|-----------|-------------|-----------|------------|
| ONNX | Scalar scale | 1-D scale + `axis` | Implicit (zero_point=0) | `axis` (default 1) |
| TFLite/LiteRT | Scalar (1-element array) | 1-D scale + `quantized_dimension` | Implicit (zero_point=0 for weights) | `quantized_dimension` |
| TensorRT | Scalar scale | Per-channel scale | Always symmetric | Output channel axis |
| PyTorch | Scalar scale | 1-D scale + `axis` | Explicit `qscheme` enum | `axis` parameter |

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

The metadata's `outputs` section reports shapes in the model's native format. When integrating with inference runtimes, ensure your input preprocessing matches the expected layout.

### Metadata Fields

```yaml
input:
  shape: [1, 640, 640, 3]  # Input tensor shape (layout varies by model)
  cameraadaptor: rgb       # Channel order (rgb, bgr, yuyv)
  # Common layouts:
  # - NHWC: [batch, height, width, channels] e.g., [1, 640, 640, 3]
  # - NCHW: [batch, channels, height, width] e.g., [1, 3, 640, 640]

outputs:
  - name: "output_0"
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
|-------|-------------|---------------|
| `rgb` | Standard RGB | Red, Green, Blue |
| `bgr` | OpenCV default | Blue, Green, Red |
| `rgba` | RGB with alpha | Red, Green, Blue, Alpha |
| `bgra` | BGR with alpha | Blue, Green, Red, Alpha |
| `grey` | Greyscale | Single channel |
| `yuyv` | YUV 4:2:2 packed | For direct camera sensor input |

---

## Validation Parameters

The `validation` section records the recommended settings based on how the model was trained. These parameters are **informational preferences** — they document the model author's intended configuration for validation and inference.

### Parameter Semantics

| Parameter | Description | Default | Override at Runtime? |
|-----------|-------------|---------|---------------------|
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
|-------|-------------|
| `none` | No external NMS. For models with embedded NMS — either architectural end-to-end (YOLO26) or engine-embedded (ONNX/TRT/TFLite with NMS ops appended). Supports both detection and segmentation |
| `numpy` | NumPy-based NMS implementation (default fallback) |
| `hal` | EdgeFirst HAL decoder NMS |
| `tensorflow` | TensorFlow NMS |
| `torch` | PyTorch (torchvision) NMS |

When `--override` is set, the validator reads `validation.nms` from the model metadata and applies it automatically.

### Box Coordinate Format (`normalized`)

The `normalized` field on detection and boxes outputs specifies the coordinate format:

| Value | Description | Coordinate Range |
|-------|-------------|------------------|
| `true` | Normalized coordinates relative to model input dimensions | `[0.0, 1.0]` |
| `false` | Pixel coordinates relative to model input (letterboxed frame) | `[0, width]` / `[0, height]` |
| *(absent)* | Must be inferred from output values | Check if any coordinate > 1.0 |

**When `normalized` is absent**, the coordinate format must be inferred by examining the output values. If any bounding box coordinate exceeds `1.0`, the coordinates are in pixels; otherwise, assume normalized.

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
# Example: End-to-end model with pixel coordinates
outputs:
  - name: "output0"
    type: detection
    shape: [1, 100, 6]    # [batch, max_det, x1+y1+x2+y2+conf+class]
    normalized: false      # Pixel coordinates
    decoder: ultralytics
```

---

## Post-Processing & Split Decoder

### What is Split Decoder?

The `split_decoder` field indicates the model's outputs have been modified from the standard architecture to improve INT8 quantization performance. The details are framework-specific:

- **ModelPack**: Raw grid features instead of decoded boxes (dequantize before anchor decode)
- **Ultralytics**: Detection tensor split into separate tensors for per-tensor quantization — `boxes` and `scores` for detection (2 outputs), or `boxes`, `scores`, `mask_coefficients`, and `protos` for segmentation (4 outputs). Box coordinates are normalized to [0,1]

```yaml
model:
  split_decoder: true    # Outputs modified for quantization (see framework docs)
  split_decoder: false   # Standard output format
```

See framework documentation for implementation details.

### Why Split Decoder Exists

Quantization introduces precision loss. Split decoder addresses this differently per framework:

**[ModelPack](modelpack/index.md)**: For small objects or high-resolution inputs, applying anchor calculations in INT8 would compound rounding errors. By deferring decoding until after dequantization, we preserve box accuracy.

**[Ultralytics](ultralytics/index.md)**: The monolithic detection tensor contains boxes, scores, and mask coefficients with very different value ranges. Splitting them into separate tensors allows per-tensor quantization scales, preserving accuracy for each component independently. Box coordinates are normalized to [0,1] for both detection and segmentation, which reduces the dynamic range and further improves INT8 quantization accuracy. See [Ultralytics Quantization](ultralytics/quantize.md) for details and accuracy benchmarks.

### Decoding Process

When `split_decoder: true`, the inference pipeline must:

1. **Run model inference** → Get quantized outputs
2. **Dequantize outputs** → Convert INT8 to float32 using per-output scale/zero_point
3. **Apply decoding** → Framework-specific: anchor decode (ModelPack) or box format conversion (Ultralytics)
4. **Run NMS** → Filter overlapping detections

```python
# Example decoding flow for split_decoder models
for output_spec in metadata['outputs']:
    if output_spec.get('decode', False):
        # Dequantize first
        quant = output_spec['quantization']
        scale = np.float32(quant['scale'])
        zp = quant.get('zero_point', 0)
        raw_float = (raw_int8.astype(np.float32) - zp) * scale
        # For per-channel quantization, use the dequantize() function above

        # Then decode (framework-specific)
        if output_spec['decoder'] == 'modelpack':
            boxes = decode_yolo_grid(raw_float, output_spec['anchors'], output_spec['stride'])
        elif output_spec['decoder'] == 'ultralytics':
            # boxes, scores, mask_coefficients are separate outputs
            pass  # Use output type to determine handling
```

### Output Types with Split Decoder

| Framework | `split_decoder` | Task | Output Types |
|-----------|-----------------|------|--------------|
| ModelPack | `true` | Detection | `detection` (raw grid, needs anchor decode) |
| ModelPack | `false` | Detection | `boxes`, `scores` (decoded) |
| Ultralytics | `true` | Detection | `boxes`, `scores` |
| Ultralytics | `true` | Segmentation | `boxes`, `scores`, `mask_coefficients`, `protos` |
| Ultralytics | `false` | Detection | `detection` (monolithic) |
| Ultralytics | `false` | Segmentation | `detection`, `protos` (monolithic) |
| Ultralytics (end-to-end) | n/a | Detection | `boxes`, `scores`, `classes` |
| Ultralytics (end-to-end) | n/a | Segmentation | `boxes`, `scores`, `classes`, `mask_coefficients`, `protos` |

### Decoder Field

The `decoder` field specifies which decoding algorithm to use:

```yaml
outputs:
  - name: "detection_output_0"
    type: detection
    decode: true
    decoder: modelpack    # Use ModelPack YOLO-style grid decoding
```

#### Supported Decoders

##### `modelpack` — Anchor-Based YOLO Decoder

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

**Required metadata fields:**

```yaml
outputs:
  - decoder: modelpack
    anchors:              # Required - normalized anchor boxes
      - [0.054, 0.065]
      - [0.089, 0.139]
    stride: [16, 16]      # Required - spatial stride
```

!!! warning "Deprecated: `decoder: yolov8`"
    The decoder value `yolov8` is deprecated. Use `ultralytics` instead. Existing models with `decoder: yolov8` will continue to work — the validator automatically normalizes `yolov8` to `ultralytics` with a deprecation warning.

##### `ultralytics` — Anchor-Free DFL Decoder

Used by [Ultralytics](ultralytics/index.md) models (YOLOv5, YOLOv8, YOLO11, YOLO26). Modern anchor-free detection using Distribution Focal Loss (DFL).

**Characteristics:**

- **Anchor-free**: Uses anchor points (grid centers) instead of pre-defined boxes
- **DFL regression**: Converts 16-bin distribution to box coordinates
- **Unified architecture**: Same decoder for YOLOv5, YOLOv8, YOLO11, and YOLO26

**Decoding formula:**

```python
# DFL converts 16-bin distribution to coordinate value
box = dfl(raw_box)  # [batch, 64, anchors] → [batch, 4, anchors]

# dist2bbox converts LTRB distances to boxes
x1y1 = anchor_points - lt
x2y2 = anchor_points + rb
# Returns xywh in pixel coordinates (ONNX float) or [0,1] normalized (TFLite INT8)
```

**Metadata structure:**

```yaml
outputs:
  - decoder: ultralytics
    anchors: null         # Not used - anchor-free
    # Strides are implicit: [8, 16, 32] for P3/P4/P5 outputs
```

**Version differences:**
All Ultralytics versions use the same anchor-free `Detect` class. Differences are in backbone architecture:

| Version | Backbone Blocks | Classification Head |
|---------|-----------------|---------------------|
| YOLOv5  | C3              | Conv→Conv→Conv2d    |
| YOLOv8  | C2f             | Conv→Conv→Conv2d    |
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
|-------|--------------|--------------|
| `yolov5` | YOLOv5 | External NMS required |
| `yolov8` | YOLOv8 | External NMS required |
| `yolo11` | YOLO11 | External NMS required |
| `yolo26` | YOLO26 | Embedded NMS (end-to-end) |

!!! note "Naming Convention"
    The naming follows Ultralytics conventions: `yolov5` and `yolov8` include the 'v' prefix, while `yolo11` and `yolo26` do not (Ultralytics dropped the 'v' starting with YOLO11).

**When `decoder_version` is `yolo26`:**

- The model uses one-to-one matching heads with NMS embedded in the architecture
- Output format is `[x1, y1, x2, y2, conf, class, ...]` (post-NMS)
- The HAL decoder uses end-to-end model types regardless of the `nms` field
- No external NMS is applied

**When `decoder_version` is absent or any other value:**

- Traditional YOLO architecture requiring external NMS
- The `nms` field controls which NMS algorithm the HAL decoder uses

### HAL NMS Field

The `nms` field at the config root level controls the HAL decoder's NMS behavior:

```yaml
nms: class_agnostic    # Suppress overlapping boxes regardless of class (default)
# or
nms: class_aware       # Only suppress boxes with the same class label
```

| Value | Behavior |
|-------|----------|
| `class_agnostic` | Suppress overlapping boxes regardless of class label (default) |
| `class_aware` | Only suppress boxes that share the same class AND overlap |

!!! warning "Different from `validation.nms`"
    The root-level `nms` field controls **HAL decoder behavior** (class-agnostic vs class-aware). The `validation.nms` field in the validation section specifies the **NMS implementation** to use during validation (hal, numpy, tensorflow, etc.) or `none` for models with embedded NMS.

**Example configuration for YOLO26 end-to-end model:**

```yaml
decoder_version: yolo26
outputs:
  - decoder: ultralytics
    type: detection
    shape: [1, 100, 6]
    normalized: false
    dshape:
      - batch: 1
      - num_boxes: 100
      - num_features: 6
validation:
  nms: none    # Model has embedded NMS
```

**Example configuration for traditional YOLOv8 model:**

```yaml
decoder_version: yolov8
nms: class_agnostic
outputs:
  - decoder: ultralytics
    type: detection
    shape: [1, 84, 8400]
    dshape:
      - batch: 1
      - num_features: 84
      - num_boxes: 8400
validation:
  nms: hal    # Use HAL decoder NMS
```

---

## ONNX-Specific Metadata

ONNX models exported from [ModelPack](modelpack/index.md) or [Ultralytics](ultralytics/index.md) include additional official metadata fields:

| Field | ModelPack Value | Ultralytics Value | Purpose |
|-------|-----------------|-------------------|---------|
| `producer_name` | "EdgeFirst ModelPack" | "EdgeFirst Ultralytics" | Identifies producing framework |
| `producer_version` | Package version | Package version | Version tracking |
| `graph.name` | Model name | Model name | Graph identification |
| `doc_string` | Description | Description | Human-readable description |

Custom metadata properties (all string values):

| Key | Content | Purpose |
|-----|---------|---------|
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
input:
  shape: [1, 640, 640, 3]  # Input tensor shape (NHWC or NCHW)
  cameraadaptor: rgb

model:
  detection: true
  segmentation: false
  split_decoder: true  # or false if decoder is built-in

outputs:
  - name: "output_0"
    shape: [1, 8400, 84]
    dtype: float32
    type: boxes  # or detection if needs decoding
    decode: false

dataset:
  classes:
    - class1
    - class2
```

### Full Traceability (Recommended)

For production MLOps integration with [EdgeFirst Studio](../studio/index.md):

```yaml
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
  split_decoder: true    # true = outputs need anchor decoding after dequantization
                         # false = outputs are fully decoded boxes
                         # See "Post-Processing & Split Decoder" section for details
  anchors:               # Per-level anchor boxes (pixels at input resolution)
    - [[35, 42], [57, 89], [125, 126]]
    - [[125, 126], [208, 260], [529, 491]]

# Ultralytics model configuration
model:
  model_version: v8      # v5, v8, v11
  model_task: segment    # detect, segment
  model_size: n          # n (nano), s (small), m (medium), l (large), x (xlarge)
  detection: false
  segmentation: true
  split_decoder: true    # true = split outputs for per-tensor INT8 quantization
                         #   Detection: boxes, scores (2 outputs)
                         #   Segmentation: boxes, scores, mask_coefficients, protos (4 outputs)
                         # false = monolithic detection tensor
                         # Default true for all quantized TFLite models
```

### Outputs Section

```yaml
# ModelPack detection output example
outputs:
  - name: "output_0"
    index: 0
    output_index: 0
    shape: [1, 40, 40, 54]
    dshape:
      - batch: 1
      - height: 40
      - width: 40
      - num_anchors_x_features: 54   # 3 anchors × (5 + 13 classes)
    dtype: float32
    type: detection
    decode: true
    decoder: modelpack
    quantization:
      scale: 0.176
      zero_point: 198
      dtype: uint8
    stride: [16, 16]
    anchors:
      - [0.054, 0.065]
      - [0.089, 0.139]
      - [0.195, 0.196]

# Ultralytics detection output example  
outputs:
  - name: "output0"
    index: 0
    output_index: 0
    shape: [1, 84, 8400]           # NCHW: [batch, 4+nc, num_boxes]
    dshape:
      - batch: 1
      - num_features: 84             # 4 box coords + 80 classes
      - num_boxes: 8400
    dtype: float32
    type: detection
    decode: true
    decoder: ultralytics
    quantization: null             # Float model
    anchors: null                  # Anchor-free
    score_format: per_class        # YOLOv8/v11/v26: class probabilities directly

# Ultralytics instance segmentation protos example
  - name: "output1"
    index: 1
    output_index: 1
    shape: [1, 32, 160, 160]       # NCHW: [batch, protos, H, W]
    dshape:
      - batch: 1
      - num_protos: 32
      - height: 160
      - width: 160
    dtype: float32
    type: protos
    decode: true
    decoder: ultralytics
    quantization: null
    anchors: null
    score_format: null             # Not applicable to protos output
```

---

## Split Hints

Split hints encode model-specific knowledge about where natural quantization boundaries exist within output tensors. The training framework identifies these boundaries based on its knowledge of the model architecture; the converter decides whether to apply them.

### Purpose

When a single output tensor contains channels with different value distributions (e.g., [0,1]-bounded box coordinates alongside unbounded linear projections), a shared quantization scale degrades accuracy. Split hints tell converters where these natural boundaries exist so they can apply independent quantization scales to each region.

### Schema Governance

Hint types are defined in this schema documentation. The schema defines the vocabulary of hint types, their structure, and their semantics. Training frameworks populate hints according to this vocabulary. Converter UIs are built against the schema vocabulary, not against hints in any particular model.

### `split_hints` Array

The `split_hints` field is a top-level array in `edgefirst.json`. Each element describes one hint.

```yaml
split_hints:
  - type: string             # Hint type identifier (see Hint Types below)
    target: string           # Output tensor name this hint applies to (e.g., "output0")
    input_dtype: string      # Suggested input quantization dtype (e.g., "uint8")
    output_dtype: string     # Suggested output quantization dtype (e.g., "int8")
    description: string      # Human-readable purpose of this split
    boundaries:              # Channel boundary definitions
      - name: string         #   Region name (e.g., "detection", "mask_coefs")
        channels: [int, int] #   Channel range [start, end) — exclusive end index
```

#### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Hint type identifier. Converters ignore types they do not understand |
| `target` | string | Yes | Name of the output tensor this hint applies to (must match an entry in `outputs`) |
| `input_dtype` | string | No | Suggested input quantization dtype (e.g., `uint8`, `float32`). Converter default, overridable by user |
| `output_dtype` | string | No | Suggested output quantization dtype (e.g., `int8`, `float32`). Converter default, overridable by user |
| `description` | string | No | Human-readable description of why this split boundary exists |
| `boundaries` | array | Yes | Ordered list of channel regions within the target tensor |
| `boundaries[].name` | string | Yes | Identifier for this region (used in split output naming) |
| `boundaries[].channels` | [int, int] | Yes | Channel range as `[start, end)` with exclusive end index |

### Behavior Rules

- `split_hints` is an array — multiple hints can coexist (e.g., one per output tensor)
- Each hint has a `type` field — converters **must ignore** types they do not understand (forward compatibility)
- Converter UI presents all known split types from this schema as options
- If the user enables a split type and matching hints exist in the model, the converter applies them
- If the user enables a split type and no matching hints exist, the converter warns (not an error) and proceeds without splitting
- Hints include suggested quantization defaults (`input_dtype`, `output_dtype`) that converters use as UI defaults; the user can override them
- Boundary `channels` ranges must be non-overlapping and cover the full channel dimension of the target tensor when taken together

### Hint Types

#### `quantization_split`

Channel boundaries within an output tensor that have different value distributions and benefit from independent quantization scales. The converter applies graph surgery to split the tensor at the specified boundaries, then quantizes each resulting tensor independently.

**Example: Ultralytics segmentation model**

The monolithic detection output `[1, 116, 8400]` contains 84 detection channels ([0,1]-bounded boxes + scores) and 32 mask coefficient channels (unbounded linear projection). Splitting at channel 84 allows independent quantization scales:

```yaml
split_hints:
  - type: "quantization_split"
    target: "output0"
    input_dtype: "uint8"
    output_dtype: "int8"
    description: "Separate mask coefficients from detection channels for independent quantization"
    boundaries:
      - name: "detection"
        channels: [0, 84]       # boxes (4) + class scores (80), [0,1] bounded
      - name: "mask_coefs"
        channels: [84, 116]     # mask coefficient linear projection, unbounded
```

#### `decoder_offload` (future)

!!! note "Planned"
    This hint type is reserved for future use. It is documented here to establish the schema vocabulary. Converters should ignore this type until a future schema revision provides the full specification.

Boundary where decoder layers can be removed from the quantized graph and run externally in float32. This is relevant for models where the decoder (e.g., anchor decode, DFL softmax) suffers disproportionate quantization loss compared to the backbone and neck.

#### `cpu_npu_boundary` (future)

!!! note "Planned"
    This hint type is reserved for future use. It is documented here to establish the schema vocabulary. Converters should ignore this type until a future schema revision provides the full specification.

Suggested partition point for heterogeneous execution across CPU and NPU. The training framework identifies layers that are NPU-friendly (convolutions, dense) versus layers that benefit from CPU execution (complex activations, dynamic shapes).

### Per-Task Split Recommendations

Based on quantization experiments:

| Task | Hints | Rationale |
|------|-------|-----------|
| **Detection** | No `split_hints` | Combined output `[1, nc+4, N]` quantizes effectively — boxes and scores are both in [0,1] range |
| **Segmentation** | One `quantization_split` on output0 | Boxes+scores ([0,1] bounded) share a scale without penalty; mask coefficients (unbounded) need their own scale |
| **Single-output (BEV)** | No `split_hints` | Single output with uniform value distribution |

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
|-----------|---------|-----|
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

- Converters **augment** — they never replace or remove existing fields in `edgefirst.json`
- Each converter adds a top-level key named after itself (e.g., `"tflite_quantizer"`, `"neutron"`, `"ara2"`)
- The converter section records conversion parameters, version, and any decisions made during conversion
- Multiple converter sections can coexist when a model passes through a pipeline chain (e.g., TFLite Quantizer followed by Neutron Converter)

### Converter Section Schema

Each converter section is a free-form object, but should include at minimum:

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Converter app version |
| `timestamp` | string | ISO 8601 conversion timestamp |
| `task` | string | Studio batch task ID for this conversion step (e.g., `bt-3a1f`) |

Additional fields are converter-specific and documented by each converter app.

### Example: Single Converter

After TFLite quantization of an Ultralytics detection model:

```json
{
  "host": { "studio_server": "test.edgefirst.studio", "..." : "..." },
  "model": { "..." : "..." },
  "outputs": [ "..." ],
  "split_hints": [ "..." ],

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
  "host": { "..." : "..." },
  "model": { "..." : "..." },
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

## Related Articles

1. [Camera Adaptor](cameraadaptor.md) - Native camera format support for edge deployment
2. [ModelPack Overview](modelpack/index.md) - Architecture details and training parameters
3. [Ultralytics Integration](ultralytics/index.md) - YOLOv8/v11/v26 training and deployment
4. [Training Vision Models](training/vision.md) - Step-by-step training workflow
5. [On Cloud Validation](validation/vision/managed.md) - Managed validation sessions
6. [On Target Validation](validation/vision/user_managed.md) - User-managed validation with `edgefirst-validator`
7. [ModelPack Quantization](modelpack/quantize.md) - Converting ONNX to quantized TFLite
8. [Deploying to Embedded Targets](deployment/evk.md) - Model deployment workflow
9. [EdgeFirst Perception Middleware](../perception/index.md) - Runtime inference stack
10. [Dataset Zoo](../datasets/index.md) - Available datasets for training
11. [Model Experiments Dashboard](../studio/models.md) - Managing training and validation sessions
