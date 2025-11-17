# YOLO v8 ONNX Ultralytic Model Conversion

<!-- TO-DO separate the ModelPack and Ultralytics stuff -->

To run YOLOv8 ONNX Ultralytics models -- either trained by Studio or downloaded from Ultralytics -- on an i.MX 95 platform, the model will need to be quantized prior to conversion to TFLite.  The steps below describe this process.

**Alternatively**, you can follow [instructions provided by Ultralytics](https://docs.ultralytics.com/modes/export/) for exporting PyTorch models to ONNX, and then to TFLite using the commands below.
