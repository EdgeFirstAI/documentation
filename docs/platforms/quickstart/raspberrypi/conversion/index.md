# Model Conversions

Now that you have trained your Vision model, we recommend quantizing your model to leverage the platform's NPU and optimize model performance.

If you have a Raspberry Pi 5 with the [Hailo accelerator](https://hailo.ai/), we recommend converting the model to [Hailo HEF format](convert_hailo.md) for NPU-accelerated inference on Hailo-8 (26 TOPS) and Hailo-8L (13 TOPS).

Otherwise, we recommend converting the model to a [Quantized TFLite](convert_tflite.md).
