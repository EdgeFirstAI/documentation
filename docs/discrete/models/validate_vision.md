# Validate Vision Model

Now that you have trained a model, you can validate its performance. The purpose of validation is to determine whether the selected model meets the performance requirements before deployment. EdgeFirst Studio offers two validation paths depending on your goal:

| Path | Where it runs | Supported formats |
|------|--------------|-------------------|
| [**Cloud Validation**](../../models/validation/vision/managed.md) (this guide) | EdgeFirst Studio EC2 | ONNX, Keras, TFLite |
| [**On-Target Profiling**](../../profiler/index.md) | Your edge platform | All converted formats (.tflite, .hef, .dvm, .engine) |

!!! info "Validating on target hardware?"
    Cloud validation only supports **ONNX, Keras, and TFLite** artifacts. If you want to measure real inference latency and accuracy on your target device — including NPU-compiled formats like Neutron, Hailo, Ara2, or TensorRT — use the [EdgeFirst Profiler](../../profiler/index.md).

## Cloud Validation

If you haven't already, click on the training session card for more information.

{{ figure("/models/assets/training/vision-view-train-details.jpg", "Training Details") }}

On the top right corner of the page, click on the "validate" button as indicated.

{{ figure("/models/assets/validation/training_validate_button.jpg", "Validate Button") }}

Select the model to use for validation. Select either an **ONNX, Keras, or TFLite** models — these are the formats supported by cloud validation. When you are ready, click **START APP** to begin the validation process.

{{ figure("/models/assets/validation/vision-validate-settings.jpg", "Start Validation Session") }}

Go to the created validation session by first going back to the "Model Experiments" page.

{{ figure("/models/assets/training/go-back-to-model-experiments.jpg", "Go to Model Experiments") }}

Next, click the validation sessions of the model experiments.

{{ figure("/models/assets/validation/validation-sessions.jpg", "Validation Sessions") }}

The validation session progress will appear in the "Validation" page as shown below.

{{ figure("/models/assets/validation/vision-session-progress.jpg", "Validation Progress") }}

Once the session is complete, the session card will appear like the following. To view the validation metrics, click the validation charts button as indicated.

{{ figure("/models/assets/validation/vision-completed-session.jpg", "Completed Session") }}

The validation metrics should appear like the following. For more information, please see the [Validation Metrics](../../models/validation/metrics/index.md) section.

{{ figure("/models/assets/validation/vision-charts.jpg", "EdgeFirst Studio — validation metrics dashboard on a completed session: mAP, AP/AR breakdowns, confusion matrices, PR curves") }}

You can navigate back to the training session by clicking on the "Training Session" link under the "Session" tab.

{{ figure("/models/assets/validation/back-to-training-session.jpg", "Go Back to the Training Session") }}
