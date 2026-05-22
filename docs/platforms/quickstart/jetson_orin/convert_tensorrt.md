# Convert to TensorRT

Once the model is trained in EdgeFirst Studio, you will find "<model_name>_saved_model.zip" and "<model_name>.onnx" artifacts.

{{ figure("../../../models/assets/training/vision-session-artifacts.jpg", "Model Artifacts") }}

This tutorial will provide the steps for converting the ONNX model to TensorRT.  Although it is possible to deploy the ONNX model, we recommend converting this model to TensorRT when deploying in the Jetson to maximize the performance of the model.  We find that the converted TensorRT model is **~1.3x faster** than ONNX with the TensorRT execution provider. 

{% include-markdown "discrete/models/onnx_to_tensorrt.md" heading-offset=0 %}

Now that you have converted the ONNX model to TensorRT, you can [validate the performance of this model](validate.md) on the Jetson Orin.
