# Hailo Conversion

Once training completes in EdgeFirst Studio, here are instructions for converting ONNX models to Hailo HEF format for NPU-accelerated inference on Hailo-8 (26 TOPS) and Hailo-8L (13 TOPS) with automatic quantization, calibration, and per-scale output decomposition.

1. Click on the completed training session

	{{ figure("/models/assets/training/vision-view-train-details.jpg", "Completed Training Session") }}

2. Navigate to the "Artifacts" tab and click on the "Hailo Converter" button under "Converters" on the right

	{{ figure("/models/assets/conversion/hailo-converter-button.jpg", "Hailo Converter") }}

3. Specify the conversion settings.  Then click on "Start App" to start the conversion process

	{{ figure("/models/assets/conversion/hailo-converter-options.jpg", "Hailo Converter Options") }}
	