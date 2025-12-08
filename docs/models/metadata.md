# Model Metadata

This document describes the metadata schema embedded in EdgeFirst model files. Model metadata provides complete traceability for MLOps workflows and contains all information needed to decode model outputs for inference.

## Overview

EdgeFirst models embed metadata that enables:

- **Full Traceability**: Link any deployed model back to its [training session](../studio/models.md#training-sessions), [dataset](../datasets/index.md), and configuration in [EdgeFirst Studio](../studio/index.md)
- **Self-Describing Models**: Models contain all information needed for inference without external configuration files
- **Cross-Platform Compatibility**: Consistent schema across TFLite and ONNX formats
- **Third-Party Integration**: Any training framework can produce EdgeFirst-compatible models by following this schema

### Supported Formats

EdgeFirst models from the [Model Zoo](index.md) (including [ModelPack](modelpack/index.md) and [Ultralytics](ultralytics/index.md)) embed metadata in format-specific locations:

| Format | Metadata Location | Config Format | Labels |
|--------|-------------------|---------------|--------|
| TFLite | ZIP archive (associated files) | `edgefirst.yaml` | `labels.txt` |
| ONNX | Custom metadata properties | `edgefirst` (JSON) | `labels` (JSON array) |

### Supported Training Frameworks

| Framework | Decoder | Architecture | Use Case |
|-----------|---------|--------------|----------|
| [ModelPack](modelpack/index.md) | `modelpack` | Anchor-based YOLO | Semantic segmentation, detection |
| [Ultralytics](ultralytics/index.md) | `ultralytics` | Anchor-free DFL (YOLOv5/v8/v11) | Instance segmentation, detection |

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
| `studio_server` | `host.studio_server` | Which [EdgeFirst Studio](../studio/index.md) instance (dev, test, stage, saas) |
| `session_id` | `host.session` | [Training session](../studio/models.md#training-sessions) ID for accessing logs, metrics, artifacts |
| `dataset_id` | `dataset.id` | [Dataset](../datasets/index.md) identifier for reproducing training data |
| `dataset` | `dataset.name` | Human-readable dataset name |

### Example Traceability Workflow

Given a deployed model, you can trace back to its origins:

```python
# Extract metadata from deployed model
metadata = get_edgefirst_metadata(model_path)

# Construct EdgeFirst Studio URLs
server = metadata['host']['studio_server']  # e.g., 'saas'
session = metadata['host']['session']       # e.g., 't-abc123'
dataset_id = metadata['dataset']['id']      # e.g., 'ds-xyz789'

# Access training session: https://{server}.edgefirst.ai/training/{session}
# Access dataset: https://{server}.edgefirst.ai/datasets/{dataset_id}
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

TFLite models are ZIP-format files containing embedded `edgefirst.yaml` and `labels.txt`:

```python
import zipfile
import yaml

def get_edgefirst_metadata(model_path: str) -> dict | None:
    """Extract EdgeFirst metadata from a TFLite model."""
    if not zipfile.is_zipfile(model_path):
        return None
    
    with zipfile.ZipFile(model_path) as zf:
        # Try JSON first (preferred), then YAML fallback
        for filename in ['edgefirst.json', 'edgefirst.yaml']:
            if filename in zf.namelist():
                with zf.open(filename) as f:
                    content = f.read().decode('utf-8')
                    if filename.endswith('.json'):
                        import json
                        return json.loads(content)
                    else:
                        return yaml.safe_load(content)
    return None

def get_labels(model_path: str) -> list[str]:
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

def get_edgefirst_metadata(model_path: str) -> dict | None:
    """Extract EdgeFirst metadata from an ONNX model."""
    model = onnx.load(model_path)
    
    for prop in model.metadata_props:
        if prop.key == 'edgefirst':
            return json.loads(prop.value)
    return None

def get_labels(model_path: str) -> list[str]:
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
  studio_server: string    # EdgeFirst Studio server (dev/test/stage/saas)
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
  size: string             # Input resolution as "WIDTHxHEIGHT"
  color_adaptor: string    # Color format (rgb, rgba, yuyv)

model:
  backbone: string         # Backbone architecture (e.g., cspdarknet19, cspdarknet53)
  model_size: string       # Size variant (nano, small, medium, large)
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
  validation_iou: float    # NMS IoU threshold
  validation_threshold: float  # NMS score threshold

export:  # See Quantization documentation for ModelPack and Ultralytics
  export: boolean          # Whether model was quantized
  export_input_type: string   # Input quantization type
  export_output_type: string  # Output quantization type
  calibration_samples: int    # Samples used for calibration

# Output Specification (Critical for Inference)
outputs:
  - name: string           # Output tensor name
    index: int             # Tensor index
    output_index: int      # Output order
    shape: [int]           # Tensor shape
    dshape:                # Named dimensions (see dshape section)
      batch: int
      height: int          # For spatial outputs
      width: int           # For spatial outputs
      num_features: int    # For detection outputs
      num_boxes: int       # For detection outputs
      num_protos: int      # For instance segmentation
      num_classes: int     # For semantic segmentation
    dtype: string          # Data type (float32, uint8, int8)
    type: string           # Semantic type (detection, segmentation, boxes, scores, masks, protos)
    decode: boolean        # Whether decoding is required
    decoder: string        # Decoder type: 'modelpack' or 'ultralytics'
    quantization: [float, int]  # [scale, zero_point] for quantized models
    stride: [int, int]     # Spatial stride for this output (ModelPack)
    anchors: [[[float, float]]]  # Normalized anchors for this output level (ModelPack only)
```

---

## Output Specification

The `outputs` section is critical for inference — it tells the runtime how to interpret model outputs.

### Output Types

| Type | Description | Typical Shape | Framework |
|------|-------------|---------------|-----------|
| `detection` | Raw detection output (needs decoding) | `[1, num_features, num_boxes]` | Both |
| `boxes` | Decoded bounding boxes | `[1, N, 4]` | ModelPack |
| `scores` | Decoded class scores | `[1, N, classes]` | ModelPack |
| `segmentation` | Semantic segmentation output | `[1, H, W, classes]` | ModelPack |
| `masks` | Semantic segmentation masks | `[1, H, W]` or `[1, H, W, classes]` | ModelPack |
| `protos` | Instance segmentation prototypes | `[1, num_protos, H, W]` (NCHW) | Ultralytics |

### Segmentation Types

EdgeFirst supports two distinct segmentation approaches:

#### Semantic Segmentation (ModelPack)

Per-pixel classification **without object instances**. Each pixel is assigned a class label, but individual objects are not distinguished.

**Use cases:**

- Driveable surface detection
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
      batch: 1
      height: 480
      width: 640
      num_classes: 5
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
      batch: 1
      num_features: 116        # 4 box coords + 80 classes + 32 mask coefficients
      num_boxes: 8400
    decoder: ultralytics

  # Prototype masks for instance computation
  - name: "protos_output"
    type: protos
    shape: [1, 32, 160, 160]   # [batch, num_protos, H, W] NCHW
    dshape:
      batch: 1
      num_protos: 32
      height: 160
      width: 160
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
    dshape:                    # Named dimensions
      batch: 1
      num_features: 84         # 4 box coords + 80 classes
      num_boxes: 8400
```

**Standard dimension names:**

| Name | Description |
|------|-------------|
| `batch` | Batch size (typically 1 for inference) |
| `height` | Spatial height |
| `width` | Spatial width |
| `num_classes` | Number of classification classes |
| `num_features` | Feature dimension (box coords + classes + mask coefficients) |
| `num_boxes` | Number of detection boxes/anchors |
| `num_protos` | Number of prototype masks (instance segmentation) |

### Decoding Information

For outputs with `decode: true`, the metadata provides all information needed to decode:

```yaml
outputs:
  - name: "detection_output_0"
    type: detection
    decode: true
    decoder: modelpack
    shape: [1, 40, 40, 54]      # Grid output
    stride: [16, 16]            # Downsampling factor
    anchors:                    # Normalized anchor boxes
      - [0.054, 0.065]
      - [0.089, 0.139]
      - [0.195, 0.196]
    quantization: [0.176, 198]  # For dequantization
```

### Quantization Parameters

For quantized models (TFLite INT8), each output includes quantization parameters:

```python
# Dequantize output
scale, zero_point = output_spec['quantization']
float_output = (quantized_output - zero_point) * scale
```

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
  size: "640x640"        # Width x Height (always WxH regardless of layout)
  color_adaptor: rgb     # Channel order (rgb, bgr, yuyv)
  # Data layout is implicit: TFLite=NHWC, ONNX=NCHW

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
  size: "640x640"        # Target dimensions (width x height)
  color_adaptor: rgb     # Expected color format
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

### Color Format

The `color_adaptor` field specifies the expected channel format:

| Value | Description | Channel Order |
|-------|-------------|---------------|
| `rgb` | Standard RGB | Red, Green, Blue |
| `bgr` | OpenCV default | Blue, Green, Red |
| `rgba` | RGB with alpha | Red, Green, Blue, Alpha |
| `yuyv` | YUV 4:2:2 packed | For direct camera sensor input |

---

## Post-Processing & Split Decoder

### What is Split Decoder?

The `split_decoder` field indicates whether the model's detection outputs require external decoding:

```yaml
model:
  split_decoder: true    # Outputs need external anchor-based decoding
  split_decoder: false   # Outputs are fully decoded (ready-to-use boxes)
```

### Why Split Decoder Exists

**For [quantized INT8 models](modelpack/quantize.md)**, [ModelPack](modelpack/index.md) uses a "split decoder" architecture where:

1. **Model outputs raw grid features** — not decoded bounding boxes
2. **Decoding happens after dequantization** — in float32 precision
3. **Anchor-based box calculation** — uses the anchors specified in metadata

**The reason:** Quantization introduces precision loss. For small objects or high-resolution inputs, applying anchor calculations in INT8 would compound rounding errors, leading to inaccurate bounding boxes. By deferring decoding until after dequantization, we preserve box accuracy.

### Decoding Process

When `split_decoder: true`, the inference pipeline must:

1. **Run model inference** → Get quantized grid outputs
2. **Dequantize outputs** → Convert INT8 to float32 using scale/zero_point
3. **Apply anchor decoding** → Transform grid predictions to bounding boxes
4. **Run NMS** → Filter overlapping detections

```python
# Example decoding flow for split_decoder models
for output_spec in metadata['outputs']:
    if output_spec.get('decode', False):
        # Dequantize first
        scale, zp = output_spec['quantization']
        grid_float = (grid_int8.astype(np.float32) - zp) * scale
        
        # Then decode with anchors
        anchors = output_spec['anchors']
        stride = output_spec['stride']
        boxes = decode_yolo_grid(grid_float, anchors, stride)
```

### Output Types with Split Decoder

| `split_decoder` | Output Type | Description |
|-----------------|-------------|-------------|
| `true` | `detection` | Raw grid features, requires anchor decoding |
| `false` | `boxes`, `scores` | Decoded boxes ready for NMS |

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

##### `ultralytics` — Anchor-Free DFL Decoder

Used by [Ultralytics](ultralytics/index.md) models (YOLOv5, YOLOv8, YOLO11). Modern anchor-free detection using Distribution Focal Loss (DFL).

**Characteristics:**

- **Anchor-free**: Uses anchor points (grid centers) instead of pre-defined boxes
- **DFL regression**: Converts 16-bin distribution to box coordinates
- **Unified architecture**: Same decoder for YOLOv5, YOLOv8, and YOLO11

**Decoding formula:**

```python
# DFL converts 16-bin distribution to coordinate value
box = dfl(raw_box)  # [batch, 64, anchors] → [batch, 4, anchors]

# dist2bbox converts LTRB distances to boxes
x1y1 = anchor_points - lt
x2y2 = anchor_points + rb
# Returns xywh or xyxy in pixel coordinates
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
| `studio_server` | Server name | Quick access for traceability |
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
  size: "640x640"
  color_adaptor: rgb

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
  studio_server: saas
  session: t-abc123

dataset:
  name: "My Dataset"
  id: ds-xyz789
  classes: [...]

name: "my-model-v1"              # Model/session name
description: "Model for production deployment"
author: "My Organization"
```

### Embedding Metadata in TFLite

```python
from tensorflow_lite_support.metadata.python.metadata_writers import metadata_writer, writer_utils
from tensorflow_lite_support.metadata import metadata_schema_py_generated as schema
import yaml

def add_edgefirst_metadata(tflite_path: str, config: dict, labels: list[str]):
    """Add EdgeFirst metadata to a TFLite model."""
    
    # Write config and labels to temp files
    with open('/tmp/edgefirst.yaml', 'w') as f:
        yaml.dump(config, f)
    
    with open('/tmp/labels.txt', 'w') as f:
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
        associated_files=['/tmp/labels.txt', '/tmp/edgefirst.yaml']
    )
    
    writer_utils.save_file(writer.populate(), tflite_path)
```

### Embedding Metadata in ONNX

```python
import onnx
import json

def add_edgefirst_metadata(onnx_path: str, config: dict, labels: list[str]):
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
  studio_server: test    # EdgeFirst Studio server identifier
  session: t-abc123      # Training session ID (prefix: t-)
  username: john.doe     # User who initiated training
```

### Dataset Section

The dataset section references the [dataset](../datasets/index.md) used for training. See the [Dataset Zoo](../datasets/index.md) for available datasets and [Dataset Structure](../datasets/structure.md) for format details.

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
  size: "640x640"        # Width x Height
  color_adaptor: rgb     # rgb, rgba, yuyv, bgr
  # Note: Data layout is format-dependent
  # - TFLite: NHWC [batch, height, width, channels]
  # - ONNX: NCHW [batch, channels, height, width]
```

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
  model_task: detect     # detect, segment
  model_size: n          # n (nano), s (small), m (medium), l (large), x (xlarge)
  detection: true
  segmentation: false
  split_decoder: false   # Ultralytics models have decoder built-in
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
      batch: 1
      height: 40
      width: 40
      num_anchors_x_features: 54   # 3 anchors × (5 + 13 classes)
    dtype: float32
    type: detection
    decode: true
    decoder: modelpack
    quantization: [0.176, 198]
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
      batch: 1
      num_features: 84             # 4 box coords + 80 classes
      num_boxes: 8400
    dtype: float32
    type: detection
    decode: true
    decoder: ultralytics
    quantization: null             # Float model
    anchors: null                  # Anchor-free

# Ultralytics instance segmentation protos example
  - name: "output1"
    index: 1
    output_index: 1
    shape: [1, 32, 160, 160]       # NCHW: [batch, protos, H, W]
    dshape:
      batch: 1
      num_protos: 32
      height: 160
      width: 160
    dtype: float32
    type: protos
    decode: true
    decoder: ultralytics
    quantization: null
    anchors: null
```

---

## Related Articles

1. [ModelPack Overview](modelpack/index.md) - Architecture details and training parameters
2. [Ultralytics Integration](ultralytics/index.md) - YOLOv8/v11 training and deployment
3. [Training Vision Models](training/vision.md) - Step-by-step training workflow
4. [On Cloud Validation](validation/vision/managed.md) - Managed validation sessions
5. [On Target Validation](validation/vision/user_managed.md) - User-managed validation with `edgefirst-validator`
6. [ModelPack Quantization](modelpack/quantize.md) - Converting ONNX to quantized TFLite
7. [Deploying to Embedded Targets](deployment/evk.md) - Model deployment workflow
8. [EdgeFirst Perception Middleware](../perception/index.md) - Runtime inference stack
9. [Dataset Zoo](../datasets/index.md) - Available datasets for training
10. [Model Experiments Dashboard](../studio/models.md) - Managing training and validation sessions
