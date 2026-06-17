# Convert Vision Model

We support model conversion and optimization workflows that enable trained models to be deployed on a wide range of target platforms and hardware architectures.

Follow the model conversion workflow that corresponds to your target platform. If you are deploying to a Windows/Linux PC or macOS system, you can skip this section and proceed directly to the next step to validate the ONNX model, which is automatically generated as part of the training session outputs.

If you are deploying to one of the supported hardware platforms listed below, follow the platform-specific conversion instructions for your target device.

| Converter | Supported Targets | Output Format | Docs |
|-----------|------------------|---------------|------|
| **TFLite Converter** | NXP i.MX 8M Plus (VIP8000), generic CPU/NPU TFLite delegates | `.tflite` flatbuffer | [TFLite Converter](../models/conversion/tflite.md) |
| **Neutron Converter** | NXP i.MX 95, i.MX 943/952, S32N79, MCX N54x/N94x, i.MX RT700, S32K5 | `.tflite` flatbuffer with Neutron microcode | [Neutron Converter](../models/conversion/neutron.md) |
| **TensorRT Converter** | NVIDIA Jetson (Orin Nano Super validated; broader lineup in progress) | `.tensorrt.zip` bundle (engine built on-device) | [TensorRT Converter](../models/conversion/tensorrt.md) |
| **Ara2 Converter** | NXP Ara240 DNPU | `.dvm` Dataflow Virtual Machine binary | [Ara2 Converter](../models/conversion/ara2.md) |
| **Hailo Converter** | Hailo-8 (26 TOPS), Hailo-8L (13 TOPS) | `.hef` Hailo Executable Format | [Hailo Converter](../models/conversion/hailo.md) |
