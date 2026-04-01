# Training Fusion Models

This tutorial describes the steps to train **Fusion** models in EdgeFirst Studio.  For a tutorial to train Vision models, see [Training Vision Models](vision.md).

## View Dataset

First ensure the dataset is ready to be used for training.  This means that the dataset is properly annotated and the dataset is properly split with training and validation samples.  The tutorial [View Fusion Dataset](../../datasets/tutorials/management.md#view-fusion-dataset) will show what to look for in a dataset before deploying it for training.

## Specify Project Experiments

From the projects page, choose the project that contains the dataset you plan to use.  In this example, the project chosen is called "Spatial Perception" project.  Next click the "Model Experiments" button as indicated in red.

{{ figure("../assets/training/fusion-model-experiments.jpg", "Model Experiments") }}

## Create Model Experiment

You will be greeted with the "Model Experiments" page.  A new project will not have any experiments as shown below.  You will need to first create a model experiment.  As mentioned in the [Model Experiments Dashboard](../../studio/models.md), model experiments will contain both training and validation sessions.

{{ figure("../assets/training/fusion-model-experiments-page.jpg", "Model Experiments Page") }}

Click on the "New Experiment" button as shown on the top right corner of the page.

{{ figure("../assets/training/new-experiment-button.jpg", "New Experiment Button") }}

Enter the name and the description of the experiment marked by the fields shown below.  Click on the "Create New Experiment" button to create your experiment.

{{ figure("../assets/training/fusion-model-experiments-fields.jpg", "Experiment Fields") }}

Your created experiment will appear like the following below.  At the start, this experiment will contain zero training and validation sessions.  The next step will show how to start your first training session on this experiment using the dataset in the project.

{{ figure("../assets/training/fusion-created-experiment.jpg", "Created Experiment") }}

## Create Training Session

In the experiment card, click the "Training Sessions" button as indicated in red below.

{{ figure("../assets/training/fusion-training-sessions.jpg", "Training Sessions") }}

You will be greeted to the "Training Sessions" page as shown below.  

{{ figure("../assets/training/fusion-training-sessions-page.jpg", "Training Sessions Page") }}

Start a training session by clicking on the "New Session" button on the top right corner of the page.

{{ figure("../assets/training/new-session-button.jpg", "New Session Button") }}

You will be greeted with the training session dialog.  In this dialog, specify the "Trainer Type" to "EdgeFirst Fusion" and provide a name and description of the training session as shown below.  Next specify the dataset to be used with training and validation partitions.  In this example, the dataset specified is the "Raivin Ultra Short" dataset.  Next specify the training parameters.  By default, the model will be trained using both the Camera and the Radar sensors.  However, you can specify one of the sensors turned off.  This model will output an occupancy grid highlighting the positions of people in world coordinates.  Additional information on these parameters are provided by hovering over the info button ![Info Button](../../assets/buttons/studio-info-button.jpg).

!!! note
    For an indoor setting, the "Radar Range Mode" is typically set to "Ultra Short (9m)" and the "Object Detection Range" is set to 9 meters.  This is the maximum range of detection, further distances are ignored.

For more information on available "Data Augmentations" please see [Vision Augmentations](../augmentations.md).

{{ figure("../assets/training/fusion-train-settings.jpg", "Training Session Fields") }}

Once the configurations have been made, go ahead and click on the "Start Session" button on the bottom right of the window.  This will start the training session which will train the model for the number of epochs specified.

## Session Progress

Once the training session has started, the progress with the stages will be shown on the left and additional information and status is shown on the right.

{{ figure("../assets/training/fusion-session-progress.jpg", "Training Session") }}

The training process begins with cloud instance initialization. Then the dataset is downloaded and cached.  Training starts afterwards.
At the end of the training process, the model is quantized and the checkpoints are published.

## Completed Session

The completed session will look as follows with the status set to "Complete".

{{ figure("../assets/training/fusion-completed-session.jpg", "Completed Session") }}

The attributes of the training session are labeled below.

{{ figure("../assets/training/training-session-attributes.jpg", "Training Session Attributes") }}

## Training Outcomes

### Training Metrics

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/Q8uiYJb1HJ4?start=1050&end=1355" title="Training Summary Metrics" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

You can view the training charts by clicking the "View Training Charts" button on the top of the session card.

{{ figure("../assets/training/fusion-charts.jpg", "Training Charts") }}

You can go back to the training session card by pressing the "Back" button as indicated in red below on the top left corner of the page.

{{ figure("../assets/training/back-button.jpg", "Back to the Session Card") }}

### Trained Models

<div style="text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/Q8uiYJb1HJ4?start=1530&end=1830" title="Downloading Model" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

The trained model artifacts can be downloaded by clicking the "View Additional Details" button on the training session card in EdgeFirst Studio.  This will open the session details and the models are listed under the "Artifacts" tab as shown below.  Click on the downward arrow indicated in red to download the models to your PC.

| Session Details                                                | Artifacts                                                                     |
|----------------------------------------------------------------|-------------------------------------------------------------------------------|
| ![session](../assets/training/fusion-session-details.jpg) | ![artifacts](../assets/training/fusion-session-artifacts.jpg) |

It is also possible to compare the training metrics for multiple sessions.  See [Training Sessions](../../studio/models.md#training-sessions) in the EdgeFirst Studio Overview for further details.

!!! info
    You can visualize the architecture of these models using [https://netron.app/](https://netron.app/).

## Next Steps

Now that you have generated your Fusion model, follow these next steps
for [validating your Fusion model](../validation/fusion/managed.md).
