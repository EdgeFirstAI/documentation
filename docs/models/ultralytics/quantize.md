# Ultralytics Quantization

To deploy Ultralytics YOLO models on edge NPU hardware (i.MX 8M Plus, i.MX 95 EVK), the float32 PyTorch model must be quantized to INT8 and converted to TFLite. EdgeFirst Studio handles this automatically during training, or you can export manually using the upstream Ultralytics CLI.

## EdgeFirst Studio Quantization

When you train a model through [EdgeFirst Studio](../index.md), INT8 TFLite export happens automatically at the end of training. The Studio trainer uses a custom quantization pipeline optimized for edge deployment:

- **TF-wrapped box normalization**: Box coordinates are normalized to [0,1] inside the DFL decode computation, producing better INT8 accuracy than post-hoc normalization
- **Split decoder**: Detection outputs are split into separate tensors (boxes, scores, and optionally mask coefficients and protos) so each gets independent per-tensor quantization scales
- **Generator-based calibration**: Validation images are streamed one at a time for memory-efficient INT8 calibration (~1.3 GB peak RAM vs ~43 GB for upstream)
- **Per-channel quantization**: Uses TensorFlow's MLIR quantizer for per-channel weight quantization

### Reference Accuracy

YOLOv8n on COCO val2017 (5000 images, 80 classes, 640x640 RGB input). Validated with [edgefirst-validator](../validation/vision/user_managed.md):

**Detection (YOLOv8n)**

| Model | mAP@0.5 | mAP@0.5-0.95 | Mean Recall |
|-------|---------|---------------|-------------|
| ONNX float32 | 50.2% | 35.75% | 46.64% |
| TFLite INT8 (EdgeFirst, 10% calibration) | 46.89% | 31.68% | 43.84% |
| TFLite INT8 (upstream full_integer_quant) | 47.51% | 32.03% | 43.83% |

**Instance Segmentation (YOLOv8n-seg)**

| Model | Det mAP@0.5 | Det mAP@0.5-0.95 | Mask mAP@0.5 | Mask mAP@0.5-0.95 |
|-------|-------------|-------------------|--------------|---------------------|
| TFLite INT8 (EdgeFirst, 10% calibration) | 41.68% | 27.83% | 40.37% | 24.62% |

EdgeFirst Studio quantized models use split decoder outputs and [0,1] normalized box coordinates for both detection and segmentation. Detection models produce 2 outputs (boxes, scores); segmentation models produce 4 (boxes, scores, mask_coefs, protos). See [Model Metadata](../metadata.md#post-processing-two-layer-outputs) for details.

### Output Format

All Studio-exported TFLite INT8 models use:

- **uint8 input** (raw pixel values)
- **int8 output** with per-tensor quantization scales
- **[0,1] normalized** box coordinates (`normalized: true` in [metadata](../metadata.md#box-coordinate-format-normalized))
- **Split decoder** for per-tensor INT8 quantization of each output component

## Manual Quantization (Upstream)

If you are not using EdgeFirst Studio, you can export a quantized TFLite using the upstream Ultralytics CLI. This uses Ultralytics' built-in export pipeline with onnx2tf integrated quantization.

1. Using a command prompt, install the Ultralytics framework.

```shell
pip install ultralytics
```

2. Download the PyTorch model from Ultralytics.

```shell
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s-seg.pt
```

!!! info "Detection Models"

    Here shows a list of detection models that can be downloaded.

    * Nano: `yolov8n.pt`
    * Small: `yolov8s.pt`
    * Medium: `yolov8m.pt`
    * Large: `yolov8l.pt`
    * X: `yolov8x.pt`

!!! info "Segmentation Models"

    Here shows a list of segmentation models that can be downloaded.

    * Nano: `yolov8n-seg.pt`
    * Small: `yolov8s-seg.pt`
    * Medium: `yolov8m-seg.pt`
    * Large: `yolov8l-seg.pt`
    * X: `yolov8x-seg.pt`

3. Convert the PyTorch models to TFLite with the following command.

```shell
yolo export model=path/to/model.pt format=tflite int8=True
```

4. This conversion will generate a directory `yolov8s_saved_model` which contains the quantized TFLite file `yolov8s_full_integer_quant.tflite`.

!!! warning "Upstream Quantization Limitations"

    The upstream `yolo export` command loads the entire calibration dataset into memory (can exceed 40 GB for large datasets) and produces a monolithic output tensor where boxes and scores share a single quantization scale. EdgeFirst Studio's custom pipeline addresses both issues with generator-based calibration and split decoder outputs.

!!! info "Deployment in the i.MX 95 Platform"

    If you plan to deploy a TFLite model on the i.MX 95 EVK Platform, you will need to convert the model to use the Neutron delegate in the platform.  To convert the model, you will need to use the Neutron Converter in NXP's EIQ portal by following the [iMX.95 Neutron Model Conversion instructions](neutron.md).

## Next Steps

Once you have a quantized TFLite, you can follow these instructions for [Deploying Models on the Target](npu.md).
