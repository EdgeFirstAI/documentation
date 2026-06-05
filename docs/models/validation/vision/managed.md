# On Cloud Validation

This tutorial walks through how to run validation in the cloud using EdgeFirst Studio. In this setup, validation is executed as a **managed validation session**, which runs on a self-hosted EC2 instance.  This option is ideal for users who do not have access to an embedded platform to host the validation process locally.

In this tutorial, you will validate a **Vision** model trained using either the [end-to-end workflows](../../../getting_started/workflows/index.md) or the [Training Vision](../../training/vision.md) guide.  Note that a Vision model detects objects in camera frames or images.  If you are working with Fusion models, refer to [Validating Fusion Models](../fusion/managed.md).

Alternatively, EdgeFirst Studio also supports **On-Target Validation**, which runs as a user-managed validation session. In this mode, the model is deployed and validated directly on an embedded platform.  For more details, see [On Target Validation](user_managed.md).

{% include-markdown "discrete/models/create_validation_session.md" %}

You will be greeted with a validation session dialog.  In this dialog, specify the name of the validation session, the model to validate, and the dataset to deploy.  In this example, the "Coffee Cup" dataset with the validation partition will be used.  *Under the model selection, you can select various trained model artifacts from the choices of ONNX, TFLite, TensorRT, Kinara, Hailo, etc.  Choose the model you plan to deploy on target.  The purpose of validation is to assess the model of whether or not it meets the performance requirements needed to be deployed on target.*  Additional parameters are available on the right for user override. Otherwise the same parameters set in the training session will be used. For more information on these parameters hover over the info button ![Info Button](../../../assets/buttons/studio-info-button.jpg).

{{ figure("../../assets/validation/vision-validate-settings.jpg", "Validation Session Fields") }}

Once the settings have been specified, go ahead and click on the "Start Session" button on the bottom right of the dialog.  This will start the validation session which will validate the model using the validation partition of the dataset.

!!! failure "InsufficientInstanceCapacity"

    {{ img("/studio/assets/models/insufficient-capacity-error.jpg", "InsufficientInstanceCapacity Error") }}

    If you see this error after starting your validation session, retry creating the session. This can happen when AWS reports that no EC2 instances are currently available to launch; the current workaround is to retry.

## Session Progress

Once the validation session has started, the progress with the stages will be shown on the left and additional information and status is shown on the right.

{{ figure("../../assets/validation/vision-session-progress.jpg", "Validation Session") }}

## Completed Session

The completed session will look as follows with the status set to "Complete".

{{ figure("../../assets/validation/vision-completed-session.jpg", "Completed Session") }}

The attributes of the validation sessions in EdgeFirst Studio are labeled below.

{{ figure("../../assets/validation/validation-session-attributes.jpg", "Validation Session Attributes") }}

## Validation Metrics

Once the validation session completes, you can view the validation metrics by clicking the "view validation charts" button on the top of the session card.

{{ figure("../../assets/validation/vision-charts.jpg", "Validation Charts") }}

!!! info
    See [detection](../metrics/detection/index.md) and [segmentation](../metrics/segmentation.md) metrics for further details.

You can go back to the validation session card by pressing the "Back" button as indicated in red below on the top left corner of the page.

{{ figure("../../assets/validation/back-button.jpg", "Back to the Session Card") }}

## Comparing Metrics

It is also possible to compare validation metrics for multiple sessions.  See [Validation Sessions](../../../studio/models.md#validation-sessions) in the Model Experiments Dashboard.

## Next Steps

Now that you have validated your model, you can find examples for deploying your model in [EdgeFirst Studio](../../deployment/studio.md), [PC](../../deployment/pc/index.md), [Embedded Targets](../../deployment/launcher.md), the [Maivin](../../deployment/maivin.md), and the [Raivin](../../deployment/2d_raivin.md). 
