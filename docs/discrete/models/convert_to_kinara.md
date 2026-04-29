# Kinara Conversion

Once training completes in EdgeFirst Studio, here are instructions for converting ONNX models to Kinara ARA-2 DVM format with quantization calibration and INT16 precision promotion for NPU-accelerated inference, leveraging the [Ara240 DNPU](https://www.nxp.com/products/ARA240) chip.

1. Click on the completed training session

	{{ figure("/models/assets/training/vision-view-train-details.jpg", "Completed Training Session") }}

2. Navigate to the "Artifacts" tab and click on the "Kinara ARA-2 Converter" button under "Converters" on the right

	{{ figure("/models/assets/conversion/kinara-converter-button.jpg", "Kinara Converter") }}

3. Select the output precision.  Then click on "Start App" to start the conversion process

    {{ figure("/models/assets/conversion/kinara-converter-options.jpg", "Kinara Converter Options") }}
