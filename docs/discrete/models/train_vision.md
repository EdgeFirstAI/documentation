# Train Vision Model

Now that your dataset is fully annotated, tagged, and split into training and validation partitions, you are ready to begin training your model.  This guide briefly shows the steps for training a model, but for an in depth tutorial, please see [Training Vision Models](../../models/training/vision.md).

Navigate back to the "Projects" page.  You can go back to the "Projects" page by clicking the "PROJECTS" button on the top navbar as shown.

{{ figure("/studio/assets/navigation/go-to-projects-page.jpg", "Go to Projects Page") }}

From the "Projects" page, click on "Model Experiments" of your project.

{{ figure("/models/assets/training/model-experiments.jpg", "Model Experiments Page") }}

Create a new experiment by clicking "New Experiment" on the top right corner.  Enter the name and the description of this experiment.  Click "Create New Experiment".

{{ figure("/models/assets/training/create-experiment.jpg", "Model Experiments Page") }}

Navigate to the "Training Sessions".

{{ figure("/models/assets/training/training-sessions.jpg", "Training Sessions") }}

Start a new training session by clicking the "Actions" dropdown menu on the top right of the page.  From here you can either train [ModelPack](../../models/modelpack/index.md) or [Ultralytics](../../models/ultralytics/index.md) models.  In this guide, we will demonstrate starting a ModelPack session.

{{ figure("/models/assets/training/new-mpk-session-button.jpg", "New Session Button") }}

Follow the settings indicated and keep the rest of the settings default.  Click "Start Session" to start the training session.

!!! note "Outdated training panel"
    The following training configuration panel is currently out of date.  Additional formatting fixes to the current panel are still in progress before we can push a new image of the layout.

{{ figure("/models/assets/training/vision-train-settings.jpg", "Start Training Session") }}

The session progress will be shown like the following below.

{{ figure("/models/assets/training/vision-session-progress.jpg", "Training Session Progress") }}

Once the session is complete, the session card will appear like the following. Click the training session card for more information.

{{ figure("/models/assets/training/vision-view-train-details.jpg", "Training Details") }}

The trained models will be listed under the "Artifacts" tab.  The download button next to these artifacts will download the artifacts to your machine.

{{ figure("/models/assets/training/vision-session-artifacts.jpg", "Model Artifacts") }}

Now that you have trained your model, you can also find various model converters and exporters in EdgeFirst Studio that builds supported model formats for specific compute hardware.  The next section will give you a quick overview of the available model converters in EdgeFirst Studio to see its intended supported target.
