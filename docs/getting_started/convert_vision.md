# Convert Vision Model

We support model conversion and optimization workflows, enabling trained models to be deployed across a wide range of target platforms and hardware architectures.  Please follow the specific model conversion that matches your platform.  If you are using a Windows or macOS system, you can either follow the TFLite Converter workflow or proceed directly to the next section to validate the ONNX model, which is already provided as part of the training session outputs.

| Converter | Supported Targets | Output Format | Docs |
|-----------|------------------|---------------|------|
| **TFLite Converter** | NXP i.MX 8M Plus (VIP8000), generic CPU/NPU TFLite delegates | `.tflite` flatbuffer | [TFLite Converter](../models/conversion/tflite.md) |
| **Neutron Converter** | NXP i.MX 95, i.MX 943/952, S32N79, MCX N54x/N94x, i.MX RT700, S32K5 | `.tflite` flatbuffer with Neutron microcode | [Neutron Converter](../models/conversion/neutron.md) |
| **TensorRT Converter** | NVIDIA Jetson (Orin Nano Super validated; broader lineup in progress) | `.tensorrt.zip` bundle (engine built on-device) | [TensorRT Converter](../models/conversion/tensorrt.md) |
| **Ara2 Converter** | NXP Ara240 DNPU | `.dvm` Dataflow Virtual Machine binary | [Ara2 Converter](../models/conversion/ara2.md) |
| **Hailo Converter** | Hailo-8 (26 TOPS), Hailo-8L (13 TOPS) | `.hef` Hailo Executable Format | [Hailo Converter](../models/conversion/hailo.md) | 
