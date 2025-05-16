# Training ModelPack

This tutorial describes the steps to train **ModelPack Vision** models in EdgeFirst Studio.  For a tutorial to train Fusion models, see [Training Fusion Models](../fusion/training.md).  It is highly recommended for users to be familiar with the concepts and UI elements in EdgeFirst Studio as described in the [EdgeFirst Studio: Overview](../../getting_started/studio.md).

## Verify Dataset

First ensure the dataset is ready to be used for training.  This means that the dataset is properly annotated and the dataset is properly split into training and validation samples.  The section in [Verifying Datasets](../../datasets/tutorials.md#verifying-datasets) will show what to look for in a dataset before deploying it for training.

## Specify Project Experiments

From the projects page, choose the project that contains the dataset you plan to use.  In this example, the project chosen is the "Object Detection" project which was created in the [Quickstart Guide](../../index.md#create-project).  Next click the "Model Experiments" button as indicated in red.

<figure markdown="span">
![Model Experiments](../assets/training/modelpack-model-experiments.jpg){ align=center }
<figcaption>Model Experiments</figcaption>
</figure>

## Create Model Experiment

You will be greeted with the "Model Experiments" page.  A new project will not have any experiments as shown below.  You will need to first create a model experiment.  As mentioned in the [EgdeFirst Studio Overview](../../getting_started/studio.md#model-experiments), model experiments will contain the training and validation sessions. 

<figure markdown="span">
![Model Experiments Page](../assets/training/modelpack-model-experiments-page.jpg){ align=center }
<figcaption>Model Experiments Page</figcaption>
</figure>

Click on the "New Experiment" button as shown on the top right corner of the page.

<figure markdown="span">
![New Experiment Button](../assets/training/new-experiment-button.jpg){ align=center }
<figcaption>New Experiment Button</figcaption>
</figure>

Enter the name and the description of the experiment marked by the fields shown below.  Click on the "Create New Experiment" button to create your experiment.

<figure markdown="span">
![Experiment Fields](../assets/training/modelpack-model-experiments-fields.jpg){ align=center }
<figcaption>Experiment Fields</figcaption>
</figure>

Your created experiment will appear like the following below.  At the start, this experiment will contain zero training and validation sessions.  The next step will show how to start your first training session on this experiment using the dataset in the project. 

<figure markdown="span">
![Created Experiment](../assets/training/modelpack-created-experiment.jpg){ align=center }
<figcaption>Created Experiment</figcaption>
</figure>

## Create Training Session

In the experiment card, click the "Training Sessions" button as indicated in red below.

<figure markdown="span">
![Training Sessions](../assets/training/modelpack-training-sessions.jpg){ align=center }
<figcaption>Training Sessions</figcaption>
</figure>

You will be greeted to the ModelPack "Training Sessions" page as shown below.  

<figure markdown="span">
![Training Sessions Page](../assets/training/modelpack-training-sessions-page.jpg){ align=center }
<figcaption>Training Sessions Page</figcaption>
</figure>

Start a training session by clicking on the "New Session" button on the top right corner of the page.

<figure markdown="span">
![New Session Button](../assets/training/new-session-button.jpg){ align=center }
<figcaption>New Session Button</figcaption>
</figure>

You will be greeted with the training session configuration window.  In this window, specify the "Trainer Type" to "ModelPack" and provide a name and description of the training session as shown below.  Next specify the dataset to be used with training and validation partitions.  In this example, the dataset specified is the "Coffee Cup" dataset which was created in the [QuickStart](../../index.md#end-to-end-workflow) guide.  Next specify the training parameters.  By default, an object detection (bounding boxes) model will be trained.  However, you can specify either "Segmentation" or "Multitask" as shown below.  This model will output both bounding boxes and segmentation masks.  Additional information on these parameters are provided by hovering over the info buttons indicated in red below.

For more information on available "Data Augmentations" please see [Vision Augmentations](../augmentations.md).

<figure markdown="span">
![Training Session Fields](../assets/training/modelpack-session-fields.jpg){ align=center }
<figcaption>Training Session Fields</figcaption>
</figure>

Once the configurations have been made, go ahead and click on the "Start Session" button on the bottom right of the window.  This will start the training session which will train the model for the number of epochs specified.

## Session Progress

Once the training session has started, the progress with the stages will be shown on the left and additional information and status is shown on the right.

<figure markdown="span">
![Training Session](../assets/training/modelpack-session-progress.jpg){ align=center }
<figcaption>Training Session</figcaption>
</figure>

## Completed Session

The completed session will look as follows with the status set to "Complete".

<figure markdown="span">
![Completed Session](../assets/training/modelpack-completed-session.jpg){ align=center }
<figcaption>Completed Session</figcaption>
</figure>

The attributes of the training session are labeled below.

<figure markdown="span">
![Training Session Attributes](../assets/training/training-session-attributes.jpg){ align=center }
<figcaption>Training Session Attributes</figcaption>
</figure>

## Training Outcomes

Once the training session completes, you can view the training charts by clicking the "View Training Charts" button on the top of the session card.

<figure markdown="span">
![Training Charts](../assets/training/modelpack-charts.jpg){ align=center }
<figcaption>Training Charts</figcaption>
</figure>

You can go back to the training session card by pressing the "Back" button as indicated in red below on the top left corner of the page. 

<figure markdown="span">
![Back to the Session Card](../assets/training/back-button.jpg){ align=center }
<figcaption>Back to the Session Card</figcaption>
</figure>

The trained model artifacts can be downloaded by clicking the "View Additional Details" button on the training session card in EdgeFirst Studio.  This will open the session details and the models are listed under the "Artifacts" tab as shown below.  Click on the downward arrow indicated in red to download the models to your PC.

| Session Details                                                | Artifacts                                                                     |
|----------------------------------------------------------------|-------------------------------------------------------------------------------|
| ![session](../assets/training/modelpack-session-details.jpg) | ![artifacts](../assets/training/modelpack-session-artifacts.jpg) | 

<figure markdown="span">
![Training Metrics](../assets/training/modelpack-training-metrics.jpg){ align=center }
<figcaption>Training Metrics</figcaption>
</figure>

It is also possible to compare the training metrics for multiple sessions.  See [Training Sessions](../../getting_started/studio.md#training-sessions) in the EdgeFirst Studio Overview for further details. 

!!! info
    You can visualize the architecture of these models using [https://netron.app/](https://netron.app/).

## Next Steps 

Now that you have generated your Vision model, follow these next steps
for [validating your model](validation.md).