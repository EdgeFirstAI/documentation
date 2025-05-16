# Validating ModelPack

This tutorial will describe the steps to validate the performance of **ModelPack Vision** models in EdgeFirst Studio that have been trained through the [end-to-end worklows](../../getting_started/workflows/index.md) or [Training ModelPack](training.md).  For a tutorial to validate Fusion models, see [Validating Fusion Models](../fusion/validation.md). 

## Specify Project Experiments

From the projects page, choose the project that contains the training session with the models you want to validate.  In this example, the project chosen is the "Object Detection" project that was created in the [Quickstart Guide](../../index.md#create-project).  Next click the "Model Experiments" button as indicated in red.

<figure markdown="span">
![Model Experiments](../assets/training/modelpack-model-experiments.jpg){ align=center }
<figcaption>Model Experiments</figcaption>
</figure>

## Create Validation Session

In the experiment card, click the "Validate Sessions" button as indicated in red below.

<figure markdown="span">
![Validate Sessions](../assets/validation/modelpack-validation-sessions.jpg){ align=center }
<figcaption>Validate Sessions</figcaption>
</figure>

You will be greeted to the "Validate Sessions" page as shown below. 

<figure markdown="span">
![Validate Sessions Page](../assets/validation/modelpack-validation-sessions-page.jpg){ align=center }
<figcaption>Validate Sessions Page</figcaption>
</figure>

Start a validation session by clicking on the "New Session" button on the top right corner of the page. 

<figure markdown="span">
![New Session Button](../assets/training/new-session-button.jpg){ align=center }
<figcaption>New Session Button</figcaption>
</figure>

You will be greeted with the validation session configuration window.  In this window, specify the name of the validation session, the model to validate, and the dataset to deploy.  In this example, the TFLite model will be validated and the "Coffee Cup" dataset with the validation partition will be used.  Next specify, the validation parameters such as the IoU and score thresholds.  Additional information on these parameters are provided by hovering over the info buttons as indicated in red below. 

<figure markdown="span">
![Validation Session Fields](../assets/validation/modelpack-session-fields.jpg){ align=center }
<figcaption>Validation Session Fields</figcaption>
</figure>

Once the configurations have been made, go ahead and click on the "Start Session" button on the bottom right of the window.  This will start the validation session which will validate the model using the validation partition of the dataset.

## Session Progress

Once the validation session has started, the progress with the stages will be shown on the left and additional information and status is shown on the right.

<figure markdown="span">
![Validation Session](../assets/validation/modelpack-session-progress.jpg){ align=center }
<figcaption>Validation Session</figcaption>
</figure>

## Completed Session

The completed session will look as follows with the status set to "Complete".

<figure markdown="span">
![Completed Session](../assets/validation/modelpack-completed-session.jpg){ align=center }
<figcaption>Completed Session</figcaption>
</figure>

The attributes of the validation session are labeled below.

<figure markdown="span">
![Validation Session Attributes](../assets/validation/validation-session-attributes.jpg){ align=center }
<figcaption>Validation Session Attributes</figcaption>
</figure>

## Validation Metrics 

Once the validation session completes, you can view the validation metrics by clicking the "View Validation Charts" button on the top of the session card.

<figure markdown="span">
![Validation Charts](../assets/validation/modelpack-charts.jpg){ align=center }
<figcaption>Validation Charts</figcaption>
</figure>

See [Validation Metrics](../metrics.md#modelpack) for further details.

You can go back to the validation session card by pressing the "Back" button as indicated in red below on the top left corner of the page. 

<figure markdown="span">
![Back to the Session Card](../assets/validation/back-button.jpg){ align=center }
<figcaption>Back to the Session Card</figcaption>
</figure>

## Comparing Metrics

It is also possible to compare validation metrics for multiple sessions.  See [Validation Sessions](../../getting_started/studio.md#validation-sessions) in the EdgeFirst Studio Overview for further details. 

## Next Steps

Now that you have validated your Vision model, you can find examples for deploying your model in the [PC](deployment/pc.md) and in the [Maivin Platform](deployment/maivin.md). 