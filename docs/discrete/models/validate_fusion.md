# Validate Fusion Model

Now that you have trained a Fusion model, you can now start validating your model.  This will briefly show the steps for validating a model, but for an in depth tutorial, please see [Validating Fusion Models](../../models/validation/fusion/managed.md).

If you haven't already, click on the train session card for more information.

{{ figure("/models/assets/training/fusion-view-train-details.jpg", "Training Details") }}

On the top right corner of the page, click on the "validate" button as indicated.

{{ figure("/models/assets/validation/training_validate_button.jpg", "Validate Button") }}

Specify the name of the validation session and the model and the dataset for validation.  The rest of the settings were kept as defaults.  Click "Start Session" at the bottom to start the validation session.

!!! failure "InsufficientInstanceCapacity"

    {{ img("/studio/assets/models/insufficient-capacity-error.jpg", "InsufficientInstanceCapacity Error") }}

    If you find the following error appear once you start your validation session - please try to recreate your validation session again. This error happens because AWS reports no EC2 instances are currently available to launch. This issue is under development and the only workaround is to retry launching sessions.

{{ figure("/models/assets/validation/fusion-session-fields.jpg", "Start Validation Session") }}

The validation session progress will appear in the "Validation" page as shown below.

{{ figure("/models/assets/validation/fusion-session-progress.jpg", "Validation Progress") }}

Once completed the session card will appear like the following below.  The validation metrics are displayed as charts which can be found by clicking the view charts button as shown.

{{ figure("/models/assets/validation/fusion-completed-session.jpg", "Completed Session") }}

{{ figure("/models/assets/validation/fusion-validation-metrics.jpg", "Validation Charts") }}
