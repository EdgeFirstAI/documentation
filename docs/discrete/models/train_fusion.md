# Train a Fusion Model

A fully annotated dataset that is split into training and validation samples is required to start training a Fusion model.  This will briefly show the steps for training a model, but for an in depth tutorial, please see [Training Fusion](../../models/fusion/training.md).

From the "Projects" page, click on "Model Experiments" of your project. 

<figure markdown="span">
![Model Experiments Page](../../models/assets/training/fusion-model-experiments.jpg){ align=center }
<figcaption>Model Experiments Page</figcaption>
</figure>

Create a new experiment by clicking "New Experiment" on the top right corner.  Enter the name the description of this experiment.  Click "Create New Experiment".

<figure markdown="span">
![Model Experiments Page](../../models/assets/training/fusion-create-experiment.jpg){ align=center }
<figcaption>Model Experiments Page</figcaption>
</figure>

Navigate to the "Training Sessions".

<figure markdown="span">
![Training Sessions](../../models/assets/training/fusion-training-sessions.jpg){ align=center }
<figcaption>Training Sessions</figcaption>
</figure>

Create a new training session by clicking on the "New Session" button on the top right corner.

<figure markdown="span">
![New Session Button](../../models/assets/training/new-session-button.jpg){ align=center }
<figcaption>New Session Button</figcaption>
</figure>

Follow the settings indicated and keep the rest of the settings by their default.  Click "Start Session" to start the training session. 

!!! warning "Session Name"
    Do not include any forward slash "/" in the session names as this can result in missing model artifacts.

<figure markdown="span">
![Start Training Session](../../models/assets/training/fusion-session-fields.jpg){ align=center }
<figcaption>Start Training Session</figcaption>
</figure>

The session progress will be shown like the following below.

<figure markdown="span">
![Training Session Progress](../../models/assets/training/fusion-session-progress.jpg){ align=center }
<figcaption>Training Session Progress</figcaption>
</figure>

Once completed the session card will appear like the following below.

<figure markdown="span">
![Completed Session](../../models/assets/training/fusion-completed-session.jpg){ align=center }
<figcaption>Completed Session</figcaption>
</figure>

On the train session card, expand the session details.

<figure markdown="span">
![Training Details](../../models/assets/training/fusion-view-train-details.jpg){ align=center }
<figcaption>Training Details</figcaption>
</figure>

The trained models will be listed under "Artifacts".  

| Session Details                                                | Artifacts                                                                     |
|----------------------------------------------------------------|-------------------------------------------------------------------------------|
| ![session](../../models/assets/training/fusion-session-details.jpg) | ![artifacts](../../models/assets/training/fusion-session-artifacts.jpg) | 
