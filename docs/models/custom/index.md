# Custom Models

If you have a custom float model, it is highly recommended to export to a quantized model to deploy and maximize the model's performance using the target's NPU.  In this section, we will show examples of [quantizing float ONNX to a TFLite](quantize.md).  We will also be showing examples of [deploying a quantized ONNX or TFLite](npu.md) in the NXP **i.MX 8M Plus EVK** using the NPU execution providers from onnxruntime or the OpenVX delegate for tflite-runtime to deploy the model in the NPU. 

Deploying a quantized TFLite on the **i.MX 95 EVK** requires an extra step of [converting the model using NXP's eIQ neutron converter](neutron.md).  This will allow the model to be deployed on the i.MX 95 using the Neutron delegate in the platform. 

!!! warning "Specific BSP versions required"

    The latest BSP available for the Maivin lacks the `onnxruntime` library needed to run ONNX on the NPU.

    On the i.MX 8M Plus EVK, BSP v5.15 are used in the examples which was noted to have the providers needed for ONNX to run on the NPU `NnapiExecutionProvider`, `VsiNpuExecutionProvider`.  Later BSPs such as v6.12 did not have these providers.  This still needs confirmation from NXP as to why these providers were removed. 
