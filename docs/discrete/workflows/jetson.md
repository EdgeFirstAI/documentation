## Copy Dataset
{% include-markdown "discrete/datasets/copy_dataset.md" %}

## Tag Dataset
{% include-markdown "discrete/datasets/tag_dataset.md" %}
{% include-markdown "discrete/models/train_vision.md" %}

## Convert to TensorRT

Once the model is trained in EdgeFirst Studio, you will find "<model_name>_saved_model.zip" and "<model_name>.onnx" artifacts.

{{ figure("/models/assets/training/vision-session-artifacts.jpg", "Model Artifacts") }}

This tutorial will provide the steps for converting the ONNX model to TensorRT.  Although it is possible to deploy the ONNX model, we recommend converting this model to TensorRT when deploying in the Jetson to maximize the performance of the model.  We find that the converted TensorRT model is **~1.3x faster** than ONNX with the TensorRT execution provider. 

The following outlines the basic steps required to convert a model to TensorRT format.  For detailed information about the conversion process and available configuration options, refer to the [TensorRT Converter](../../models/conversion/tensorrt.md).

{% include-markdown "discrete/models/convert_to_tensorrt.md" heading-offset=0 %}

{% include-markdown "discrete/models/validate_vision.md" %}

## Deploy Model on Jetson Orin

You can find examples for deploying your model in [EdgeFirst Studio](../../models/deployment/studio.md).  Otherwise, instructions for deploying in the Jetson Orin will be coming soon.
