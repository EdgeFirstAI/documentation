# TFLite Quantization

This guide explains how to quantize Float32 models to TensorFlow Lite (TFLite).  If you plan to deploy the model on a low-power embedded platform such as the NXP i.MX 8M Plus (≈5W), quantization enables efficient inference on the device’s NPU, improving performance and reducing power consumption.

Once training completes in EdgeFirst Studio, you can convert the SavedModel to TFLite with optional INT8 quantization, per-channel calibration, MLIR quantizer, and configurable split support.

1. Click on the completed training session

	{{ figure("/models/assets/training/vision-view-train-details.jpg", "Completed Training Session") }}

2. Navigate to the "Artifacts" tab and click on the "TFLite Converter" button under "Converters" on the right

	{{ figure("/models/assets/conversion/tflite-converter-button.jpg", "TFLite Converter") }}

3. Specify the conversion settings.  The Studio converter uses a custom quantization pipeline optimized for edge deployment:

	- **TF-wrapped box normalization**: Box coordinates are normalized to [0,1] inside the DFL decode computation, producing better INT8 accuracy than post-hoc normalization
	- **Split decoder**: Detection outputs are split into separate tensors (boxes, scores, and optionally mask coefficients and protos) so each gets independent per-tensor quantization scales
	- **Generator-based calibration**: Validation images are streamed one at a time for memory-efficient INT8 calibration (~1.3 GB peak RAM vs ~43 GB for upstream)
	- **Per-channel quantization**: Uses TensorFlow's MLIR quantizer for per-channel weight quantization

	Click on "Start App" to start the conversion process

	{{ figure("/models/assets/conversion/tflite-converter-options.jpg", "TFLite Converter Options") }}

### Reference Accuracy

YOLOv8n on COCO val2017 (5000 images, 80 classes, 640x640 RGB input).  Validated with the [EdgeFirst Profiler](../../profiler/index.md):

**Detection (YOLOv8n)**

| Model | mAP@0.5 | mAP@0.5-0.95 | Mean Recall |
|-------|---------|--------------|-------------|
| ONNX float32 | 50.2% | 35.75% | 46.64% |
| TFLite INT8 (EdgeFirst, 10% calibration) | 46.89% | 31.68% | 43.84% |
| TFLite INT8 (upstream full_integer_quant) | 47.51% | 32.03% | 43.83% |

**Instance Segmentation (YOLOv8n-seg)**

| Model | Det mAP@0.5 | Det mAP@0.5-0.95 | Mask mAP@0.5 | Mask mAP@0.5-0.95 |
|-------|-------------|------------------|--------------|-------------------|
| TFLite INT8 (EdgeFirst, 10% calibration) | 41.68% | 27.83% | 40.37% | 24.62% |

EdgeFirst Studio quantized models use split decoder outputs and [0,1] normalized box coordinates for both detection and segmentation. Detection models produce 2 outputs (boxes, scores); segmentation models produce 4 (boxes, scores, mask_coefs, protos). See [Model Metadata](../../models/metadata.md#post-processing-two-layer-outputs) for details.

### Output Format

All Studio-exported TFLite INT8 models use:

- **uint8 input** (raw pixel values)
- **int8 output** with per-tensor quantization scales
- **[0,1] normalized** box coordinates (`normalized: true` in [metadata](../../models/metadata.md#box-coordinate-format-normalized))
- **Split decoder** for per-tensor INT8 quantization of each output component
