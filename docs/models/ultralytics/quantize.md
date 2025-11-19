# Ultralytics Quantization

To run a YOLOv8 Float32 PyTorch model either [downloaded from Ultralytics](https://github.com/ultralytics/ultralytics) on an i.MX 8M Plus or 95 EVK platform, the model will need to be quantized to an INT8 model and converted to TFLite.  The steps below describe this process.

## PyTorch to TFLite

Follow along this tutorial to convert an Ultralytics Float32 PyTorch model into a quantized TFLite.  **Otherwise**, you can follow the [official docs provided by Ultralytics](https://docs.ultralytics.com/modes/export/) for exporting PyTorch models to TFLite.

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

!!! info "Deployment in the i.MX 95 Platform"

    If you plan to deploy a TFLite model on the i.MX 95 EVK Platform, you will need to convert the model to use the Neutron delegate in the platform.  To convert the model, you will need to use the Neutron Converter in NXP's EIQ portal by following the [iMX.95 Neutron Model Conversion instructions](neutron.md).

## Next Steps

Once you have a quantized TFLite, you can follow these instructions for [Deploying Models on the Target](npu.md). 
