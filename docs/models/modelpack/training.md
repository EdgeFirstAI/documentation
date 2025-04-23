# Training ModelPack

This page will provide a walk-through for training Vision models using ModelPack in EdgeFirst Studio. For a walkthrough on [Training Fusion Models](../fusion/training.md) please see the link attached.

## Verify Dataset

Before running a training session, ensure the dataset is ready to be used for training.  
This means that the dataset is properly annotated and the dataset is properly split 
with training and validation samples.  The sample dataset shown below has a dedicated 
split for training (1656 samples) and validation (184 samples).

<figure markdown="span">
![Dataset Groups](../assets/training/vision-dataset-groups.jpg){ align=center }
<figcaption>Dataset Groups</figcaption>
</figure>

To verify the annotations, click the button that navigates to the gallery.  This will show the contents of the dataset.  The dataset may be comprised of multiple sequences as shown below.  

<figure markdown="span">
![Dataset Sequences](../assets/training/vision-dataset-sequences.jpg){ align=center }
<figcaption>Dataset Sequences</figcaption>
</figure>

Clicking on any of these sequences will open individual images in the sequence with the visualizations of the annotations.  

!!! info
    Datasets that train Vision models provide image annotations of the object's 2D bounding box and segmentation mask.  For more information on the dataset annotations, please see [EdgeFirst Dataset Format](../../datasets/format.md#dataset-annotation-format).

<figure markdown="span">
![Vision Annotations](../assets/training/vision-annotations.jpg){ align=center }
<figcaption>Vision Annotations</figcaption>
</figure>

For cases where the annotations need corrections, please see [Dataset Tutorials](../../datasets/tutorials.md#audit-annotations) for more details.

## Select the Trainer Tool

Once the training dataset is ready, select *Trainer* from the tool options.  

<figure markdown="span">
![Trainer Tool](../assets/training/trainer-tool.jpg){ align=center }
<figcaption>Tool Options</figcaption>
</figure>

## Specify the Project

Specify the project to run training at the center of the top menu bar.

<figure markdown="span">
![Project Selection](../assets/training/trainer-project-selection.jpg){ align=center }
<figcaption>Project Selection</figcaption>
</figure>

## Create Training Experiment

If you haven't already done so, create a training experiment.  
Create a new training experiment by clicking the *create* button on the top right.

<figure markdown="span">
![Create New Experiment](../assets/validation/create-button.jpg){ align=center }
<figcaption>Create New Experiment</figcaption>
</figure>

This will provide pop-up for the user to specify the name and description of 
the experiment.  Give a name and a description that reflects your goals in this experiment.

<figure markdown="span">
![Create New Experiment](../assets/training/training-experiment.jpg){ align=center }
<figcaption>Create New Experiment</figcaption>
</figure>

## Create Training Session

Create a new training session within this experiment by 
clicking the *NEW SESSION* button as shown below.

<figure markdown="span">
![Training Session](../assets/training/training-session.jpg){ align=center }
<figcaption>Training Session</figcaption>
</figure>

Configure the settings on the left panel by specifying *Trainer Type* to *ModelPack* 
and provide additional configurations for the name of the session and the dataset to deploy.  
Next configure the settings on the right panel by specifying training parameters.  
By default a segmentation model will be trained, however, object detection or 
multi-task based models are possible variations.  

!!! note
    Additional information on these parameters are provided by hovering over the info button.
    For more information on available vision augmentation please see [Vision Augmentations](../augmentations.md).

<figure markdown="span">
![Training Options](../assets/training/modelpack-training-options.jpg){ align=center }
<figcaption>Training Options</figcaption>
</figure>

## Start the Session

Start the session by clicking the *START SESSION* button on the bottom right.

<figure markdown="span">
![Start Session](../assets/validation/start-session.jpg){ align=center }
<figcaption>Start the Session</figcaption>
</figure>

## Session Progress

The training session has now started while the progress is tracked on the 
left panel and additional information and status is shown on the right panel.

<figure markdown="span">
![Training Session](../assets/training/modelpack-training-session.jpg){ align=center }
<figcaption>Training Session</figcaption>
</figure>

<figure markdown="span">
![Training Session Attributes](../assets/training/training-session-attributes.jpg){ align=center }
<figcaption>Training Session Attributes</figcaption>
</figure>

## Training Metrics

The training metrics are shown by clicking the button that views the training charts on the top left of the session card.  

<figure markdown="span">
![Training Metrics](../assets/training/modelpack-training-metrics.jpg){ align=center }
<figcaption>Training Metrics</figcaption>
</figure>

## Completed Session

Once completed, the status will be shown as complete.

<figure markdown="span">
![Completed Session](../assets/training/modelpack-completed-session.jpg){ align=center }
<figcaption>Completed Session</figcaption>
</figure>

## Trained Models 

The trained Keras, TFLite, and RTM models can be found and downloaded by clicking on the 
button that views the session details on the top right of the session card.  
This will open a new dialog with the session details and the models are placed 
on the top right which can then be downloaded.

<figure markdown="span">
![Session Details](../assets/training/modelpack-session-details.jpg){ align=center }
<figcaption>Session Details</figcaption>
</figure>

## Next Steps 

Now that you have generated your Vision model, follow these next steps
for [validating your Vision model](validation.md).