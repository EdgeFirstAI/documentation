# Validate Vision Model

Now that you have trained a model, you can now validate the performance of your model.  This will briefly show the steps for validating a model, but for an in depth tutorial, please see [Validating Vision Models](../../models/validation/vision/managed.md).

If you haven't already, click on the training session card for more information.

{{ figure("/models/assets/training/vision-view-train-details.jpg", "Training Details") }}

On the top right corner of the page, click on the "validate" button as indicated.

{{ figure("/models/assets/validation/training_validate_button.jpg", "Validate Button") }}

Specify the name of the validation session and the model and the dataset for validation.  *Under the model selection, you can select various trained model artifacts from the choices of ONNX, TFLite, TensorRT, Kinara, Hailo, etc.  Choose the model you plan to deploy on target.  The purpose of validation is to assess the model of whether or not it meets the performance requirements needed to be deployed on target.*  The rest of the settings were kept as defaults.  Click "Start Session" at the bottom to start the validation session.

!!! failure "InsufficientInstanceCapacity"

    {{ img("/studio/assets/models/insufficient-capacity-error.jpg", "InsufficientInstanceCapacity Error") }}

    If you find the following error appear once you start your validation session - please try to recreate your validation session again. This error happens because AWS reports no EC2 instances are currently available to launch. This issue is under development and the only workaround is to retry launching sessions.

{{ figure("/models/assets/validation/vision-validate-settings.jpg", "Start Validation Session") }}

Go to the created validation session by first going back to the "Model Experiments" page.

{{ figure("/models/assets/training/go-back-to-model-experiments.jpg", "Go to Model Experiments") }}

Next, click the validation sessions of the model experiments.

{{ figure("/models/assets/validation/validation-sessions.jpg", "Validation Sessions") }}

The validation session progress will appear in the "Validation" page as shown below.

{{ figure("/models/assets/validation/vision-session-progress.jpg", "Validation Progress") }}

Once completed the session card will appear like the following below.  To view the validation metrics, click on the validation charts button as indicated.

{{ figure("/models/assets/validation/vision-completed-session.jpg", "Completed Session") }}

The validation metrics should appear like the following.  For more information, please see the [Validation Metrics](../../models/validation/metrics/index.md) section.

{{ figure("/models/assets/validation/vision-charts.jpg", "Validation Charts") }}

You can navigate back to the training session by clicking on the "Training Session" link under the "Session" tab.

{{ figure("/models/assets/validation/back-to-training-session.jpg", "Go Back to the Training Session") }}
