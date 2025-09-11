# Managed Validation

This tutorial will describe the steps to validate the performance of **ModelPack Vision** models as managed sessions in EdgeFirst Studio that have been trained through the [end-to-end workflows](../../../getting_started/workflows/index.md) or [Training ModelPack](../training.md).  For a tutorial to validate Fusion models, see [Validating Fusion Models](../../fusion/validation.md).  A managed validation session is self hosted in an EC2 instance which is suited for users that do not have an embedded platform available to host the validation process.  A [user-managed validation](user_managed.md) session deploys the model in an embedded platform for validation.

{% include-markdown "discrete/studio/create_mpk_validation_session.md" %}

You will be greeted with a validation session dialog.  In this dialog, specify the name of the validation session, the model to validate, and the dataset to deploy.  In this example, the TFLite model will be validated and the "Coffee Cup" dataset with the validation partition will be used.  Next specify, the validation parameters on the right.  Additional information on these parameters are provided by hovering over the info button ![Info Button](../../../assets/buttons/studio-info-button.jpg). 

<figure markdown="span">
![Validation Session Fields](../../assets/validation/vision-validate-settings.jpg){ align=center }
<figcaption>Validation Session Fields</figcaption>
</figure>

Once the settings have been specified, go ahead and click on the "Start Session" button on the bottom right of the dialog.  This will start the validation session which will validate the model using the validation partition of the dataset.

## Session Progress

Once the validation session has started, the progress with the stages will be shown on the left and additional information and status is shown on the right.

<figure markdown="span">
![Validation Session](../../assets/validation/vision-session-progress.jpg){ align=center }
<figcaption>Validation Session</figcaption>
</figure>

## Completed Session

The completed session will look as follows with the status set to "Complete".

<figure markdown="span">
![Completed Session](../../assets/validation/vision-completed-session.jpg){ align=center }
<figcaption>Completed Session</figcaption>
</figure>

The attributes of the validation sessions in EdgeFirst Studio are labeled below.

<figure markdown="span">
![Validation Session Attributes](../../assets/validation/validation-session-attributes.jpg){ align=center }
<figcaption>Validation Session Attributes</figcaption>
</figure>

## Validation Metrics 

Once the validation session completes, you can view the validation metrics by clicking the "View Validation Charts" button on the top of the session card.

<figure markdown="span">
![Validation Charts](../../assets/validation/vision-charts.jpg){ align=center }
<figcaption>Validation Charts</figcaption>
</figure>

!!! info
    See [detection](../../metrics/detection.md) and [segmentation](../../metrics/segmentation.md) metrics for further details.

You can go back to the validation session card by pressing the "Back" button as indicated in red below on the top left corner of the page. 

<figure markdown="span">
![Back to the Session Card](../../assets/validation/back-button.jpg){ align=center }
<figcaption>Back to the Session Card</figcaption>
</figure>

## Comparing Metrics

It is also possible to compare validation metrics for multiple sessions.  See [Validation Sessions](../../../studio/models.md#validation-sessions) in the Model Experiments Dashboard.

## Next Steps

Now that you have validated your Vision model, you can find examples for deploying your model in the [PC](../deployment/pc.md), [EVK](../deployment/evk.md), and [Maivin Platform](../deployment/maivin.md). 