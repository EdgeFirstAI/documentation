# Train a Fusion Model

Before you can start training your model, check that the dataset meets the following requirements:

- [x] Complete Annotations (2D and 3D bounding boxes and segmentation masks/polygons)
- [x] Contains [training and validation partitions](../../datasets/tutorials/management.md#split-dataset)
- [x] Contains a [dataset tag/version](../../datasets/tutorials/management.md#tag-dataset)

Once you have a fully annotated dataset with a training and validation partition, you can begin training your model.  This will briefly show the steps for training a model, but for an in depth tutorial, please see [Training Fusion Models](../../models/training/fusion.md).

Navigate back to the "Projects" page.

{{ figure("/studio/assets/navigation/go-to-projects-page.jpg", "Go to Projects Page") }}

From the "Projects" page, click on "Model Experiments" of your project.

{{ figure("/models/assets/training/model-experiments.jpg", "Model Experiments Page") }}

Create a new experiment by clicking "New Experiment" on the top right corner.  Enter the name the description of this experiment.  Click "Create New Experiment".

{{ figure("/models/assets/training/create-experiment.jpg", "Model Experiments Page") }}

Navigate to the "Training Sessions".

{{ figure("/models/assets/training/training-sessions.jpg", "Training Sessions") }}

Create a new training session by clicking the "Actions" dropdown menu on the top right of the page and then click the "+ New Trainer Session" button.

{{ figure("/models/assets/training/new-fusion-session-button.jpg", "New Session Button") }}

Follow the settings indicated and keep the rest of the settings by their default.  Click "Start Session" to start the training session.

{{ figure("/models/assets/training/fusion-train-settings.jpg", "Start Training Session") }}

The session progress will be shown like the following below.

{{ figure("/models/assets/training/fusion-session-progress.jpg", "Training Session Progress") }}

Once the session is complete, the session card will appear like the following.

{{ figure("/models/assets/training/fusion-completed-session.jpg", "Completed Session") }}

Click the training session card for more information.

{{ figure("/models/assets/training/fusion-view-train-details.jpg", "Training Details") }}

The trained models will be listed under "Artifacts".  

{{ figure("/models/assets/training/fusion-session-artifacts.jpg", "Model Artifacts") }}
