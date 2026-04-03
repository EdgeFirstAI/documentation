# Validate Vision Model

Now that you have trained a model, you can now validate the performance of your model.  This will briefly show the steps for validating a model, but for an in depth tutorial, please see [Validating Vision Models](../../models/validation/vision/managed.md).

If you haven't already, click on the training session card for more information.

{{ figure("/models/assets/training/vision-view-train-details.jpg", "Training Details") }}

Click the "Validate" button at the top right of the session as shown.

{{ figure("/models/assets/training/vision-validate-button.jpg", "Create Validation Session") }}

Specify the name of the validation session and the model and the dataset for validation.  The rest of the settings were kept as defaults.  Click "Start Session" at the bottom to start the validation session.

{{ figure("/models/assets/validation/vision-validate-settings.jpg", "Start Validation Session") }}

Go to the created validation session by first going back to the "Model Experiments" page.

{{ figure("/models/assets/training/go-back-to-model-experiments.jpg", "Go to Model Experiments") }}

Next, click the validation sessions of the model experiments.

{{ figure("/models/assets/validation/vision-validation-sessions.jpg", "Validation Sessions") }}

The validation session progress will appear in the "Validation" page as shown below.

{{ figure("/models/assets/validation/vision-session-progress.jpg", "Validation Progress") }}

Once completed the session card will appear like the following below.  To view the validation metrics, click on the validation charts button as indicated.

{{ figure("/models/assets/validation/vision-completed-session.jpg", "Completed Session") }}

The validation metrics should appear like the following.  For more information, please see the [Validation Metrics](../../models/validation/metrics/index.md) section.

{{ figure("/models/assets/validation/vision-charts.jpg", "Validation Charts") }}

You can navigate back to the training session by clicking on the "Training Session" link under the "Session" tab.

{{ figure("/models/assets/validation/back-to-training-session.jpg", "Go Back to the Training Session") }}
