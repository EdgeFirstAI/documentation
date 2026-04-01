# Model Experiments Dashboard

A model experiment is a container of training and validation sessions in the experiment.  The following figure shown is the "Model Experiments" page.  This page will contain all the experiments that were started by the user.

{{ figure("assets/models/experiments-page.jpg", "Project Experiments") }}

The following figure breaks down the elements of an "Experiment" card.

{{ figure("assets/models/model-experiment-attributes.jpg", "Experiment Attributes") }}

An experiment will contain child training and validation sessions.  The training sessions and validation sessions will be described in more detail in the sections below.

#### Training Sessions

Training sessions take in datasets and synthesize from them new AI models for object recognition (Vision) or object perception (Fusion).

From the "Model Experiments" page, we can click on the "Training Sessions" button with the icon ![Trainers Button](../assets/buttons/studio-trainers-button.png) to see the training sessions in the experiment.  The figure below shows the layout of the training session cards under the "Training Sessions" page.

{{ figure("assets/models/training-sessions.jpg", "Training Sessions") }}

The following figure describes the attributes of any given training session.

{{ figure("../models/assets/training/training-session-attributes.jpg", "Training Session Attributes") }}

To compare all the training charts of each session, click on "All Charts" at the top right corner of the "Training Sessions" page.  This will show the charts from each session overlaid on top of one another for a quick comparison.

{{ figure("assets/models/all-charts.jpg", "All Charts") }}

All the training charts will be displayed with a legend that indicates the training session.

{{ figure("assets/models/all-training-charts.jpg", "All Charts") }}

For more details regarding deploying training sessions, please see [Training Vision Models](../models/training/vision.md) and [Training Fusion Models](../models/training/fusion.md) for training Fusion models.

#### Validation Sessions

The validation sessions will assess the performance of the models in the training sessions.  A training session can have any number of validation sessions.  From the "Model Experiments" page, we can click on the "Validation Sessions" button with the icon ![Validation Button](../assets/buttons/studio-validation-button.jpg) to see the validation sessions in the experiment.  The figure below shows the layout of the validation session cards under the "Validation Sessions" page.

{{ figure("assets/models/validation-sessions.jpg", "Validation Sessions") }}

The following figure describes the attributes of any given validation session.

{{ figure("../models/assets/validation/validation-session-attributes.jpg", "Validation Session Attributes") }}

To compare the validation charts of each session, click on "Compare" at the top right corner of the "Validate Sessions" page.  This will show the charts of each validation session side-by-side for a quick comparison.

{{ figure("assets/models/compare-validation-sessions.jpg", "Compare Validation Sessions") }}

Next select the validation session results you wish to compare.  Once selected, click "Compare" to show the validation charts side-by-side.

{{ figure("assets/models/validation-sessions-to-compare.jpg", "Select Validation Sessions") }}

Now the charts for each session are displayed side-by-side.  All the charts for a single training session will be shown in one column.  A new column indicates another session.

{{ figure("assets/models/validation-charts-comparison.jpg", "Comparing Validation Sessions") }}

There are two types of validation: **managed** and **user-managed**. Managed validations are set to default in EdgeFirst Studio which triggers an EC2 instance that downloads the dataset and the inference model for validation. This type of validation is best used if you do not have an embedded platform to deploy the model. User-managed validations are hosted in embedded platforms where the dataset and the inference model will be downloaded. This type of validation is best used if you have an embedded platform available to verify how the model would perform in the platform and determine the model's inference time when deployed.

For more details regarding deploying validation sessions, please see [Validating Vision Models](../models/validation/vision/managed.md) and [Validating Fusion Models](../models/validation/fusion/managed.md) for validating Fusion models.

## Next Steps

Now that you are familiar with the layout of the Model Experiments Dashboard, proceed to the next section for learning more about the context of the [Cloud Instances Dashboard](instances.md).
