# Training Vision Models

This tutorial describes the steps to train **Vision** models in EdgeFirst Studio.  Recall that Vision models are models that perform object detection in camera frames or images.  EdgeFirst Studio is capable of training ModelPack and Ultralytics object detection models.  For a tutorial to train Fusion models, see [Training Fusion Models](fusion.md).

## View Dataset

First ensure that the dataset is ready to be used for training.  This means that the dataset meets all of the criteria listed below.

- [x] Complete Annotations (bounding boxes and/or segmentation masks/polygons)
- [x] Contains training and validation partitions
- [x] Contains a dataset tag/version

The section [View Dataset](../../datasets/tutorials/management.md#view-dataset) will show an example of a completed dataset.

## Specify Project Experiments

From the [Projects page](../../studio/projects.md), choose the project that contains the dataset you plan to use.  In this example, the project chosen is called "My First Project".  Next click the "Model Experiments" button as indicated in red.

{{ figure("../assets/training/model-experiments.jpg", "Model Experiments") }}

{% include-markdown "discrete/models/create_model_experiments.md" %}

## Create Training Session

In the experiment card, click the "Training Sessions" button as indicated in red below.

{{ figure("../assets/training/training-sessions.jpg", "Training Sessions") }}

You will be greeted to the "Training Sessions" page as shown below.  

{{ figure("../assets/training/training-sessions-page.jpg", "Training Sessions Page") }}

Start a training session by clicking on the "Actions" button on the top right corner of the page and then click "+ New" as indicated.

{{ figure("../assets/training/new-session-button.jpg", "New Session Button") }}

Select the trainer, either "ModelPack" or "Ultralytics".  Both trainers run as Studio apps on cloud GPU instances, and Studio opens the launch form of the selected trainer.  Provide a name and description of the training session and specify the dataset to be used for training and validation.  In this example, the dataset specified is the "Coffee Cup" dataset which was used as an example under the [Getting Started](../../getting_started/capture_data.md).  Next specify the training parameters.  Additional information on these parameters are provided by hovering over the info button ![Info Button](../../assets/buttons/studio-info-button.jpg).

!!! tip "Input Resolution"
    For ModelPack, we recommend changing the input resolution to 640x360 to maximize detection rates on small datasets.

!!! warning "Large Batch Size"
    For small datasets, a large batch size may produce poor results. Use a batch size of 4 or 8.

For more information on available "Data Augmentations" please see [Vision Augmentations](../augmentations.md).

The launch forms of both trainers start with the same three groups.

| Group | Description |
|-------|-------------|
| **Training Session** | The **Name** and optional **Description** of the training session.  The name is also used to name the artifacts. |
| **Source Dataset** | The dataset the session trains and validates on, with its annotation set and tag. |
| **Destination Experiment** | The experiment the training session is created in.  Artifacts and charts are published there when the session finishes. |

The groups that follow depend on the trainer.

| Trainer | Groups | Parameter Reference |
|---------|--------|---------------------|
| **ModelPack** | Input (Input Resolution, Camera Adaptor, Input Tiling (SAHI), Letterbox Resize), Model Parameters, Training Parameters, Data Augmentation, Export Parameters | [ModelPack Training Parameters](../modelpack/index.md#training-parameters) |
| **Ultralytics** | Input (Input Resolution), Task Selection, Training (Weights, Enable Training and its training settings), Export Parameters | [Ultralytics Training Parameters](../ultralytics/index.md#training-parameters) |

Click "Start Session" to start the training session.

### Weights and Enable Training

The two trainers start from different weights.

- **ModelPack** always trains.  The backbone starts from ImageNet-pretrained weights and the detection and segmentation heads start fresh.
- **Ultralytics** has a **Weights** field and an **Enable Training** toggle in its Training group.  **Weights** is either **Pretrained (COCO)** (default), the Ultralytics COCO weights for the selected model, or a previous Ultralytics training session, whose published weights bring their own model definition.  **Enable Training** is off by default.

| Weights | Enable Training | Ultralytics Session Behavior |
|---------|-----------------|------------------------------|
| Pretrained (COCO) | Off | **Default.** No training.  The session exports the COCO pretrained weights (80 classes) at the selected Input Resolution.  This lets you reproduce validation and profiling results from the [EdgeFirst Model Zoo on Hugging Face](https://huggingface.co/spaces/EdgeFirst/Models) using the published COCO checkpoints. |
| Pretrained (COCO) | On | Fine-tunes the COCO pretrained weights on the selected dataset. |
| A previous training session | On | Fine-tunes the weights published by that session on the selected dataset. |
| A previous training session | Off | No training.  The session exports that session's weights at the Input Resolution and Deployment chosen on the form, for example to deploy tile-trained weights whole frame. |

A session with **Enable Training** off validates the exported model and reports the results as its final validation metrics.  It runs no epochs, so its loss and learning-rate charts stay empty.  See [Weights Source](../ultralytics/index.md#weights-source) for the details.

!!! warning "COCO pretrained weights and dataset compatibility"
    **Pretrained (COCO)** weights without training detect the 80 COCO classes.  When your dataset classes differ from the COCO classes, the session skips validation, and the model's class outputs do not correspond to your labels.  Turn on **Enable Training** to fine-tune the weights on your dataset.

!!! failure "InsufficientInstanceCapacity"

    {{ img("/studio/assets/models/insufficient-capacity-error.jpg", "InsufficientInstanceCapacity Error") }}

    If you see this error after starting your training session, retry creating the session. This can happen when AWS reports that no EC2 instances are currently available to launch; the current workaround is to retry.

## Session Progress

Once the training session has started, the progress with the stages will be shown on the left and additional information and status is shown on the right.

{{ figure("../assets/training/vision-session-progress.jpg", "Training Session") }}

The training process begins with cloud instance initialization. Then the dataset is downloaded and cached.  Training starts afterwards.
At the end of the training process, the model is exported and the model artifacts are published on the training session, available for download.

## Completed Session

The completed session will look as follows with the status set to "Complete".

{{ figure("../assets/training/vision-completed-session.jpg", "Completed Session") }}

The attributes of the training sessions in EdgeFirst Studio are labeled below.

{{ figure("../assets/training/training-session-attributes.jpg", "Training Session Attributes") }}

## Training Outcomes

Once the training session completes, you can view the training charts by clicking the "view training session charts" button on the top of the session card.

{{ figure("../assets/training/vision-charts.jpg", "Training Charts") }}

You can go back to the training session card by pressing the "Back" button as indicated in red below on the top left corner of the page.

{{ figure("../assets/training/back-button.jpg", "Back to the Session Card") }}

The trained model artifacts can be downloaded by clicking the session card.  This will open the session details and the models are listed under the "Artifacts" tab as shown below.  Click on the downward arrows to download the models to your PC.

{{ figure("../assets/training/vision-session-artifacts.jpg", "Training Session Artifacts") }}

It is also possible to compare the training metrics for multiple sessions.  See [Training Sessions](../../studio/models.md#training-sessions) in the Model Experiments Dashboard for further details.

!!! info "Netron"
    You can visualize the architecture of these models using [https://netron.app/](https://netron.app/).

## Next Steps

Now that you have trained your model, you can validate the performance of your model either [on target/device](../validation/vision/user_managed.md) or on the [cloud](../validation/vision/managed.md).
