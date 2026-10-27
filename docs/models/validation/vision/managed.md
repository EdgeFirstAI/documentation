# On Cloud Validation

This tutorial walks through how to run validation in the cloud using EdgeFirst Studio which runs on a self-hosted EC2 instance.  This option is ideal for users who do not have access to an embedded platform to host the validation process locally.

In this tutorial, you will validate a **Vision** model trained using either the [end-to-end workflows](../../../getting_started/workflows/index.md) or the [Training Vision](../../training/vision.md) guide.  Note that a Vision model detects objects in camera frames or images.  If you are working with Fusion models, refer to [Validating Fusion Models](../fusion/managed.md).

Alternatively, EdgeFirst Studio also supports **On-Target Validation**. In this mode, the model is deployed and validated directly on an embedded platform.  For more details, see [On Target Validation](user_managed.md).

{% include-markdown "discrete/models/create_validation_session.md" %}

You will be greeted with the validation session dialog.  Select the model to use for validation. Select either an **ONNX, Keras, or TFLite** models — these are the formats supported by cloud validation. When you are ready, click **START APP** to begin the validation process.

{{ figure("../../assets/validation/vision-validate-settings.jpg", "Validation Session Fields") }}

Once the settings have been specified, go ahead and click on the "Start Session" button on the bottom right of the dialog.  This will start the validation session which will validate the model using the validation partition of the dataset.

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
