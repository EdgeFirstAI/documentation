# On Cloud Validation

This tutorial walks through how to run validation in the cloud using EdgeFirst Studio. In this setup, validation is executed as a **managed validation session**, which runs on a self-hosted EC2 instance.  This option is ideal for users who do not have access to an embedded platform to host the validation process locally.

In this tutorial, you will validate a **Fusion** model trained using either the [end-to-end workflows](../../../getting_started/workflows/index.md) or the [Training Fusion](../../training/fusion.md) guide.  Note that a Fusion model performs spatial perception using Radar and Camera sensors.  If you are working with Vision models, refer to [Validating Vision Models](../vision/managed.md).

{% include-markdown "discrete/studio/create_mpk_validation_session.md" %}

You will be greeted with the validation session dialog.  In this dialog, specify the name of the validation session, the model to validate, and the dataset to deploy.  In this example, the ONNX model will be validated.  Next specify, the validation parameters such as the detection window size and the detection threshold.  Additional information on these parameters are provided by hovering over the info button ![Info Button](../../../assets/buttons/studio-info-button.jpg).

The only augmentation available for this type of validation is `blur`.  See [Vision Augmentations](../../augmentations.md#blur) for further details.

{{ figure("../../assets/validation/fusion-session-fields.jpg", "Validation Session Fields") }}

Once the configurations have been made, go ahead and click on the "Start Session" button on the bottom right of the window.  This will start the validation session which will validate the model using the validation partition of the dataset.

## Session Progress

Once the validation session has started, the progress with the stages will be shown on the left and additional information and status is shown on the right.

{{ figure("../../assets/validation/fusion-session-progress.jpg", "Validation Session") }}

## Completed Session

The completed session will look as follows with the status set to "Complete".

{{ figure("../../assets/validation/fusion-completed-session.jpg", "Completed Session") }}

The attributes of the validation session are labeled below.

{{ figure("../../assets/validation/validation-session-attributes.jpg", "Validation Session Attributes") }}

## Validation Metrics

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/oKh4k0CCLmU?start=440&end=655" title="Validation Summary Metrics" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

Once the validation session completes, you can view the validation metrics by clicking the "View Validation Charts" button on the top of the session card.

{{ figure("../../assets/validation/fusion-validation-metrics.jpg", "Validation Metrics") }}

The metrics provides the precision, recall, F1, and IoU scores of the model at the specified window sizes.  Additional charts are provided for the Precision versus Recall and bird’s-eye view
heatmap describing where the model performs well and where the model makes errors.  

!!! info
    See [Fusion Metrics](../metrics/fusion.md) for further details.

You can go back to the validation session card by pressing the "Back" button as indicated in red below on the top left corner of the page.

{{ figure("../../assets/validation/back-button.jpg", "Back to the Session Card") }}

## Comparing Metrics

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/oKh4k0CCLmU?start=713&end=975" title="Comparing Validation Metrics" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

It is also possible to compare validation metrics for multiple sessions.  See [Validation Sessions](../../../studio/models.md#validation-sessions) in EdgeFirst Studio Overview for further details.

## Next Steps

Now that you have validated your Fusion model, follow these next steps
for [deploying your Fusion model](../../deployment/3d_raivin.md) in a Raivin Platform.
