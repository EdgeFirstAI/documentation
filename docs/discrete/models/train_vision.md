# Train Vision Model

Now that you have a fully annotated dataset that with training and validation samples, you can start training a Vision model.  This will briefly show the steps for training a model, but for an in depth tutorial, please see [Training Vision Models](../../models/training/vision.md).

Navigate back to the "Projects" page.  You can go back to the "Projects" page by clicking the Apps Menu waffle button on the top right of the Navigation bar.  Click the first selection to take you to the "Projects page".

{{ figure("/studio/assets/navigation/apps-menu.png", "Apps Menu") }}

From the "Projects" page, click on "Model Experiments" of your project.

{{ figure("/models/assets/training/vision-model-experiments.jpg", "Model Experiments Page") }}

Create a new experiment by clicking "New Experiment" on the top right corner.  Enter the name the description of this experiment.  Click "Create New Experiment".

{{ figure("/models/assets/training/vision-create-experiment.jpg", "Model Experiments Page") }}

Navigate to the "Training Sessions".

{{ figure("/models/assets/training/vision-training-sessions.jpg", "Training Sessions") }}

Create a new training session by clicking on the "New Session" button on the top right corner.

{{ figure("/models/assets/training/new-session-button.jpg", "New Session Button") }}

Follow the settings indicated and keep the rest of the settings by their default.  Click "Start Session" to start the training session.

!!! warning "Session Name"
    Do not include any forward slash "/" in the session names as this can result in missing model artifacts.

{{ figure("/models/assets/training/vision-train-settings.jpg", "Start Training Session") }}

!!! warning "No Datasets Available"

    In case there are no datasets visible on the dropdown (3).  Please refresh your browser.

The session progress will be shown like the following below.

{{ figure("/models/assets/training/vision-session-progress.jpg", "Training Session Progress") }}

Once completed the session card will appear like the following below.

{{ figure("/models/assets/training/vision-completed-session.jpg", "Completed Session") }}

On the train session card, expand the session details.

{{ figure("/models/assets/training/vision-view-train-details.jpg", "Training Details") }}

The trained models will be listed under "Artifacts".  

| Session Details                                                | Artifacts                                                                     |
|----------------------------------------------------------------|-------------------------------------------------------------------------------|
| ![session](../../models/assets/training/vision-session-details.jpg) | ![artifacts](../../models/assets/training/vision-session-artifacts.jpg) |
