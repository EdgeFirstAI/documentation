# Train a Fusion Model

A fully annotated dataset that is split into training and validation samples is required to start training a Fusion model.  This will briefly show the steps for training a model, but for an in depth tutorial, please see [Training Fusion Models](../../models/training/fusion.md).

From the "Projects" page, click on "Model Experiments" of your project.

{{ figure("/models/assets/training/fusion-model-experiments.jpg", "Model Experiments Page") }}

Create a new experiment by clicking "New Experiment" on the top right corner.  Enter the name the description of this experiment.  Click "Create New Experiment".

{{ figure("/models/assets/training/fusion-create-experiment.jpg", "Model Experiments Page") }}

Navigate to the "Training Sessions".

{{ figure("/models/assets/training/fusion-training-sessions.jpg", "Training Sessions") }}

Create a new training session by clicking on the "New Session" button on the top right corner.

{{ figure("/models/assets/training/new-session-button.jpg", "New Session Button") }}

Follow the settings indicated and keep the rest of the settings by their default.  Click "Start Session" to start the training session.

!!! warning "Session Name"
    Do not include any forward slash "/" in the session names as this can result in missing model artifacts.

{{ figure("/models/assets/training/fusion-train-settings.jpg", "Start Training Session") }}

The session progress will be shown like the following below.

{{ figure("/models/assets/training/fusion-session-progress.jpg", "Training Session Progress") }}

Once completed the session card will appear like the following below.

{{ figure("/models/assets/training/fusion-completed-session.jpg", "Completed Session") }}

On the train session card, expand the session details.

{{ figure("/models/assets/training/fusion-view-train-details.jpg", "Training Details") }}

The trained models will be listed under "Artifacts".  

| Session Details                                                | Artifacts                                                                     |
|----------------------------------------------------------------|-------------------------------------------------------------------------------|
| ![session](../../models/assets/training/fusion-session-details.jpg) | ![artifacts](../../models/assets/training/fusion-session-artifacts.jpg) |
