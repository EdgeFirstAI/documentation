# Validate Vision Model

Now that you have trained a Vision model, you can now start validating your Vision model.  This will briefly show the steps for validating a model, but for an in depth tutorial, please see [Validating Vision Models](../../models/validation/vision/managed.md).

On the train session card, expand the session details.

{{ figure("/models/assets/training/vision-view-train-details.jpg", "Training Details") }}

Click the "Validate" button.

{{ figure("/models/assets/training/vision-validate-button.jpg", "Create Validation Session") }}

Specify the name of the validation session and the model and the dataset for validation.  The rest of the settings were kept as defaults.  Click "Start Session" at the bottom to start the validation session.

{{ figure("/models/assets/validation/vision-validate-settings.jpg", "Start Validation Session") }}

!!! warning "No Datasets Available"

    In case there are no datasets visible on the dropdown.  Please refresh your browser.

The validation session progress will appear in the "Validation" page as shown below.

{{ figure("/models/assets/validation/vision-session-progress.jpg", "Validation Progress") }}

Once completed the session card will appear like the following below.

{{ figure("/models/assets/validation/vision-completed-session.jpg", "Completed Session") }}

The validation metrics are displayed as charts which can be found by clicking the validation charts.

{{ figure("/models/assets/validation/vision-charts-button.jpg", "Validation Charts Button") }}

{{ figure("/models/assets/validation/vision-charts.jpg", "Validation Charts") }}
